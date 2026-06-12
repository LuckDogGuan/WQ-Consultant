from __future__ import annotations

import logging
import threading
import time
import concurrent.futures
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import requests
from typing import Any

from ..storage import get_setting, update_job, add_job_event, add_check_result, upsert_alpha, connect
from ..job_runner import JobRunner
from .wq_client import login_with_credentials
from .simulation_service import is_in_blocked_window, handle_reconnect

logger = logging.getLogger(__name__)


def count_today_checks() -> int:
    """统计中国时间今天已经运行的 check 数量"""
    try:
        sh_tz = ZoneInfo("Asia/Shanghai")
        today_str = datetime.now(sh_tz).strftime("%Y-%m-%d")
        with connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM check_results WHERE strftime('%Y-%m-%d', created_at) = strftime('%Y-%m-%d', ?)",
                (datetime.now().isoformat(),) # SQLite date string comparison fallback
            ).fetchone()
            
            # 严格一点，使用 Python 进行 ISO 日期时间解析和过滤
            rows = conn.execute("SELECT created_at FROM check_results").fetchall()
            count = 0
            for r in rows:
                dt = datetime.fromisoformat(r["created_at"])
                dt_sh = dt.astimezone(sh_tz)
                if dt_sh.strftime("%Y-%m-%d") == today_str:
                    count += 1
            return count
    except Exception as e:
        logger.error(f"Error counting today's checks: {e}")
        return 0


def check_limits_and_wait_check(job_id: int, session_container: dict[str, Any], session_lock: threading.Lock) -> None:
    """check_submission 模块的额度限制拦截器"""
    runner = JobRunner()
    while True:
        runner.check_paused(job_id)
        
        # 1. 禁用时间段不限制 check_submission，但限制 simulation。
        # 2. check 额度限制校验
        check_limit = int(get_setting("check_daily_limit", "4500"))
        today_count = count_today_checks()
        if today_count >= check_limit:
            poll_minutes = float(get_setting("poll_minutes", "20"))
            
            # 刷新窗口检查
            sh_tz = ZoneInfo("Asia/Shanghai")
            now_sh = datetime.now(sh_tz)
            now_time = now_sh.strftime("%H:%M")
            is_refresh_window = "12:00" <= now_time <= "14:00"
            sleep_seconds = 300 if is_refresh_window else int(poll_minutes * 60)
            
            msg = f"Check daily limit reached ({today_count}/{check_limit}). Waiting {sleep_seconds // 60}m for reset..."
            update_job(job_id, status="waiting_limit", message=msg)
            
            slept = 0
            while slept < sleep_seconds:
                runner.check_paused(job_id)
                time.sleep(10)
                slept += 10
            continue
            
        update_job(job_id, status="running")
        break


def check_alpha_remotely(s: requests.Session, alpha_id: str) -> tuple[str, float | None, str, dict[str, Any]]:
    """查询远程 WorldQuant API 以核验 Alpha 的 checks"""
    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/check"
    resp = s.get(url, timeout=30)
    
    if resp.status_code == 401:
        raise ConnectionResetError("Session expired (401)")
    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 5))
        time.sleep(retry_after)
        resp = s.get(url, timeout=30)
        
    if resp.status_code != 200:
        return "ERROR", None, f"HTTP Error {resp.status_code}", {}
        
    data = resp.json()
    if data.get("is", 0) == 0:
        raise ConnectionResetError("Logged out indicator in body")
        
    checks = data.get("is", {}).get("checks", [])
    checks_df = pd.DataFrame(checks)
    
    if checks_df.empty:
        return "ERROR", None, "No check results found in response", data
        
    # 获取 PROD_CORRELATION
    prod_corr = None
    if "name" in checks_df.columns and "value" in checks_df.columns:
        corr_rows = checks_df[checks_df.name == "PROD_CORRELATION"]
        if not corr_rows.empty:
            val = corr_rows["value"].values[0]
            try:
                prod_corr = float(val)
            except Exception:
                pass
                
    # 判定是否有 FAIL
    if "result" in checks_df.columns:
        has_fail = any(checks_df["result"] == "FAIL")
        if has_fail:
            failed_items = checks_df[checks_df.result == "FAIL"]["name"].tolist()
            return "FAIL", prod_corr, f"Failed checks: {', '.join(failed_items)}", data
        else:
            return "PASS", prod_corr, "", data
            
    return "ERROR", None, "Invalid checks schema", data


def run_check_job(job_id: int, params: dict[str, Any]) -> None:
    """JobRunner 调用的 check_submission 后台任务"""
    from consultant_core.machine_lib import get_recent_alphas
    
    runner = JobRunner()
    
    # 1. 整理与合并三来源候选
    update_job(job_id, message="Constructing check submission queue...")
    
    region = get_setting("region", "USA")
    universe = get_setting("universe", "TOP3000")
    
    # 来源 1：最近的 submit 候选
    lookback = int(get_setting("submit_lookback_days", "30"))
    sharpe = float(get_setting("submit_sharpe", "1.58"))
    fitness = float(get_setting("submit_fitness", "1.0"))
    alpha_num = int(get_setting("submit_alpha_num", "200"))
    
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    if not username or not password:
        raise ValueError("Missing WorldQuant credentials in Settings.")
        
    logger.info("Fetching recent submit candidates from WorldQuant Brain...")
    session = login_with_credentials(username, password)
    
    recent_submit_ids = []
    try:
        recent_alphas = get_recent_alphas(
            lookback_days=lookback,
            sharpe_th=sharpe,
            fitness_th=fitness,
            region=region,
            universe=universe,
            alpha_num=alpha_num,
            usage="submit",
            session=session,
            verbose=False
        )
        recent_submit_ids = [rec[0] for rec in recent_alphas]
    except Exception as e:
        logger.error(f"Failed to fetch recent submit candidates: {e}")
    finally:
        session.close()
        
    # 来源 2：本地相关性分析的 PPA/RA/ATOM 优质候选
    correlation_candidates = []
    try:
        with connect() as conn:
            # 获取 PPA/RA/ATOM 且未 check 或上次结果为 ERROR 的
            rows = conn.execute(
                """
                SELECT alpha_id FROM alpha_records 
                WHERE alpha_type IN ('PPA', 'RA', 'ATOM')
                  AND (
                    alpha_id NOT IN (SELECT alpha_id FROM check_results)
                    OR alpha_id IN (SELECT alpha_id FROM check_results WHERE result = 'ERROR')
                  )
                """
            ).fetchall()
            correlation_candidates = [r["alpha_id"] for r in rows]
    except Exception as e:
        logger.error(f"Failed to fetch correlation candidates from DB: {e}")
        
    # 来源 3：用户手动粘贴的 ids
    manual_ids = params.get("manual_ids", [])
    
    # 合并排重并记录来源
    id_sources: dict[str, list[str]] = {}
    
    for aid in recent_submit_ids:
        id_sources.setdefault(aid, []).append("recent_submit")
    for aid in correlation_candidates:
        id_sources.setdefault(aid, []).append("correlation_candidate")
    for aid in manual_ids:
        # 去除首尾空格
        clean_aid = str(aid).strip()
        if clean_aid:
            id_sources.setdefault(clean_aid, []).append("manual")
            
    check_queue = list(id_sources)
    total_checks = len(check_queue)
    
    msg = f"Check queue constructed. Total unique candidates: {total_checks} (Recent: {len(recent_submit_ids)}, Corr: {len(correlation_candidates)}, Manual: {len(manual_ids)})."
    logger.info(msg)
    update_job(job_id, message=msg)
    add_job_event(job_id, "info", msg, {
        "unique_count": total_checks,
        "recent_submit_count": len(recent_submit_ids),
        "correlation_candidate_count": len(correlation_candidates),
        "manual_count": len(manual_ids)
    })
    
    if total_checks == 0:
        update_job(job_id, message="No candidates to check.", progress_current=100, progress_total=100)
        return
        
    # 2. 启动 3 线程并发检查
    session_container = {"session": login_with_credentials(username, password)}
    session_lock = threading.Lock()
    reconnect_count = 0
    completed_count = 0
    
    def check_worker(alpha_id: str) -> dict[str, Any]:
        nonlocal reconnect_count
        runner.check_paused(job_id)
        
        # 额度与时间段检查
        check_limits_and_wait_check(job_id, session_container, session_lock)
        
        attempts = 0
        while attempts < 3:
            runner.check_paused(job_id)
            with session_lock:
                current_session = session_container["session"]
            
            try:
                result, prod_corr, error_msg, payload = check_alpha_remotely(current_session, alpha_id)
                sources_str = ",".join(id_sources[alpha_id])
                
                # 写入 check_results
                add_check_result(
                    alpha_id=alpha_id,
                    result=result,
                    prod_corr=prod_corr,
                    message=error_msg,
                    source=sources_str,
                    payload=payload
                )
                
                # 同步更新 alpha_records
                with connect() as conn:
                    conn.execute(
                        """
                        UPDATE alpha_records 
                        SET prod_corr = ?, status = ?, updated_at = datetime('now')
                        WHERE alpha_id = ?
                        """,
                        (prod_corr, f"CHECKED_{result}", alpha_id)
                    )
                    
                return {
                    "alpha_id": alpha_id,
                    "result": result,
                    "prod_corr": prod_corr,
                    "error_msg": error_msg
                }
                
            except (requests.exceptions.RequestException, OSError, ConnectionResetError) as exc:
                attempts += 1
                logger.warning(f"Connection error checking {alpha_id}: {exc}. Retry {attempts}/3")
                
                if attempts >= 3:
                    # 触发断开重连逻辑
                    with session_lock:
                        if session_container["session"] == current_session:
                            try:
                                new_session = handle_reconnect(job_id, reconnect_count)
                                session_container["session"] = new_session
                                reconnect_count += 1
                            except Exception:
                                pass
                    attempts = 0  # 重置尝试以在重连后继续
                time.sleep(5)
                
        return {"alpha_id": alpha_id, "result": "ERROR", "prod_corr": None, "error_msg": "Max connection retries exceeded"}

    # 3. 线程池分发
    threads_num = int(get_setting("check_threads", "3"))
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads_num) as executor:
            futures = {executor.submit(check_worker, aid): aid for aid in check_queue}
            for future in concurrent.futures.as_completed(futures):
                runner.check_paused(job_id)
                completed_count += 1
                pct = int((completed_count / total_checks) * 100)
                
                res = future.result()
                msg = f"[{completed_count}/{total_checks}] Check {res['alpha_id']}: {res['result']} | Prod Corr: {res['prod_corr'] or 'N/A'}"
                if res['error_msg']:
                    msg += f" | Msg: {res['error_msg']}"
                    
                logger.info(msg)
                update_job(job_id, progress_current=completed_count, progress_total=total_checks, message=msg)
                
    finally:
        with session_lock:
            session_container["session"].close()
            logger.info("WorldQuant session closed in check job.")

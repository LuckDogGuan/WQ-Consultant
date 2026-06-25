from __future__ import annotations

import logging
import threading
import time
import concurrent.futures
import json
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
import requests
from typing import Any

from ..storage import get_setting, update_job, add_job_event, add_check_result, upsert_alpha, connect
from ..job_runner import JobRunner
from .wq_client import login_with_credentials
from .simulation_service import is_in_blocked_window, handle_reconnect

logger = logging.getLogger(__name__)


# Thread-safe global cache for today's check counts
_today_checks_cache_lock = threading.Lock()
_today_checks_cache: dict[str, int] = {}  # Key: "YYYY-MM-DD" Shanghai date, Value: count


def count_today_checks() -> int:
    """统计中国时间今天已经运行的 check 数量"""
    try:
        sh_tz = ZoneInfo("Asia/Shanghai")
        today_str = datetime.now(sh_tz).strftime("%Y-%m-%d")
        
        # Check cache first
        with _today_checks_cache_lock:
            if today_str in _today_checks_cache:
                return _today_checks_cache[today_str]
                
        # If cache miss, query using UTC range filter based on Shanghai today
        start_sh = datetime.strptime(today_str, "%Y-%m-%d").replace(tzinfo=sh_tz)
        start_utc = start_sh.astimezone(timezone.utc)
        end_utc = start_utc + timedelta(days=1)
        
        start_utc_str = start_utc.isoformat()
        end_utc_str = end_utc.isoformat()
        
        with connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM check_results WHERE created_at >= ? AND created_at < ?",
                (start_utc_str, end_utc_str)
            ).fetchone()
            count = row["n"] if row else 0
            
        with _today_checks_cache_lock:
            # Clear older keys to avoid cache leak/accumulation
            _today_checks_cache.clear()
            _today_checks_cache[today_str] = count
            
        return count
    except Exception as e:
        logger.error(f"Error counting today's checks: {e}")
        return 0


def increment_today_checks_cache() -> None:
    """递增今日缓存的 check 计数"""
    try:
        sh_tz = ZoneInfo("Asia/Shanghai")
        today_str = datetime.now(sh_tz).strftime("%Y-%m-%d")
        with _today_checks_cache_lock:
            if today_str in _today_checks_cache:
                _today_checks_cache[today_str] += 1
    except Exception as e:
        logger.error(f"Error incrementing today's checks cache: {e}")


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
    
    for attempt in range(5):
        resp = s.get(url, timeout=30)
        
        if resp.status_code == 401:
            raise ConnectionResetError("Session expired (401)")
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 5))
            sleep_time = min(60, retry_after)
            logger.warning(f"Rate limited (429) checking {alpha_id}. Sleeping for {sleep_time}s...")
            time.sleep(sleep_time)
            continue
            
        if resp.status_code != 200:
            return "ERROR", None, f"HTTP Error {resp.status_code}", {}
            
        try:
            data = resp.json()
        except Exception as je:
            logger.warning(f"JSONDecodeError checking {alpha_id}: {je}. Response: {resp.text[:200]}")
            raise requests.exceptions.ContentDecodingError(f"Invalid JSON response: {je}", response=resp)
            
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
                    
        # 判定是否有 FAIL / FAILED / ERROR
        if "result" in checks_df.columns:
            results_upper = checks_df["result"].astype(str).str.upper()
            is_fail_mask = results_upper.isin({"FAIL", "FAILED", "ERROR"})
            if is_fail_mask.any():
                failed_details = []
                for _, chk in checks_df[is_fail_mask].iterrows():
                    chk_name = str(chk.get("name", ""))
                    chk_val = chk.get("value")
                    chk_lim = chk.get("limit")
                    if pd.notna(chk_val) and pd.notna(chk_lim):
                        try:
                            val_f = float(chk_val)
                            lim_f = float(chk_lim)
                            failed_details.append(f"{chk_name}(value:{val_f:.4f},limit:{lim_f:.4f})")
                        except Exception:
                            failed_details.append(f"{chk_name}(value:{chk_val},limit:{chk_lim})")
                    elif pd.notna(chk_val):
                        failed_details.append(f"{chk_name}(value:{chk_val})")
                    else:
                        failed_details.append(chk_name)
                
                error_msg = f"Failed checks: {', '.join(failed_details)}"
                return "FAIL", prod_corr, error_msg, data
            else:
                return "PASS", prod_corr, "", data
                
        return "ERROR", None, "Invalid checks schema", data
        
    return "ERROR", None, "Max 429 retries exceeded", {}


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
    
    timezone_name = get_setting("alpha_date_timezone", "Asia/Shanghai")
    fetch_limit_multiplier = int(get_setting("alpha_fetch_limit_multiplier", "3"))
    try:
        from consultant_core.machine_lib import get_alphas_full, recent_alpha_date_range
        start_date, end_date = recent_alpha_date_range(
            lookback,
            timezone_name=timezone_name
        )
        fetch_limit = max(alpha_num, alpha_num * fetch_limit_multiplier)
        
        alpha_df = get_alphas_full(
            start_date=start_date,
            end_date=end_date,
            sharpe_th=sharpe,
            fitness_th=fitness,
            region=region,
            limit=fetch_limit,
            usage="submit",
            session=session,
            min_instrument_count=101,
        )
        
        if not alpha_df.empty:
            if "universe" in alpha_df.columns:
                alpha_df = alpha_df[alpha_df["universe"] == universe]
            alpha_df = alpha_df.head(alpha_num)
            
            for _, row in alpha_df.iterrows():
                upsert_alpha({
                    "alpha_id": row["alpha_id"],
                    "alpha_type": "",
                    "name": row.get("name") or "",
                    "region": row.get("region") or region,
                    "universe": row.get("universe") or universe,
                    "sharpe": row.get("sharpe"),
                    "fitness": row.get("fitness"),
                    "margin": row.get("margin"),
                    "returns": row.get("returns"),
                    "drawdown": row.get("drawdown"),
                    "status": row.get("status") or "UNSUBMITTED",
                    "source": "recent_submit",
                    "payload": dict(row)
                })
            recent_submit_ids = alpha_df["alpha_id"].tolist()
        else:
            recent_submit_ids = []
    except Exception as e:
        logger.error(f"Failed to fetch recent submit candidates: {e}")
    finally:
        session.close()
        
    # 来源 2：本地相关性分析的 PPA/RA/ATOM 优质候选
    correlation_candidates = []
    try:
        from datetime import timezone, timedelta
        check_lookback = int(get_setting("check_lookback_days", "60"))
        check_max = int(get_setting("check_max_candidates", "4000"))
        cutoff_date = (datetime.now(timezone.utc) - timedelta(days=check_lookback)).isoformat()
        
        with connect() as conn:
            rows = conn.execute(
                """
                SELECT alpha_id FROM alpha_records 
                WHERE alpha_type IN ('PPA', 'RA', 'ATOM')
                  AND created_at >= ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (cutoff_date, check_max)
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
    
    # 增量断点恢复：过滤自当前 Job 创建时间以来，已写入 check_results 的记录
    with connect() as conn:
        job_row = conn.execute("SELECT created_at FROM jobs WHERE id = ?", (job_id,)).fetchone()
        job_created_at = job_row["created_at"] if job_row else "1970-01-01 00:00:00"
        
        finished_ids = {
            r["alpha_id"] 
            for r in conn.execute(
                "SELECT alpha_id FROM check_results WHERE created_at >= ? AND result != 'ERROR'", 
                (job_created_at,)
            ).fetchall()
        }
        
    check_queue = [aid for aid in check_queue if aid not in finished_ids]
    total_checks = len(check_queue) + len(finished_ids)
    
    msg = f"Check queue constructed. Total unique candidates: {total_checks} (Already check: {len(finished_ids)}, Pending: {len(check_queue)})."
    logger.info(msg)
    update_job(job_id, message=msg)
    add_job_event(job_id, "info", msg, {
        "unique_count": total_checks,
        "recent_submit_count": len(recent_submit_ids),
        "correlation_candidate_count": len(correlation_candidates),
        "manual_count": len(manual_ids)
    })
    
    if len(check_queue) == 0:
        update_job(job_id, message="All check candidates already processed.", progress_current=total_checks, progress_total=total_checks)
        return
        
    # 2. 启动 3 线程并发检查
    session_container = {"session": login_with_credentials(username, password)}
    session_lock = threading.Lock()
    reconnect_count = 0
    completed_count = len(finished_ids)
    
    def check_worker(alpha_id: str) -> dict[str, Any]:
        nonlocal reconnect_count
        runner.check_paused(job_id)
        
        # 额度与时间段检查
        check_limits_and_wait_check(job_id, session_container, session_lock)
        
        sources_str = ",".join(id_sources.get(alpha_id, []))
        
        # 尝试从本地数据库中获取已有的详情
        existing_record = None
        try:
            with connect() as conn:
                row = conn.execute(
                    "SELECT * FROM alpha_records WHERE alpha_id = ?",
                    (alpha_id,)
                ).fetchone()
                if row:
                    existing_record = dict(row)
        except Exception as e:
            logger.error(f"Error querying local alpha record {alpha_id}: {e}")
            
        try:
            attempts = 0
            last_exc_msg = "Unknown error"
            while attempts < 3:
                runner.check_paused(job_id)
                with session_lock:
                    current_session = session_container["session"]
                
                try:
                    result, prod_corr, error_msg, check_payload = check_alpha_remotely(current_session, alpha_id)
                    
                    # Fetch online details to save to alpha_records so we have all metrics
                    detail_data = {}
                    is_cached = False
                    
                    if existing_record and existing_record.get("sharpe") is not None:
                        try:
                            if existing_record.get("payload"):
                                detail_data = json.loads(existing_record["payload"])
                                if "is" not in detail_data:
                                    detail_data["is"] = {}
                                if "settings" not in detail_data:
                                    detail_data["settings"] = {}
                                is_cached = True
                        except Exception:
                            pass
                            
                    if not is_cached:
                        detail_resp = current_session.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}", timeout=30)
                        if detail_resp.status_code == 200:
                            detail_data = detail_resp.json()
                        elif detail_resp.status_code == 401:
                            raise ConnectionResetError("Session expired (401)")
                        elif detail_resp.status_code == 429:
                            retry_after = int(detail_resp.headers.get("Retry-After", 5))
                            sleep_time = min(60, retry_after)
                            logger.warning(f"Rate limited (429) getting details for {alpha_id}. Sleeping for {sleep_time}s...")
                            time.sleep(sleep_time)
                            attempts += 1
                            continue
                            
                    is_metrics = detail_data.get("is", {})
                    settings = detail_data.get("settings", {})
                    
                    # Fallback to existing columns if we fetched details but got empty dict (non-200 etc.)
                    if not is_metrics and existing_record:
                        is_metrics = {
                            "sharpe": existing_record.get("sharpe"),
                            "fitness": existing_record.get("fitness"),
                            "margin": existing_record.get("margin"),
                            "returns": existing_record.get("returns"),
                            "drawdown": existing_record.get("drawdown")
                        }
                    if not settings and existing_record:
                        settings = {
                            "region": existing_record.get("region") or region,
                            "universe": existing_record.get("universe") or universe
                        }
                    
                    # 写入 check_results
                    add_check_result(
                        alpha_id=alpha_id,
                        result=result,
                        prod_corr=prod_corr,
                        message=error_msg,
                        source=sources_str,
                        payload=check_payload
                    )
                    increment_today_checks_cache()
                    
                    # 同步 upsert_alpha
                    upsert_alpha({
                        "alpha_id": alpha_id,
                        "alpha_type": "",  # ON CONFLICT CASE will preserve existing
                        "name": detail_data.get("name") or (existing_record.get("name") if existing_record else "") or "",
                        "region": settings.get("region") or region,
                        "universe": settings.get("universe") or universe,
                        "sharpe": is_metrics.get("sharpe"),
                        "fitness": is_metrics.get("fitness"),
                        "margin": is_metrics.get("margin"),
                        "returns": is_metrics.get("returns"),
                        "drawdown": is_metrics.get("drawdown"),
                        "prod_corr": prod_corr,
                        "status": f"CHECKED_{result}",
                        "source": sources_str,
                        "payload": detail_data
                    })
                    
                    # 适当延迟以平滑并发请求速率
                    time.sleep(0.5)
                    
                    return {
                        "alpha_id": alpha_id,
                        "result": result,
                        "prod_corr": prod_corr,
                        "error_msg": error_msg
                    }
                    
                except (requests.exceptions.RequestException, OSError, ConnectionResetError, ValueError) as exc:
                    attempts += 1
                    last_exc_msg = str(exc)
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
            
            # If we hit max retries
            err_msg = f"Max connection retries exceeded: {last_exc_msg}"
            add_check_result(
                alpha_id=alpha_id,
                result="ERROR",
                prod_corr=None,
                message=err_msg,
                source=sources_str,
                payload={}
            )
            increment_today_checks_cache()
            return {"alpha_id": alpha_id, "result": "ERROR", "prod_corr": None, "error_msg": err_msg}
            
        except Exception as e:
            err_msg = f"Unexpected error: {e}"
            logger.error(f"Unexpected error checking {alpha_id}: {e}", exc_info=True)
            try:
                add_check_result(
                    alpha_id=alpha_id,
                    result="ERROR",
                    prod_corr=None,
                    message=err_msg,
                    source=sources_str,
                    payload={}
                )
                increment_today_checks_cache()
            except Exception:
                pass
            return {"alpha_id": alpha_id, "result": "ERROR", "prod_corr": None, "error_msg": err_msg}

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


def run_inline_checks(session: Any, alpha_ids: list[str]) -> None:
    """在回测任务中穿插调用的 Checks 检查逻辑"""
    if not alpha_ids:
        return
    logger.info(f"Running inline checks for {len(alpha_ids)} alphas...")
    for aid in alpha_ids:
        try:
            result, prod_corr, error_msg, check_payload = check_alpha_remotely(session, aid)
            # 写入 check_results
            add_check_result(
                alpha_id=aid,
                result=result,
                prod_corr=prod_corr,
                message=error_msg,
                source="inline_backtest",
                payload=check_payload
            )
            # 更新 alpha_records 里的最新状态
            with connect() as conn:
                conn.execute(
                    "UPDATE alpha_records SET status = ?, prod_corr = ?, updated_at = datetime('now') WHERE alpha_id = ?",
                    (f"CHECKED_{result}", prod_corr, aid)
                )
            logger.info(f"Inline check for {aid}: {result} (Prod Corr={prod_corr})")
        except Exception as ex:
            logger.error(f"Failed to run inline checks for {aid}: {ex}")


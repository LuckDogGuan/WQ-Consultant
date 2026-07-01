from __future__ import annotations

import logging
import json
import requests
import time
from datetime import datetime, timedelta
from typing import Any

from app.storage import connect, get_settings, upsert_alpha, create_job, utc_now
from app.job_runner import update_job, add_job_event, JobRunner
from app.services.wq_client import login_with_credentials
from consultant_core.machine_lib import get_alphas_full

logger = logging.getLogger(__name__)


def _completed_sync_chunks(region: str) -> set[tuple[str, str]]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT chunk_start, chunk_end
            FROM sync_chunks
            WHERE kind = 'wq_sync' AND region = ? AND status = 'success'
            """,
            (region,),
        ).fetchall()
    return {(row["chunk_start"], row["chunk_end"]) for row in rows}


def _record_sync_chunk(region: str, st: Any, ed: Any, status: str, fetched_count: int = 0, error: str = "") -> None:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO sync_chunks(kind, region, chunk_start, chunk_end, status, fetched_count, error, updated_at)
            VALUES ('wq_sync', ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(kind, region, chunk_start, chunk_end) DO UPDATE SET
                status = excluded.status,
                fetched_count = excluded.fetched_count,
                error = excluded.error,
                updated_at = excluded.updated_at
            """,
            (region, st.isoformat(), ed.isoformat(), status, int(fetched_count), str(error)[:1000], utc_now()),
        )

def run_sync_alphas_job(job_id: int, params: dict[str, Any]) -> None:
    """同步云端因子任务：拉取最近 30 天因子，将未记录的新增因子添加入库，并自动触发评估"""
    lookback_days = int(params.get("lookback_days", 30))
    
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    
    if not username or not password:
        raise ValueError("请先在设置中配置 WQ 账号和密码。")
        
    update_job(job_id, status="running", message="正在连接 WorldQuant Brain 平台...", progress_current=10, progress_total=100)
    add_job_event(job_id, "info", f"Logging in to WQ platform as {username}...")
    
    session = login_with_credentials(username.strip(), password.strip())
    
    try:
        update_job(job_id, message=f"正在拉取最近 {lookback_days} 天的已回测因子记录...", progress_current=30, progress_total=100)
        
        # 拉取时间区间
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)
        region = settings.get("region", "USA")
        
        logger.info(f"[SyncJob] Fetching all alphas for region {region} from {start_date.isoformat()} to {end_date.isoformat()} concurrently in chunks.")
        
        # 将天数切分为 1 天的分片以绕过 WQ 10k offset 截断限制。成功分片会落库，后续同步不重复拉取。
        import pandas as pd
        
        today = datetime.now().date()
        all_chunks = []
        for i in range(lookback_days + 1):
            st = today - timedelta(days=lookback_days - i)
            ed = st + timedelta(days=1)
            all_chunks.append((st, ed))
        completed_chunks = _completed_sync_chunks(region)
        chunks = [(st, ed) for st, ed in all_chunks if (st.isoformat(), ed.isoformat()) not in completed_chunks]
            
        dfs = []
        failed_chunks = []
        skipped_count = len(all_chunks) - len(chunks)
        
        def fetch_chunk(st, ed):
            logger.info(f"[SyncJob] Thread starting chunk fetch: {st.strftime('%Y-%m-%d')} to {ed.strftime('%Y-%m-%d')}")
            return get_alphas_full(
                start_date=st,
                end_date=ed,
                sharpe_th=-10.0,
                region=region,
                usage="submit",
                session=session,
                order="-dateCreated",
                limit=100000
            )
            
        for idx, (st, ed) in enumerate(chunks, start=1):
            JobRunner().check_paused(job_id)
            update_job(
                job_id,
                message=f"正在同步 {st.strftime('%Y-%m-%d')} ({idx}/{len(chunks)}，已跳过成功分片 {skipped_count} 个)...",
                progress_current=30 + int((idx / max(1, len(chunks))) * 30),
                progress_total=100,
            )
            last_error = ""
            for attempt in range(1, 4):
                try:
                    df_chunk = fetch_chunk(st, ed)
                    if not df_chunk.empty:
                        logger.info(f"[SyncJob] Chunk {st.strftime('%Y-%m-%d')} to {ed.strftime('%Y-%m-%d')} fetched {len(df_chunk)} alphas.")
                        dfs.append(df_chunk)
                    else:
                        logger.info(f"[SyncJob] Chunk {st.strftime('%Y-%m-%d')} to {ed.strftime('%Y-%m-%d')} empty.")
                    _record_sync_chunk(region, st, ed, "success", len(df_chunk), "")
                    break
                except Exception as exc:
                    last_error = str(exc)
                    logger.error(f"[SyncJob] Chunk {st.strftime('%Y-%m-%d')} to {ed.strftime('%Y-%m-%d')} attempt {attempt}/3 failed: {exc}")
                    _record_sync_chunk(region, st, ed, "failed", 0, last_error)
                    if attempt < 3:
                        time.sleep(attempt * 5)
                        try:
                            session.close()
                        except Exception:
                            pass
                        session = login_with_credentials(username.strip(), password.strip())
            else:
                failed_chunks.append((st, ed, last_error))
                    
        session.close()
        
        if dfs:
            alphas_df = pd.concat(dfs, ignore_index=True)
            alphas_df = alphas_df.drop_duplicates(subset=["alpha_id"])
        else:
            alphas_df = pd.DataFrame()
        
        if alphas_df.empty and not failed_chunks:
            update_job(job_id, status="completed", message="云端没有查询到最近 30 天的回测因子记录。", progress_current=100, progress_total=100)
            add_job_event(job_id, "info", f"No simulated alphas found; skipped {skipped_count} already-synced day chunk(s).")
            return
            
        update_job(job_id, message="正在比对本地数据库，过滤重复因子...", progress_current=60, progress_total=100)
        
        # 获取本地已有的所有 alpha_id
        with connect() as conn:
            existing_rows = conn.execute("SELECT alpha_id FROM alpha_records").fetchall()
            existing_ids = {r["alpha_id"] for r in existing_rows}
            
        synced_count = 0
        new_count = 0
        
        for _, row in alphas_df.iterrows():
            alpha_id = row.get("alpha_id")
            if not alpha_id:
                continue
                
            synced_count += 1
            
            # 仅新增没有添加到记录中的因子
            if alpha_id in existing_ids:
                logger.debug(f"[SyncJob] Alpha {alpha_id} already exists in database, skipping.")
                continue
                
            upsert_alpha({
                "alpha_id": alpha_id,
                "alpha_type": "",  # 初始留空，由下一阶段评估任务评级
                "name": row.get("name") or "",
                "region": region,
                "universe": row.get("universe") or settings.get("universe", "TOP3000"),
                "sharpe": row.get("sharpe"),
                "fitness": row.get("fitness"),
                "margin": row.get("margin"),
                "returns": row.get("returns"),
                "drawdown": row.get("drawdown"),
                "status": row.get("status") or "UNSUBMITTED",
                "source": "wq_sync",
                "payload": dict(row)
            })
            new_count += 1
            
        add_job_event(job_id, "info", f"Fetched {synced_count} alphas; added {new_count} new alphas to database; skipped {skipped_count} completed day chunk(s).")
        
        if new_count > 0:
            update_job(job_id, message=f"同步完成，共新增 {new_count} 个因子。正在启动评估校验任务...", progress_current=85, progress_total=100)
            
            # 自动创建并触发本地评估与校验任务
            new_job_id = create_job(
                "alpha_inspection", 
                f"自动评估新增云端因子 ({new_count} 个)", 
                {"only_new": True}
            )
            JobRunner().start_job(new_job_id, "alpha_inspection", {"only_new": True})
            
            update_job(
                job_id, 
                status="completed", 
                message=f"同步完成，新增 {new_count} 个因子。已自动触发评估任务 Job #{new_job_id}。", 
                progress_current=100, 
                progress_total=100
            )
        else:
            update_job(
                job_id, 
                status="completed", 
                message="同步完成，云端最近 30 天的因子均已存在于本地数据库中，无需新增。", 
                progress_current=100, 
                progress_total=100
            )

        if failed_chunks:
            failed_days = ", ".join(st.strftime("%Y-%m-%d") for st, _, _ in failed_chunks[:5])
            add_job_event(job_id, "warning", f"{len(failed_chunks)} day chunk(s) failed and will be retried next sync: {failed_days}")
            update_job(
                job_id,
                status="completed",
                message=f"同步完成，但 {len(failed_chunks)} 个日期分片拉取失败；已成功分片不会重复，下次同步会重试：{failed_days}",
                progress_current=100,
                progress_total=100,
            )
            
    except Exception as e:
        logger.error(f"[SyncJob] Sync failed: {e}", exc_info=True)
        raise e


def run_alpha_inspection_job(job_id: int, params: dict[str, Any]) -> None:
    """批量对未做自相关性检测、核查或缺失 IS/OS 统计的因子进行自动校验与优化"""
    from app.services.background_inspector import BackgroundInspector
    from app.services.template_iteration import grade_candidate_result
    from app.services.optimization_planner import _extract_yearly_stats
    
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    
    if not username or not password:
        raise ValueError("请先在设置中配置 WQ 账号 and 密码。")
        
    update_job(job_id, status="running", message="正在分析待评估的因子列表...", progress_current=5, progress_total=100)
    
    # 1. 查找所有未被标记为 garbage 的因子
    with connect() as conn:
        rows = conn.execute("SELECT * FROM alpha_records WHERE is_garbage = 0").fetchall()
        
    candidates = []
    
    for row in rows:
        row_dict = dict(row)
        alpha_id = row_dict["alpha_id"]
        prod_corr = row_dict.get("prod_corr")
        status = str(row_dict.get("status") or "").upper()
        payload_str = row_dict.get("payload")
        
        payload = {}
        if payload_str:
            try:
                payload = json.loads(payload_str)
            except Exception:
                pass
                
        # 计算当前因子的评级以校验其他缺失指标
        sharpe = row_dict.get("sharpe")
        fitness = row_dict.get("fitness")
        margin = row_dict.get("margin")
        yearly_stats = _extract_yearly_stats(payload)
        turnover = row_dict.get("turnover") or (yearly_stats[0].get("turnover") if yearly_stats else None)
        self_corr = row_dict.get("ppa_corr") or 0.0
        prod_corr_val = prod_corr or 0.0
        
        grading = grade_candidate_result({
            "sharpe": sharpe,
            "fitness": fitness,
            "margin": margin,
            "turnover": turnover,
            "self_corr": self_corr,
            "prod_corr": prod_corr_val,
            "status": status,
            "payload": payload,
        })
        grade = grading.get("grade", "C")

        # 0. 垃圾/D级因子发现 -> 立即触发物理退休删除
        if grade == "D":
            candidates.append((row_dict, "RETIRE"))
            continue
            
        # A. 自相关性检测缺失 (prod_corr IS NULL 或 0.0) -> 必须是已提交/已校验过 (status != 'UNSUBMITTED')
        # 否则 UNSUBMITTED 没有 PNL 无法在本地算自相关，须先进行 CHECK 提交生成 PNL
        if (prod_corr is None or prod_corr == 0.0) and status != 'UNSUBMITTED':
            candidates.append((row_dict, "CORR"))
            continue
            
        # B. 评级 C 级及以上，状态为 UNSUBMITTED，且没有本地 check 记录 -> 自动远程 Checks 校验
        if grade in {"S", "A", "B", "C"} and status == "UNSUBMITTED":
            with connect() as conn:
                chk_row = conn.execute("SELECT id FROM check_results WHERE alpha_id = ?", (alpha_id,)).fetchone()
            if not chk_row:
                candidates.append((row_dict, "CHECK"))
                continue
                
        # C. 评级 C 级及以上，但缺少年度分解数据 (yearly-stats) -> 补充明细数据
        if grade in {"S", "A", "B", "C"}:
            if not yearly_stats:
                candidates.append((row_dict, "FETCH"))
                continue
                
    total_candidates = len(candidates)
    if total_candidates == 0:
        update_job(job_id, status="completed", message="分析完成，没有发现需要做自相关或 IS/OS 校验的因子。", progress_current=100, progress_total=100)
        return
        
    add_job_event(job_id, "info", f"Found {total_candidates} alphas needing inspection. Starting workflow...")
    
    session = login_with_credentials(username.strip(), password.strip())
    inspector = BackgroundInspector()
    
    try:
        for idx, (row_dict, work_type) in enumerate(candidates, start=1):
            # 支持用户在界面上“暂停”任务
            JobRunner().check_paused(job_id)
            
            alpha_id = row_dict["alpha_id"]
            action_desc = ""
            if work_type == "RETIRE":
                action_desc = "垃圾因子物理退休"
            elif work_type == "CORR":
                action_desc = "自相关性补算"
            elif work_type == "CHECK":
                action_desc = "远程 Checks 提交校验"
            elif work_type == "FETCH":
                action_desc = "获取年度 PnL 数据"
                
            msg = f"[{idx}/{total_candidates}] 正在对 {alpha_id} 进行{action_desc}..."
            update_job(job_id, message=msg, progress_current=idx, progress_total=total_candidates)
            add_job_event(job_id, "info", f"Processing {alpha_id}: WorkType={work_type}")
            
            if work_type == "RETIRE":
                inspector._run_retire(session, alpha_id, row_dict)
            elif work_type == "CHECK":
                inspector._run_check_submit(session, alpha_id, row_dict)
            elif work_type == "CORR":
                inspector._run_autocorrelation(session, alpha_id, row_dict)
            elif work_type == "FETCH":
                inspector._run_fetch_pnl_details(session, alpha_id, row_dict)
                
        update_job(
            job_id, 
            status="completed", 
            message=f"自动评估优化已圆满完成！共处理了 {total_candidates} 个因子。", 
            progress_current=total_candidates, 
            progress_total=total_candidates
        )
        add_job_event(job_id, "info", f"All {total_candidates} alpha inspections completed.")
        
    except Exception as e:
        logger.error(f"[InspectionJob] Inspection failed: {e}", exc_info=True)
        raise e
    finally:
        session.close()


def run_sync_local_alphas_job(job_id: int, params: dict[str, Any]) -> None:
    """同步本地因子任务：计算本地所有 C 级别及以上已回测因子的自相关性"""
    from app.services.background_inspector import BackgroundInspector
    from app.services.template_iteration import grade_candidate_result
    from app.services.optimization_planner import _extract_yearly_stats
    
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    
    if not username or not password:
        raise ValueError("请先在设置中配置 WQ 账号和密码。")
        
    update_job(job_id, status="running", message="正在获取本地已提交因子列表...", progress_current=5, progress_total=100)
    
    # 查找所有未被标记为 garbage 且不是 UNSUBMITTED 的因子（因为 UNSUBMITTED 没有 PNL，无法在本地算自相关）
    with connect() as conn:
        rows = conn.execute("SELECT * FROM alpha_records WHERE is_garbage = 0 AND status != 'UNSUBMITTED'").fetchall()
        
    candidates = []
    for row in rows:
        row_dict = dict(row)
        payload_str = row_dict.get("payload")
        payload = {}
        if payload_str:
            try:
                payload = json.loads(payload_str)
            except Exception:
                pass
                
        sharpe = row_dict.get("sharpe")
        fitness = row_dict.get("fitness")
        margin = row_dict.get("margin")
        yearly_stats = _extract_yearly_stats(payload)
        turnover = row_dict.get("turnover") or (yearly_stats[0].get("turnover") if yearly_stats else None)
        self_corr = row_dict.get("ppa_corr") or 0.0
        prod_corr_val = row_dict.get("prod_corr") or 0.0
        
        # 实时判定级别
        grading = grade_candidate_result({
            "sharpe": sharpe,
            "fitness": fitness,
            "margin": margin,
            "turnover": turnover,
            "self_corr": self_corr,
            "prod_corr": prod_corr_val,
            "status": row_dict.get("status") or "",
            "payload": payload,
        })
        grade = grading.get("grade", "C")
        
        # 仅同步 C 级别及以上的因子
        if grade in {"S", "A", "B", "C"}:
            candidates.append(row_dict)
            
    total_candidates = len(candidates)
    if total_candidates == 0:
        update_job(job_id, status="completed", message="同步完成，本地没有发现需要计算自相关的 C 级及以上因子。", progress_current=100, progress_total=100)
        return
        
    add_job_event(job_id, "info", f"Found {total_candidates} local C-and-above alphas for correlation check.")
    
    session = login_with_credentials(username.strip(), password.strip())
    inspector = BackgroundInspector()
    
    try:
        # 预先跑一次 download_correlation_data 以拉取最新 OS/PPA 收益率缓存
        update_job(job_id, message="正在更新本地 OS/PPA 因子 PnL 缓存库...", progress_current=10, progress_total=100)
        from app.services.background_inspector import download_correlation_data
        download_correlation_data(session, flag_increment=True)
        
        for idx, row_dict in enumerate(candidates, start=1):
            JobRunner().check_paused(job_id)
            alpha_id = row_dict["alpha_id"]
            progress_pct = 10 + int((idx / total_candidates) * 90)
            
            update_job(
                job_id, 
                message=f"[{idx}/{total_candidates}] 正在更新 {alpha_id} 的自相关与评级/改名...", 
                progress_current=progress_pct, 
                progress_total=100
            )
            
            try:
                # _run_autocorrelation 会做: 1.算相关性 2._update_alpha_grade_and_status 3.远程改名
                inspector._run_autocorrelation(session, alpha_id, row_dict)
            except Exception as e:
                logger.error(f"[SyncLocalAlphas] Autocorrelation check failed for {alpha_id}: {e}")
                add_job_event(job_id, "warning", f"Alpha {alpha_id} correlation calculation failed: {e}")
                
        update_job(
            job_id, 
            status="completed", 
            message=f"本地因子自相关同步计算已全部完成！共处理了 {total_candidates} 个因子。", 
            progress_current=100, 
            progress_total=100
        )
    except Exception as e:
        logger.error(f"[SyncLocalAlphasJob] Job failed: {e}", exc_info=True)
        raise e
    finally:
        session.close()

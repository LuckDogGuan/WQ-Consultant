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

def fix_missing_metrics(session: requests.Session) -> None:
    """批量从 WQ 平台拉取和修补本地数据库中缺失 returns/drawdown 等静态指标的非垃圾因子"""
    logger.info("[SyncJob] Starting fix_missing_metrics execution...")
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT alpha_id FROM alpha_records 
            WHERE is_garbage = 0 
              AND (returns IS NULL OR drawdown IS NULL OR fitness IS NULL)
            """
        ).fetchall()
    
    missing_ids = [row["alpha_id"] for row in rows]
    if not missing_ids:
        logger.info("[SyncJob] No alphas with missing metrics found.")
        return
        
    logger.info(f"[SyncJob] Found {len(missing_ids)} alphas with missing metrics. Starting batch fetch...")
    
    batch_size = 50
    for i in range(0, len(missing_ids), batch_size):
        batch = missing_ids[i:i+batch_size]
        id_filter = "%1F".join(batch)
        url = f"https://api.worldquantbrain.com/users/self/alphas?id={id_filter}&fields=id,is.sharpe,is.fitness,is.margin,is.returns,is.drawdown"
        
        results = []
        for attempt in range(1, 4):
            try:
                resp = session.get(url, timeout=30)
                is_rate_limited = False
                if resp.status_code in (403, 429):
                    is_rate_limited = True
                else:
                    try:
                        resp_json = resp.json()
                        if isinstance(resp_json, dict) and "rate limit" in str(resp_json.get("message", "")).lower():
                            is_rate_limited = True
                    except Exception:
                        pass
                
                if is_rate_limited:
                    retry_after = 15 * attempt
                    if resp.status_code in (403, 429) and resp.headers.get("Retry-After"):
                        try:
                            retry_after = max(retry_after, int(resp.headers.get("Retry-After")))
                        except Exception:
                            pass
                    logger.warning(f"[SyncJob] Rate limited during metrics repair (status={resp.status_code}). Attempt {attempt}/3, sleeping for {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    break
                else:
                    logger.warning(f"[SyncJob] Query failed (status={resp.status_code}). Attempt {attempt}/3...")
                    time.sleep(2 * attempt)
            except Exception as e:
                logger.warning(f"[SyncJob] Error during request: {e}. Attempt {attempt}/3...")
                time.sleep(2 * attempt)
        else:
            logger.error(f"[SyncJob] Batch {i//batch_size + 1} failed after 3 attempts. Skipping batch.")
            time.sleep(5)
            continue
            
        if results:
            with connect() as conn:
                for alpha in results:
                    aid = alpha.get("id")
                    metrics = alpha.get("is") or {}
                    sharpe = metrics.get("sharpe")
                    fitness = metrics.get("fitness")
                    margin = metrics.get("margin")
                    returns = metrics.get("returns")
                    drawdown = metrics.get("drawdown")
                    
                    conn.execute(
                        """
                        UPDATE alpha_records 
                        SET sharpe = COALESCE(?, sharpe),
                            fitness = COALESCE(?, fitness),
                            margin = COALESCE(?, margin),
                            returns = COALESCE(?, returns),
                            drawdown = COALESCE(?, drawdown),
                            updated_at = datetime('now')
                        WHERE alpha_id = ?
                        """,
                        (sharpe, fitness, margin, returns, drawdown, aid)
                    )
        logger.info(f"[SyncJob] Successfully repaired metrics for batch {i//batch_size + 1}/{(len(missing_ids)-1)//batch_size + 1} (Fetched {len(results)} records)")
        time.sleep(0.8)

def run_get_server_alphas_job(job_id: int, params: dict[str, Any]) -> None:
    """获取服务器因子任务：拉取最近 30 天满足 Sharpe >= 1.25, Fitness >= 0.60, Margin >= 0.0005 的新因子，并对其中的 S 级因子进行自相关计算"""
    lookback_days = int(params.get("lookback_days", 30))
    
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    
    if not username or not password:
        raise ValueError("请先在设置中配置 WQ 账号和密码。")
        
    def to_float(val):
        try: return float(val) if val is not None else None
        except: return None
        
    update_job(job_id, status="running", message="正在连接 WorldQuant Brain 平台...", progress_current=10, progress_total=100)
    add_job_event(job_id, "info", f"Logging in to WQ platform as {username}...")
    
    session = login_with_credentials(username.strip(), password.strip())
    
    try:
        update_job(job_id, message=f"正在拉取最近 {lookback_days} 天的云端因子记录...", progress_current=30, progress_total=100)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)
        region = settings.get("region", "USA")
        
        logger.info(f"[GetServerAlphasJob] Fetching alphas for region {region} from {start_date.isoformat()} to {end_date.isoformat()} in chunks.")
        
        import pandas as pd
        today = datetime.now().date()
        
        # 清除今天和昨天的同步分片缓存以防遗漏
        delete_threshold_date = today - timedelta(days=1)
        with connect() as conn:
            conn.execute(
                """
                DELETE FROM sync_chunks
                WHERE kind = 'wq_sync' AND region = ? AND chunk_end >= ?
                """,
                (region, delete_threshold_date.isoformat())
            )
            
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
                message=f"正在拉取服务器因子 {st.strftime('%Y-%m-%d')} (分片 {idx}/{len(chunks)})...",
                progress_current=30 + int((idx / max(1, len(chunks))) * 25),
                progress_total=100,
            )
            last_error = ""
            for attempt in range(1, 4):
                try:
                    df_chunk = fetch_chunk(st, ed)
                    if not df_chunk.empty:
                        dfs.append(df_chunk)
                    _record_sync_chunk(region, st, ed, "success", len(df_chunk), "")
                    break
                except Exception as exc:
                    last_error = str(exc)
                    logger.error(f"[GetServerAlphasJob] Chunk {st.strftime('%Y-%m-%d')} attempt {attempt}/3 failed: {exc}")
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
                    
        # 增量修补缺失 metrics
        try:
            update_job(job_id, message="正在从 WQ 平台修补静态属性...", progress_current=55, progress_total=100)
            fix_missing_metrics(session)
        except Exception as e:
            logger.error(f"[GetServerAlphasJob] Metrics repair failed: {e}")
            
        if dfs:
            alphas_df = pd.concat(dfs, ignore_index=True)
            alphas_df = alphas_df.drop_duplicates(subset=["alpha_id"])
        else:
            alphas_df = pd.DataFrame()
            
        if alphas_df.empty and not failed_chunks:
            update_job(job_id, status="completed", message="服务器没有查询到最近 30 天的因子记录。", progress_current=100, progress_total=100)
            return
            
        update_job(job_id, message="正在过滤不满足条件或重复的因子...", progress_current=60, progress_total=100)
        
        # 1. 过滤：Sharpe >= 1.25, Fitness >= 0.60, Margin >= 0.0005
        def filter_row(row):
            sh = to_float(row.get("sharpe"))
            fit = to_float(row.get("fitness"))
            marg = to_float(row.get("margin"))
            return (sh is not None and sh >= 1.25) and (fit is not None and fit >= 0.60) and (marg is not None and marg >= 0.0005)
            
        filtered_rows = [row for _, row in alphas_df.iterrows() if filter_row(row)]
        
        # 2. 与本地查重
        with connect() as conn:
            existing_rows = conn.execute("SELECT alpha_id FROM alpha_records").fetchall()
            existing_ids = {r["alpha_id"] for r in existing_rows}
            
        new_candidates = []
        for row in filtered_rows:
            alpha_id = row.get("alpha_id")
            if alpha_id and alpha_id not in existing_ids:
                new_candidates.append(row)
                
        if not new_candidates:
            update_job(job_id, status="completed", message="过滤完成，未发现符合阈值要求的新增因子。", progress_current=100, progress_total=100)
            return
            
        # 3. 入库并筛选出定级为 S 级的因子
        from app.services.background_inspector import BackgroundInspector
        from app.services.template_iteration import grade_candidate_result
        from app.services.optimization_planner import _extract_yearly_stats
        
        s_candidates = []
        for idx, row in enumerate(new_candidates, start=1):
            alpha_id = row.get("alpha_id")
            payload = dict(row)
            
            sharpe = to_float(row.get("sharpe"))
            fitness = to_float(row.get("fitness"))
            margin = to_float(row.get("margin"))
            yearly_stats = _extract_yearly_stats(payload)
            turnover = to_float(row.get("turnover")) or (yearly_stats[0].get("turnover") if yearly_stats else None)
            
            # 实时评级判定
            grading = grade_candidate_result({
                "sharpe": sharpe,
                "fitness": fitness,
                "margin": margin,
                "turnover": turnover,
                "self_corr": 0.0,
                "prod_corr": 0.0,
                "status": row.get("status") or "UNSUBMITTED",
                "payload": payload,
            })
            grade = grading.get("grade", "C")
            
            # 入库
            upsert_alpha({
                "alpha_id": alpha_id,
                "alpha_type": grade,
                "name": row.get("name") or "",
                "region": region,
                "universe": row.get("universe") or settings.get("universe", "TOP3000"),
                "sharpe": sharpe,
                "fitness": fitness,
                "margin": margin,
                "returns": to_float(row.get("returns")),
                "drawdown": to_float(row.get("drawdown")),
                "status": row.get("status") or "UNSUBMITTED",
                "source": "get_server_alphas",
                "payload": payload
            })
            
            if grade == "S":
                with connect() as conn:
                    inserted_row = conn.execute("SELECT * FROM alpha_records WHERE alpha_id = ?", (alpha_id,)).fetchone()
                    if inserted_row:
                        s_candidates.append(dict(inserted_row))
                        
        total_new = len(new_candidates)
        total_s = len(s_candidates)
        add_job_event(job_id, "info", f"Successfully synced {total_new} new alphas. Found {total_s} S-grade alphas.")
        
        # 4. 对新因子中 S 级的因子进行本地自相关性计算
        if total_s > 0:
            inspector = BackgroundInspector()
            update_job(job_id, message="正在更新本地 OS/PPA 因子 PnL 缓存库...", progress_current=70, progress_total=100)
            from app.services.background_inspector import download_correlation_data
            download_correlation_data(session, flag_increment=True)
            
            for s_idx, row_dict in enumerate(s_candidates, start=1):
                JobRunner().check_paused(job_id)
                alpha_id = row_dict["alpha_id"]
                progress_pct = 70 + int((s_idx / total_s) * 30)
                
                update_job(
                    job_id,
                    message=f"[{s_idx}/{total_s}] 正在计算 S 级因子 {alpha_id} 的自相关...",
                    progress_current=progress_pct,
                    progress_total=100
                )
                try:
                    inspector._run_autocorrelation(session, alpha_id, row_dict)
                except Exception as e:
                    logger.error(f"[GetServerAlphasJob] Autocorrelation failed for {alpha_id}: {e}")
                    add_job_event(job_id, "warning", f"S-grade Alpha {alpha_id} correlation failed: {e}")
                time.sleep(1.0)
                
        update_job(
            job_id, 
            status="completed", 
            message=f"获取服务器因子任务已全部完成！共新增入库 {total_new} 个因子，并对其中 {total_s} 个 S 级因子计算了自相关性。", 
            progress_current=100, 
            progress_total=100
        )
        
        if failed_chunks:
            failed_days = ", ".join(st.strftime("%Y-%m-%d") for st, _, _ in failed_chunks[:5])
            add_job_event(job_id, "warning", f"{len(failed_chunks)} day chunk(s) failed and will be retried next sync: {failed_days}")
            update_job(
                job_id,
                status="completed",
                message=f"获取完毕，但 {len(failed_chunks)} 个日期分片拉取失败，下次会自动重试：{failed_days}",
                progress_current=100,
                progress_total=100,
            )
    except Exception as e:
        logger.error(f"[GetServerAlphasJob] Job failed: {e}", exc_info=True)
        raise e


def run_alpha_inspection_job(job_id: int, params: dict[str, Any]) -> None:
    """批量对未做自相关性检测、核查或静态指标缺失的因子进行自动校验与优化"""
    from app.services.background_inspector import BackgroundInspector
    from app.services.template_iteration import grade_candidate_result
    from app.services.optimization_planner import _extract_yearly_stats
    
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    
    if not username or not password:
        raise ValueError("请先在设置中配置 WQ 账号 and 密码。")
        
    update_job(job_id, status="running", message="正在分析待评估的因子列表...", progress_current=5, progress_total=100)
    
    only_new = params.get("only_new", False) if isinstance(params, dict) else False
    
    # 1. 根据 only_new 分支读取待处理因子
    with connect() as conn:
        if only_new:
            # 仅处理最近同步且未评级的因子
            rows = conn.execute(
                "SELECT * FROM alpha_records WHERE is_garbage = 0 AND (alpha_type IS NULL OR alpha_type = '')"
            ).fetchall()
        else:
            # 全量巡检正常因子
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
                
        pnl_fetched = payload.get("pnl_fetched", False)
        self_corr_checked = payload.get("self_corr_checked", False)
        
        # 计算当前因子的评级以校验其他指标
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
            
        # 1. 检查 Checkpoint 1: pnl_fetched
        if not pnl_fetched:
            candidates.append((row_dict, "FETCH_PRECHECK"))
            continue
            
        # 2. 检查 Checkpoint 2: self_corr_checked (自相关性检测)
        if not self_corr_checked:
            candidates.append((row_dict, "CORR"))
            continue
            
        sim_status = str(payload.get("status") or "").upper()
        if sim_status in {"ERROR", "FAIL"}:
            # 如果是仿真 Error/Fail 因子，且数据库中的状态还没打上 ERROR/FAIL，需要触发 CORR 来自动标记并改名
            if status not in {"ERROR", "FAIL"}:
                candidates.append((row_dict, "CORR"))
            continue
            
        # 3. 评级 C 级及以上，状态为 UNSUBMITTED，且没有本地 check 记录 -> 自动远程 Checks 校验
        if grade in {"S", "A", "B", "C"} and status == "UNSUBMITTED":
            with connect() as conn:
                chk_row = conn.execute("SELECT id FROM check_results WHERE alpha_id = ?", (alpha_id,)).fetchone()
            if not chk_row:
                candidates.append((row_dict, "CHECK"))
                continue
                
        # 4. 评级 C 级及以上，但缺少年度分解数据 (yearly-stats) -> 补充明细数据并最终评级重命名
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
        # 重置自相关比对缓存库，保证本轮任务手动运行能拉取最新数据
        inspector.correlation_cache = None
        for idx, (row_dict, work_type) in enumerate(candidates, start=1):
            # 支持用户在界面上“暂停”任务
            JobRunner().check_paused(job_id)
            
            alpha_id = row_dict["alpha_id"]
            action_desc = ""
            if work_type == "RETIRE":
                action_desc = "垃圾因子物理退休"
            elif work_type == "FETCH_PRECHECK":
                action_desc = "拉取详情与时序"
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
            elif work_type == "FETCH_PRECHECK":
                inspector._fetch_alpha_precheck_data(session, alpha_id, row_dict)
            elif work_type == "CHECK":
                inspector._run_check_submit(session, alpha_id, row_dict)
            elif work_type == "CORR":
                inspector._run_autocorrelation(session, alpha_id, row_dict)
            elif work_type == "FETCH":
                inspector._run_fetch_pnl_details(session, alpha_id, row_dict)
                
            # 引入自适应休眠延迟，避免短时高频请求 WQ API 触发 429 频控限制
            time.sleep(1.0)
                
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


def run_refresh_correlation_job(job_id: int, params: dict[str, Any]) -> None:
    """刷新自相关性任务：只对本地 S 级别的因子进行本地自相关性计算"""
    from app.services.background_inspector import BackgroundInspector
    
    settings = get_settings()
    username = settings.get("wq_username")
    password = settings.get("wq_password")
    
    if not username or not password:
        raise ValueError("请先在设置中配置 WQ 账号和密码。")
        
    update_job(job_id, status="running", message="正在获取本地 S 级因子列表...", progress_current=5, progress_total=100)
    
    # 仅查找本地评级为 S 级且非垃圾的因子
    with connect() as conn:
        rows = conn.execute("SELECT * FROM alpha_records WHERE is_garbage = 0 AND alpha_type = 'S'").fetchall()
        
    candidates = [dict(row) for row in rows]
    total_candidates = len(candidates)
    
    if total_candidates == 0:
        update_job(job_id, status="completed", message="刷新完成，本地未发现 S 等级的因子。", progress_current=100, progress_total=100)
        return
        
    add_job_event(job_id, "info", f"Found {total_candidates} local S-grade alphas for autocorrelation check.")
    
    session = login_with_credentials(username.strip(), password.strip())
    inspector = BackgroundInspector()
    
    try:
        # 预先拉取最新 OS/PPA 收益率缓存
        update_job(job_id, message="正在更新本地 OS/PPA 因子 PnL 缓存库...", progress_current=10, progress_total=100)
        from app.services.background_inspector import download_correlation_data
        download_correlation_data(session, flag_increment=True)
        
        for idx, row_dict in enumerate(candidates, start=1):
            JobRunner().check_paused(job_id)
            alpha_id = row_dict["alpha_id"]
            progress_pct = 10 + int((idx / total_candidates) * 90)
            
            update_job(
                job_id, 
                message=f"[{idx}/{total_candidates}] 正在更新 S 级因子 {alpha_id} 的自相关与评级...", 
                progress_current=progress_pct, 
                progress_total=100
            )
            
            try:
                inspector._run_autocorrelation(session, alpha_id, row_dict)
            except Exception as e:
                logger.error(f"[RefreshCorrelation] Autocorrelation failed for {alpha_id}: {e}")
                add_job_event(job_id, "warning", f"Alpha {alpha_id} correlation calculation failed: {e}")
                
            time.sleep(1.0)
                
        update_job(
            job_id, 
            status="completed", 
            message=f"本地 S 级因子自相关刷新计算已全部完成！共处理了 {total_candidates} 个 S 级因子。", 
            progress_current=100, 
            progress_total=100
        )
    except Exception as e:
        logger.error(f"[RefreshCorrelationJob] Job failed: {e}", exc_info=True)
        raise e
    finally:
        session.close()

from __future__ import annotations

import logging
import json
import requests
from datetime import datetime, timedelta
from typing import Any

from app.storage import connect, get_settings, upsert_alpha, create_job
from app.job_runner import update_job, add_job_event, JobRunner
from app.services.wq_client import login_with_credentials
from consultant_core.machine_lib import get_alphas_full

logger = logging.getLogger(__name__)

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
        
        limit_val = 500
        try:
            limit_val = int(settings.get("wq_sync_limit", "500"))
        except (ValueError, TypeError):
            pass
            
        logger.info(f"[SyncJob] Fetching alphas for region {region} from {start_date.isoformat()} to {end_date.isoformat()} (limit={limit_val})")
        alphas_df = get_alphas_full(
            start_date=start_date,
            end_date=end_date,
            sharpe_th=-10.0,  # 允许拉取低分因子进行本地分类
            region=region,
            usage="submit",
            session=session,
            order="-dateCreated",
            limit=limit_val
        )
        
        session.close()
        
        if alphas_df.empty:
            update_job(job_id, status="completed", message="云端没有查询到最近 30 天的回测因子记录。", progress_current=100, progress_total=100)
            add_job_event(job_id, "info", "No simulated alphas found on WQ platform for the last 30 days.")
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
            
        add_job_event(job_id, "info", f"Fetched {synced_count} alphas; added {new_count} new alphas to database.")
        
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
                
        # A. 最优先：自相关性检测缺失 (prod_corr IS NULL 或 0.0)
        if prod_corr is None or prod_corr == 0.0:
            candidates.append((row_dict, "CORR"))
            continue
            
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
            if work_type == "CORR":
                action_desc = "自相关性补算"
            elif work_type == "CHECK":
                action_desc = "远程 Checks 提交校验"
            elif work_type == "FETCH":
                action_desc = "获取年度 PnL 数据"
                
            msg = f"[{idx}/{total_candidates}] 正在对 {alpha_id} 进行{action_desc}..."
            update_job(job_id, message=msg, progress_current=idx, progress_total=total_candidates)
            add_job_event(job_id, "info", f"Processing {alpha_id}: WorkType={work_type}")
            
            if work_type == "CHECK":
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

from __future__ import annotations
 
import time
import logging
import threading
import json
import re
import requests
import pandas as pd
from datetime import datetime, timezone
 
from ..storage import connect, get_setting, upsert_alpha, add_check_result
from .wq_client import login_with_credentials, retire_wq_alpha
from .check_service import check_alpha_remotely
from .correlation_service import (
    get_alpha_pnl,
    calc_self_corr_local,
    load_correlation_data,
    download_correlation_data
)
from .template_iteration import grade_candidate_result
from .network_monitor import NetworkMonitor
 
logger = logging.getLogger(__name__)
 
class BackgroundInspector:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.thread = None
                cls._instance.stop_event = threading.Event()
            return cls._instance
            
    def start(self) -> None:
        """启动后台自动巡检核查服务"""
        with self._lock:
            if self.thread is None or not self.thread.is_alive():
                self.stop_event.clear()
                self.thread = threading.Thread(target=self._run_loop, daemon=True, name="BackgroundInspector")
                self.thread.start()
                logger.info("BackgroundInspector daemon thread started.")
                
    def stop(self) -> None:
        """停止后台自动巡检核查服务"""
        with self._lock:
            if self.thread is not None:
                self.stop_event.set()
                self.thread.join(timeout=1.0)
                self.thread = None
                logger.info("BackgroundInspector daemon thread stopped.")
                
    def _run_loop(self) -> None:
        # 避开系统启动瞬态，先休眠 15 秒
        slept = 0
        while slept < 15 and not self.stop_event.is_set():
            time.sleep(1)
            slept += 1
            
        while not self.stop_event.is_set():
            try:
                # 检查网络是否连接
                if not NetworkMonitor().is_connected:
                    logger.debug("[BackgroundInspector] Network offline, skipping this cycle.")
                    self._sleep_seconds(10)
                    continue
                    
                username = get_setting("wq_username")
                password = get_setting("wq_password")
                if not username or not password:
                    logger.debug("[BackgroundInspector] WorldQuant credentials missing in Settings, skipping.")
                    self._sleep_seconds(30)
                    continue
                
                # 开始本次巡检处理
                self._process_candidates(username.strip(), password.strip())
                
            except Exception as e:
                logger.error(f"[BackgroundInspector] Error in loop: {e}", exc_info=True)
                
            # 每 30 秒轮询一次，降低对 WQ 平台的请求负荷
            self._sleep_seconds(30)
            
    def _sleep_seconds(self, seconds: int) -> None:
        slept = 0
        while slept < seconds and not self.stop_event.is_set():
            time.sleep(1)
            slept += 1
 
    def _process_candidates(self, username: str, password: str) -> None:
        # 从本地数据库读取所有未标记为 garbage 的因子
        with connect() as conn:
            rows = conn.execute(
                "SELECT * FROM alpha_records WHERE is_garbage = 0 ORDER BY created_at DESC"
            ).fetchall()
            
        if not rows:
            return
            
        retire_candidates = []
        target_alpha = None
        work_type = None  # "CORR", "CHECK", "FETCH"
        
        for row in rows:
            row_dict = dict(row)
            alpha_id = row_dict["alpha_id"]
            prod_corr = row_dict.get("prod_corr")
            status = str(row_dict.get("status") or "").upper()
            payload_str = row_dict.get("payload")
            
            # 解析 payload
            payload = {}
            if payload_str:
                try:
                    payload = json.loads(payload_str)
                except Exception:
                    pass
            
            # 计算当前因子的初步评级
            sharpe = row_dict.get("sharpe")
            fitness = row_dict.get("fitness")
            margin = row_dict.get("margin")
            from .optimization_planner import _extract_yearly_stats
            yearly_stats = _extract_yearly_stats(payload)
            turnover = row_dict.get("turnover") or (yearly_stats[0].get("turnover") if yearly_stats else None)
            self_corr = row_dict.get("ppa_corr") or 0.0
            prod_corr_val = prod_corr or 0.0
            
            # 引入评级算法进行实时诊断
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

            # 0. 垃圾/D级因子发现 -> 收集到批量退休列表中
            if grade == "D":
                retire_candidates.append(row_dict)
                if len(retire_candidates) >= 50:  # 单次批量处理最多 50 个
                    break
                continue
            
            # 如果目前没有处于退休状态的因子，我们才去查其他耗时的单体工作 (CORR, CHECK, FETCH)
            # 这样可以在有 Grade D 堆积时优先全速批量清理垃圾
            if not retire_candidates and not work_type:
                # A. 自相关性检测缺失 (prod_corr IS NULL 或等于 0.0) -> 但必须是已提交/已校验过 (status != 'UNSUBMITTED')
                if (prod_corr is None or prod_corr == 0.0) and status != 'UNSUBMITTED':
                    target_alpha = row_dict
                    work_type = "CORR"
                    
                # B. 评级 C 级及以上，但状态为 UNSUBMITTED，且没有本地 check_results 历史 -> 自动 check submit
                elif grade in {"S", "A", "B", "C"} and status == "UNSUBMITTED":
                    # 查询本地是否已有该因子的 check 结果
                    with connect() as conn:
                        chk_row = conn.execute("SELECT id FROM check_results WHERE alpha_id = ?", (alpha_id,)).fetchone()
                    if not chk_row:
                        target_alpha = row_dict
                        work_type = "CHECK"
                        
                # C. 评级 C 级及以上，但 payload 中缺少年度分解统计 (yearly-stats) 或没有 recordsets_data
                elif grade in {"S", "A", "B", "C"} and not yearly_stats:
                    target_alpha = row_dict
                    work_type = "FETCH"

        # 如果有需要退休的垃圾因子，执行批量退休
        if retire_candidates:
            logger.info(f"[BackgroundInspector] Found {len(retire_candidates)} Grade D alphas. Starting batch retire...")
            session = login_with_credentials(username, password)
            try:
                for idx, alpha in enumerate(retire_candidates, 1):
                    # 检查是否请求终止
                    if self.stop_event.is_set():
                        break
                    aid = alpha["alpha_id"]
                    logger.info(f"[BackgroundInspector] Batch retiring ({idx}/{len(retire_candidates)}): {aid}")
                    self._run_retire(session, aid, alpha)
                    # 适当小休眠防平台限流
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"[BackgroundInspector] Batch retirement error: {e}")
            finally:
                session.close()
            return

        # 如果是其他单体任务
        if target_alpha and work_type:
            alpha_id = target_alpha["alpha_id"]
            logger.info(f"[BackgroundInspector] Auto trigger workflow for alpha {alpha_id}: WorkType={work_type}")
            session = login_with_credentials(username, password)
            try:
                if work_type == "CHECK":
                    self._run_check_submit(session, alpha_id, target_alpha)
                elif work_type == "CORR":
                    self._run_autocorrelation(session, alpha_id, target_alpha)
                elif work_type == "FETCH":
                    self._run_fetch_pnl_details(session, alpha_id, target_alpha)
            except Exception as e:
                logger.error(f"[BackgroundInspector] Workflow failed for {alpha_id}: {e}")
            finally:
                session.close()
 
    def _run_check_submit(self, session: requests.Session, alpha_id: str, row_dict: dict[str, Any]) -> None:
        """自动触发 WQ 平台 Checks 进行核验评估"""
        logger.info(f"[BackgroundInspector] Submitting check request for {alpha_id}...")
        try:
            result, prod_corr, error_msg, check_payload = check_alpha_remotely(session, alpha_id)
            
            # 记录到 check_results 库
            add_check_result(
                alpha_id=alpha_id,
                result=result,
                prod_corr=prod_corr,
                message=error_msg,
                source="background_inspector_check",
                payload=check_payload
            )
            
            # 同时更新 alpha 记录状态
            with connect() as conn:
                conn.execute(
                    "UPDATE alpha_records SET status = ?, prod_corr = COALESCE(?, prod_corr), updated_at = datetime('now') WHERE alpha_id = ?",
                    (f"CHECKED_{result}", prod_corr, alpha_id)
                )
            logger.info(f"[BackgroundInspector] Check validation completed for {alpha_id}: result={result}, prod_corr={prod_corr}")
            
            # 完成后，重新触发一次属性补充和最终定级
            self._run_fetch_pnl_details(session, alpha_id, row_dict)
            
        except Exception as e:
            logger.error(f"[BackgroundInspector] Check submission failed for {alpha_id}: {e}")

    def _run_retire(self, session: requests.Session, alpha_id: str, row_dict: dict[str, Any]) -> None:
        """自动物理退休 Grade D 垃圾因子"""
        logger.info(f"[BackgroundInspector] Automatically retiring Grade D alpha {alpha_id} on WQ platform...")
        try:
            from app.services.wq_client import retire_wq_alpha
            retire_wq_alpha(session, alpha_id)
            
            # 更新本地数据库，将 is_garbage 设为 1
            with connect() as conn:
                conn.execute(
                    "UPDATE alpha_records SET is_garbage = 1, alpha_type = 'D', updated_at = datetime('now') WHERE alpha_id = ?",
                    (alpha_id,)
                )
            logger.info(f"[BackgroundInspector] Retired and marked Grade D alpha {alpha_id} in database.")
        except Exception as e:
            logger.error(f"[BackgroundInspector] Failed to retire Grade D alpha {alpha_id}: {e}")

    def _run_autocorrelation(self, session: requests.Session, alpha_id: str, row_dict: dict[str, Any]) -> None:
        """自动拉取远程 PNL 并在本地做自相关性分析"""
        logger.info(f"[BackgroundInspector] Downloading correlation data & PnL for {alpha_id}...")
        try:
            # 1. 增量更新本地相关性缓存库
            download_correlation_data(session, flag_increment=True)
            all_ids, all_rets = load_correlation_data(tag=None)
            ppa_ids, ppa_rets = load_correlation_data(tag='PPAC')
            
            # 2. 获取该因子的 PnL 收益率明细
            target_pnl_df = get_alpha_pnl(session, alpha_id)
            if target_pnl_df.empty or alpha_id not in target_pnl_df.columns:
                logger.warning(f"[BackgroundInspector] PnL data empty for {alpha_id}, skipping.")
                return
                
            target_pnl_series = target_pnl_df.set_index('Date')[alpha_id]
            alpha_rets_series = target_pnl_series - target_pnl_series.ffill().shift(1)
            
            # 计算 PnL 覆盖率 (非零收益率天数比例)
            total_days = len(alpha_rets_series)
            non_zero_days = (alpha_rets_series != 0).sum()
            pnl_coverage_rate = non_zero_days / total_days if total_days > 0 else 1.0
            
            # 5. 更新 payload 并传递
            payload_str = row_dict.get("payload") or "{}"
            try:
                detail_payload = json.loads(payload_str)
            except Exception:
                detail_payload = {}
            detail_payload["pnl_coverage_rate"] = pnl_coverage_rate
            
            # 3. 本地计算相关性
            region = row_dict.get("region") or "USA"
            prod_corr_val = calc_self_corr_local(alpha_rets_series, all_rets, all_ids, region)
            ppa_corr_val = calc_self_corr_local(alpha_rets_series, ppa_rets, ppa_ids, region)
            
            # 4. 重新进行定档定级
            self._update_alpha_grade_and_status(session, alpha_id, row_dict, prod_corr_val, ppa_corr_val, detail_payload)
            
        except Exception as e:
            logger.error(f"[BackgroundInspector] Autocorrelation calculation failed for {alpha_id}: {e}")
 
    def _run_fetch_pnl_details(self, session: requests.Session, alpha_id: str, row_dict: dict[str, Any]) -> None:
        """自动拉取 WQ yearly-stats 和因子详情，补充本地 payload 以支持 IS/OS 检验"""
        logger.info(f"[BackgroundInspector] Fetching yearly-stats and full details for {alpha_id}...")
        try:
            # 1. 获取 yearly-stats
            yearly_stats = []
            url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats"
            resp = session.get(url, timeout=30)
            if resp.status_code == 200:
                try:
                    stats_json = resp.json()
                    yearly_stats = stats_json.get('records', [])
                except Exception as e:
                    logger.warning(f"[BackgroundInspector] Failed to parse yearly-stats JSON for {alpha_id}: {e}")
                
            # 2. 获取 PNL 每日数据
            pnl_records = []
            url_pnl = f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/pnl"
            resp_pnl = session.get(url_pnl, timeout=30)
            pnl_coverage_rate = 1.0
            if resp_pnl.status_code == 200:
                try:
                    pnl_json = resp_pnl.json()
                    pnl_records = pnl_json.get('records', [])
                    if pnl_records:
                        import pandas as pd
                        pnl_df = pd.DataFrame(pnl_records)
                        if not pnl_df.empty and "pnl" in pnl_df.columns:
                            pnl_series = pnl_df["pnl"]
                            rets = pnl_series - pnl_series.ffill().shift(1)
                            total_days = len(rets)
                            non_zero_days = (rets != 0).sum()
                            pnl_coverage_rate = non_zero_days / total_days if total_days > 0 else 1.0
                except Exception as e:
                    logger.warning(f"[BackgroundInspector] Failed to parse PNL JSON for {alpha_id}: {e}")
                
            # 3. 获取因子明细
            detail_data = {}
            detail_resp = session.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}", timeout=30)
            if detail_resp.status_code == 200:
                try:
                    detail_data = detail_resp.json()
                except Exception as e:
                    logger.warning(f"[BackgroundInspector] Failed to parse detail JSON for {alpha_id}: {e}")
            else:
                # 使用已有 payload fallback
                payload_str = row_dict.get("payload")
                if payload_str:
                    try:
                        detail_data = json.loads(payload_str)
                    except Exception:
                        pass
                        
            # 将年度明细及 PNL 封装进 payload
            if isinstance(detail_data, dict):
                # 统一拼入 recordsets_data 中
                if "recordsets_data" not in detail_data or not isinstance(detail_data["recordsets_data"], dict):
                    detail_data["recordsets_data"] = {}
                if yearly_stats:
                    detail_data["recordsets_data"]["yearly-stats"] = yearly_stats
                if pnl_records:
                    detail_data["recordsets_data"]["pnl"] = pnl_records
                detail_data["pnl_coverage_rate"] = pnl_coverage_rate
            
            # 4. 计算相关性并最终定级
            prod_corr_val = row_dict.get("prod_corr") or 0.0
            ppa_corr_val = row_dict.get("ppa_corr") or 0.0
            
            # 如果相关性也缺失，强制拉取并算一遍相关性
            if prod_corr_val == 0.0:
                try:
                    all_ids, all_rets = load_correlation_data(tag=None)
                    target_pnl_df = get_alpha_pnl(session, alpha_id)
                    if not target_pnl_df.empty and alpha_id in target_pnl_df.columns:
                        target_pnl_series = target_pnl_df.set_index('Date')[alpha_id]
                        alpha_rets_series = target_pnl_series - target_pnl_series.ffill().shift(1)
                        prod_corr_val = calc_self_corr_local(alpha_rets_series, all_rets, all_ids, row_dict.get("region") or "USA")
                except Exception:
                    pass
                    
            self._update_alpha_grade_and_status(session, alpha_id, row_dict, prod_corr_val, ppa_corr_val, detail_data)
            
        except Exception as e:
            logger.error(f"[BackgroundInspector] Fetch PnL details failed for {alpha_id}: {e}")
 
    def _update_alpha_grade_and_status(
        self,
        session: requests.Session,
        alpha_id: str,
        row_dict: dict[str, Any],
        prod_corr: float,
        ppa_corr: float,
        detail_payload: dict[str, Any] | None = None
    ) -> None:
        """运行诊断评级模型，更新数据库评级并将垃圾因子自动从平台物理退休隐藏"""
        if detail_payload is None:
            payload_str = row_dict.get("payload")
            detail_payload = {}
            if payload_str:
                try:
                    detail_payload = json.loads(payload_str)
                except Exception:
                    pass
 
        # 解析指标
        is_metrics = detail_payload.get("is", {})
        if not is_metrics:
            is_metrics = {
                "sharpe": row_dict.get("sharpe"),
                "fitness": row_dict.get("fitness"),
                "margin": row_dict.get("margin"),
                "returns": row_dict.get("returns"),
                "drawdown": row_dict.get("drawdown")
            }
 
        # 读取 check_results 中最新记录判定结果
        with connect() as conn:
            chk_row = conn.execute(
                "SELECT result FROM check_results WHERE alpha_id = ? ORDER BY id DESC LIMIT 1",
                (alpha_id,)
            ).fetchone()
        chk_res = chk_row["result"] if chk_row else ""
 
        # 整理指标并做 S/A/B/C/D 重新定级
        from .optimization_planner import _extract_yearly_stats
        yearly_stats = _extract_yearly_stats(detail_payload)
        turnover = is_metrics.get("turnover") or (yearly_stats[0].get("turnover") if yearly_stats else None)
        
        grading = grade_candidate_result({
            "sharpe": is_metrics.get("sharpe"),
            "fitness": is_metrics.get("fitness"),
            "margin": is_metrics.get("margin"),
            "turnover": turnover,
            "self_corr": ppa_corr,
            "prod_corr": prod_corr,
            "failed_checks": 1 if chk_res == "FAIL" else 0,
            "status": chk_res or row_dict.get("status") or "",
            "payload": detail_payload,
        })
        
        new_grade = grading.get("grade", "C")
        
        # 决定更新入库的数据包
        logger.info(f"[BackgroundInspector] Alpha {alpha_id} re-graded to {new_grade} (prod_corr={prod_corr:.4f}, ppa_corr={ppa_corr:.4f})")
        
        # 物理退休 D 级垃圾因子并设置 is_garbage = 1
        if new_grade == "D":
            try:
                retire_wq_alpha(session, alpha_id)
                logger.info(f"[BackgroundInspector] Successfully retired Grade D alpha {alpha_id} on WQ platform.")
            except Exception as re_err:
                logger.error(f"[BackgroundInspector] Failed to retire Grade D alpha {alpha_id}: {re_err}")
            with connect() as conn:
                conn.execute(
                    "UPDATE alpha_records SET is_garbage = 1, updated_at = datetime('now') WHERE alpha_id = ?",
                    (alpha_id,)
                )
        else:
            with connect() as conn:
                conn.execute(
                    "UPDATE alpha_records SET is_garbage = 0, updated_at = datetime('now') WHERE alpha_id = ?",
                    (alpha_id,)
                )

        # C级及以上因子：若未改名，则自动触发符合平台格式规范的 Scheme A 远程重命名
        target_name = detail_payload.get("name") or row_dict.get("name") or ""
        db_status = f"CHECKED_{chk_res}" if chk_res else row_dict.get("status")

        if new_grade in {"S", "A", "B", "C"} and db_status != "RENAMED":
            from app.services.wq_client import rename_wq_alpha_scheme_a
            region = detail_payload.get("settings", {}).get("region") or row_dict.get("region") or "USA"
            universe = detail_payload.get("settings", {}).get("universe") or row_dict.get("universe") or "TOP3000"
            rename_res = rename_wq_alpha_scheme_a(
                session=session,
                alpha_id=alpha_id,
                grade=new_grade,
                region=region,
                universe=universe,
                self_corr=prod_corr,
                sharpe=is_metrics.get("sharpe"),
                turnover=turnover,
                fitness=is_metrics.get("fitness")
            )
            if rename_res:
                target_name = rename_res
                db_status = "RENAMED"

        # 写入数据库，更新 alpha_type 和相关指标
        upsert_alpha({
            "alpha_id": alpha_id,
            "alpha_type": new_grade,  # 统一在此列存级别字母（S/A/B/C/D）
            "name": target_name,
            "region": detail_payload.get("settings", {}).get("region") or row_dict.get("region") or "USA",
            "universe": detail_payload.get("settings", {}).get("universe") or row_dict.get("universe") or "TOP3000",
            "sharpe": is_metrics.get("sharpe"),
            "fitness": is_metrics.get("fitness"),
            "margin": is_metrics.get("margin"),
            "returns": is_metrics.get("returns"),
            "drawdown": is_metrics.get("drawdown"),
            "prod_corr": prod_corr,
            "ppa_corr": ppa_corr,
            "status": db_status,
            "source": row_dict.get("source") or "background_inspector",
            "payload": detail_payload
        })

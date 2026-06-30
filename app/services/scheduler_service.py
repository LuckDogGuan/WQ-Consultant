import time
import logging
import threading
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from ..storage import get_setting, connect, create_job
from ..job_runner import JobRunner
from .job_params import normalize_optimization_params

logger = logging.getLogger(__name__)

class SchedulerService:
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
        """启动定时任务调度线程"""
        with self._lock:
            if self.thread is None or not self.thread.is_alive():
                self.stop_event.clear()
                self.thread = threading.Thread(target=self._run_scheduler, daemon=True, name="SchedulerService")
                self.thread.start()
                logger.info("SchedulerService background thread started.")
                
    def stop(self) -> None:
        """停止定时任务调度线程"""
        with self._lock:
            if self.thread is not None:
                self.stop_event.set()
                self.thread.join(timeout=1.0)
                self.thread = None
                logger.info("SchedulerService background thread stopped.")
                
    def _run_scheduler(self) -> None:
        # 启动后等待 10 秒以避开系统启动瞬态
        slept = 0
        while slept < 10 and not self.stop_event.is_set():
            time.sleep(1)
            slept += 1
            
        while not self.stop_event.is_set():
            try:
                self._check_and_trigger()
            except Exception as e:
                logger.error(f"Error in scheduler check: {e}")
                
            # 每 3600 秒轮询一次 (1 小时)
            slept = 0
            while slept < 3600 and not self.stop_event.is_set():
                time.sleep(1)
                slept += 1
                
    def _check_and_trigger(self) -> None:
        sh_tz = ZoneInfo("Asia/Shanghai")
        now_sh = datetime.now(sh_tz)

        # 1. 定时自动提交检查任务
        check_enabled = get_setting("check_schedule_enabled", "0") == "1"
        if check_enabled:
            interval_hours = int(get_setting("check_schedule_interval_hours", "24"))
            schedule_hour = int(get_setting("check_schedule_hour", "0"))
            last_run_str = get_setting("check_schedule_last_run", "")
            
            trigger = False
            
            if interval_hours >= 24:
                # 每天在特定小时运行
                current_date_str = now_sh.strftime("%Y-%m-%d")
                if now_sh.hour == schedule_hour:
                    last_run_date = ""
                    if last_run_str:
                        try:
                            last_run_dt = datetime.fromisoformat(last_run_str).astimezone(sh_tz)
                            last_run_date = last_run_dt.strftime("%Y-%m-%d")
                        except Exception:
                            pass
                    if last_run_date != current_date_str:
                        trigger = True
            else:
                # 每隔 N 小时运行一次
                if last_run_str:
                    try:
                        last_run_dt = datetime.fromisoformat(last_run_str)
                        now_utc = datetime.now(timezone.utc)
                        elapsed = (now_utc - last_run_dt).total_seconds() / 3600.0
                        if elapsed >= interval_hours:
                            trigger = True
                    except Exception:
                        trigger = True
                else:
                    trigger = True
                    
            if trigger:
                logger.info("Scheduler triggering auto check submission job...")
                now_iso = datetime.now(timezone.utc).isoformat()
                
                # 更新上次执行时间
                with connect() as conn:
                    conn.execute(
                        "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES ('check_schedule_last_run', ?, datetime('now'))",
                        (now_iso,)
                    )
                    
                # 发起任务
                lookback = int(get_setting("check_lookback_days", "60"))
                max_candidates = int(get_setting("check_max_candidates", "4000"))
                params = {"manual_ids": []}
                job_id = create_job(
                    "check_submission",
                    f"定时自动提交检查 (最近 {lookback} 天, 前 {max_candidates} 个)",
                    params
                )
                JobRunner().start_job(job_id, "check_submission", params)

        # 2. 定时自动相关性诊断任务
        corr_enabled = get_setting("corr_schedule_enabled", "0") == "1"
        if corr_enabled:
            corr_hour = int(get_setting("corr_schedule_hour", "11"))
            corr_last_run_str = get_setting("corr_schedule_last_run", "")
            
            corr_trigger = False
            current_date_str = now_sh.strftime("%Y-%m-%d")
            
            # 每天在特定小时运行
            if now_sh.hour == corr_hour:
                last_run_date = ""
                if corr_last_run_str:
                    try:
                        last_run_dt = datetime.fromisoformat(corr_last_run_str).astimezone(sh_tz)
                        last_run_date = last_run_dt.strftime("%Y-%m-%d")
                    except Exception:
                        pass
                if last_run_date != current_date_str:
                    corr_trigger = True
                    
            if corr_trigger:
                logger.info("Scheduler triggering auto correlation job...")
                now_iso = datetime.now(timezone.utc).isoformat()
                
                # 更新上次执行时间
                with connect() as conn:
                    conn.execute(
                        "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES ('corr_schedule_last_run', ?, datetime('now'))",
                        (now_iso,)
                    )
                    
                # 发起相关性任务
                lookback = int(get_setting("corr_schedule_lookback_days", "7"))
                max_candidates = int(get_setting("corr_schedule_max_candidates", "4000"))
                auto_rename_val = get_setting("auto_rename", "1") == "1"
                
                params = {
                    "lookback_days": lookback,
                    "limit": str(max_candidates) if max_candidates > 0 else "",
                    "auto_rename": auto_rename_val
                }
                job_id = create_job(
                    "correlation",
                    f"定时自动相关性检测 (最近 {lookback} 天, 限额 {max_candidates} 个)",
                    params
                )
                JobRunner().start_job(job_id, "correlation", params)

        # 3. 定时自动 Alpha 优化任务
        opt_enabled = get_setting("optimization_schedule_enabled", "0") == "1"
        if opt_enabled:
            opt_hour = int(get_setting("optimization_schedule_hour", "1"))
            opt_last_run_str = get_setting("optimization_schedule_last_run", "")

            opt_trigger = False
            current_date_str = now_sh.strftime("%Y-%m-%d")
            if now_sh.hour == opt_hour:
                last_run_date = ""
                if opt_last_run_str:
                    try:
                        last_run_dt = datetime.fromisoformat(opt_last_run_str).astimezone(sh_tz)
                        last_run_date = last_run_dt.strftime("%Y-%m-%d")
                    except Exception:
                        pass
                if last_run_date != current_date_str:
                    opt_trigger = True

            if opt_trigger:
                logger.info("Scheduler triggering auto optimization job...")
                now_iso = datetime.now(timezone.utc).isoformat()
                with connect() as conn:
                    conn.execute(
                        "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES ('optimization_schedule_last_run', ?, datetime('now'))",
                        (now_iso,),
                    )

                params = normalize_optimization_params({
                    "source_mode": get_setting("optimization_source_mode", "recent"),
                    "recent_days": int(get_setting("optimization_recent_days", "14")),
                    "candidate_limit": int(get_setting("optimization_candidate_limit", "20")),
                    "children_per_request": int(get_setting("optimization_children_per_request", "1")),
                })
                job_id = create_job(
                    "optimization_run",
                    f"定时 Alpha 优化任务 (最近 {params['recent_days']} 天，最多 {params['candidate_limit']} 个)",
                    params,
                )
                JobRunner().start_job(job_id, "optimization_run", params)

        cleanup_enabled = get_setting("submitted_cleanup_schedule_enabled", "1") == "1"
        if cleanup_enabled:
            cleanup_hour = int(get_setting("submitted_cleanup_schedule_hour", "0"))
            cleanup_last_run_str = get_setting("submitted_cleanup_schedule_last_run", "")
            cleanup_trigger = False
            current_date_str = now_sh.strftime("%Y-%m-%d")
            if now_sh.hour == cleanup_hour:
                last_run_date = ""
                if cleanup_last_run_str:
                    try:
                        last_run_dt = datetime.fromisoformat(cleanup_last_run_str).astimezone(sh_tz)
                        last_run_date = last_run_dt.strftime("%Y-%m-%d")
                    except Exception:
                        pass
                if last_run_date != current_date_str:
                    cleanup_trigger = True

            if cleanup_trigger:
                logger.info("Scheduler triggering submitted alpha cleanup job...")
                now_iso = datetime.now(timezone.utc).isoformat()
                with connect() as conn:
                    conn.execute(
                        "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES ('submitted_cleanup_schedule_last_run', ?, datetime('now'))",
                        (now_iso,),
                    )
                params = {"schema_version": 1, "limit": 100, "max_pages": 20}
                job_id = create_job("submitted_cleanup", "每日 submitted Alpha 本地候选清理", params)
                JobRunner().start_job(job_id, "submitted_cleanup", params)

        # 5. 定时自动本地因子同步与自相关性计算任务
        local_sync_enabled = get_setting("local_sync_schedule_enabled", "1") == "1"
        if local_sync_enabled:
            local_sync_hour = int(get_setting("local_sync_schedule_hour", "0"))
            local_sync_last_run_str = get_setting("local_sync_schedule_last_run", "")
            
            local_sync_trigger = False
            current_date_str = now_sh.strftime("%Y-%m-%d")
            if now_sh.hour == local_sync_hour:
                last_run_date = ""
                if local_sync_last_run_str:
                    try:
                        last_run_dt = datetime.fromisoformat(local_sync_last_run_str).astimezone(sh_tz)
                        last_run_date = last_run_dt.strftime("%Y-%m-%d")
                    except Exception:
                        pass
                if last_run_date != current_date_str:
                    local_sync_trigger = True
                    
            if local_sync_trigger:
                logger.info("Scheduler triggering auto local sync and correlation job...")
                now_iso = datetime.now(timezone.utc).isoformat()
                with connect() as conn:
                    conn.execute(
                        "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES ('local_sync_schedule_last_run', ?, datetime('now'))",
                        (now_iso,)
                    )
                job_id = create_job("sync_local_alphas", "定时本地因子自相关同步计算", {})
                JobRunner().start_job(job_id, "sync_local_alphas", {})

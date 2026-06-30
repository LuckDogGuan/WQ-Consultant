from __future__ import annotations

import logging
import sys
import threading
import traceback
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .paths import LOG_DIR
from .storage import update_job, add_job_event, add_error, connect

logger = logging.getLogger(__name__)


class JobPausedException(Exception):
    """当任务被用户主动暂停时抛出此异常"""
    pass


class ThreadLocalStream:
    """线程本地流，用于将不同后台任务的 stdout/stderr 重定向到各自的日志文件"""
    def __init__(self, original_stream):
        self.original_stream = original_stream
        self.local = threading.local()

    def write(self, data: str) -> int:
        f = getattr(self.local, "file", None)
        if f:
            try:
                need_timestamp = getattr(self.local, "need_timestamp", True)
                from datetime import datetime
                parts = []
                lines = data.splitlines(keepends=True)
                for line in lines:
                    if need_timestamp and line.strip() != "":
                        ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
                        parts.append(ts + line)
                    else:
                        parts.append(line)
                    need_timestamp = line.endswith("\n")
                self.local.need_timestamp = need_timestamp
                new_data = "".join(parts)
                f.write(new_data)
                f.flush()
                return len(data)
            except Exception:
                pass
        return self.original_stream.write(data)

    def flush(self) -> None:
        f = getattr(self.local, "file", None)
        if f:
            try:
                f.flush()
            except Exception:
                pass
        self.original_stream.flush()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.original_stream, name)


# 实例化并重定向系统标准流
original_stdout = sys.stdout
original_stderr = sys.stderr
redirected_stdout = ThreadLocalStream(sys.stdout)
redirected_stderr = ThreadLocalStream(sys.stderr)


def patch_streams() -> None:
    """替换 stdout 和 stderr 为线程本地流"""
    sys.stdout = redirected_stdout
    sys.stderr = redirected_stderr


@contextmanager
def redirect_to_job_log(log_path: Path):
    """上下文管理器：重定向当前线程的标准输出与错误输出到任务日志文件"""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    f = open(log_path, "a", encoding="utf-8", errors="replace")
    redirected_stdout.local.file = f
    redirected_stderr.local.file = f
    try:
        yield f
    finally:
        redirected_stdout.local.file = None
        redirected_stderr.local.file = None
        f.close()


class JobRunner:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.active_jobs = {}  # job_id -> threading.Thread
                cls._instance.pause_flags = set()  # set of job_id
            return cls._instance

    def init_runner(self) -> None:
        """初始化任务管理器，重置未完成的 Job 状态"""
        patch_streams()
        self.reset_running_jobs()

    def reset_running_jobs(self) -> None:
        """启动时重置所有未完结的任务状态为 paused，避免断电重启后网络并发冲突"""
        logger.info("Initializing JobRunner: Scanning and resetting unfinished jobs...")
        with connect() as conn:
            # 扫描处于 running, waiting_limit, waiting_time_window, reconnecting 状态的任务
            conn.execute(
                """
                UPDATE jobs 
                SET status = 'paused', message = 'Service restarted. Job paused.', updated_at = ?
                WHERE status IN ('running', 'waiting_limit', 'waiting_time_window', 'reconnecting')
                """,
                (conn.execute("SELECT datetime('now')").fetchone()[0],)
            )

    def start_job(self, job_id: int, kind: str, params: dict[str, Any]) -> None:
        """开始或恢复运行一个任务"""
        with self._lock:
            if job_id in self.active_jobs:
                if job_id in self.pause_flags:
                    self.pause_flags.discard(job_id)
                    update_job(job_id, status="running", message="Task resumed, running...")
                    add_job_event(job_id, "info", "User resumed task before background thread exited.")
                    logger.info(f"Resumed Job {job_id} before thread exited.")
                    return
                else:
                    logger.warning(f"Job {job_id} is already running.")
                    return
            
            with connect() as conn:
                row = conn.execute("SELECT status FROM jobs WHERE id = ?", (job_id,)).fetchone()
                if row and row["status"] == "completed":
                    # Delete job log
                    log_path = LOG_DIR / f"job_{job_id}.log"
                    if log_path.exists():
                        try:
                            log_path.unlink()
                        except Exception as e:
                            logger.error(f"Failed to delete completed log: {e}")
                    
                    # Delete stage progress files
                    for p in LOG_DIR.glob(f"*_progress_{job_id}_*.jsonl"):
                        try:
                            p.unlink()
                        except Exception as e:
                            logger.error(f"Failed to delete stage progress file {p}: {e}")
                    
                    # Reset progress in DB
                    conn.execute("UPDATE jobs SET progress_current = 0, progress_total = 100 WHERE id = ?", (job_id,))
                    logger.info(f"Cleared previous logs and progress files for completed Job {job_id} to run fresh.")
            
            self.pause_flags.discard(job_id)
            t = threading.Thread(
                target=self._run_job_worker,
                args=(job_id, kind, params),
                name=f"Job-{job_id}",
                daemon=True
            )
            self.active_jobs[job_id] = t
            t.start()

    def pause_job(self, job_id: int) -> None:
        """请求暂停一个任务"""
        with self._lock:
            if job_id in self.active_jobs:
                self.pause_flags.add(job_id)
                update_job(job_id, status="paused", message="Pausing task...")
                add_job_event(job_id, "info", "User requested job pause.")
                logger.info(f"Requested pause for Job {job_id}")

    def is_paused(self, job_id: int) -> bool:
        """检查任务是否已被请求暂停。由具体工作业务层循环调用以响应暂停请求。"""
        return job_id in self.pause_flags

    def check_paused(self, job_id: int) -> None:
        """如果收到暂停请求，则直接抛出 JobPausedException"""
        if self.is_paused(job_id):
            raise JobPausedException("Job paused by user.")

    def _run_job_worker(self, job_id: int, kind: str, params: dict[str, Any]) -> None:
        """任务线程包装器"""
        log_path = LOG_DIR / f"job_{job_id}.log"
        
        # 线程开始执行，更新状态为 running
        update_job(job_id, status="running", message="Task is running...")
        add_job_event(job_id, "info", f"Background worker for job {job_id} ({kind}) started.")
        
        try:
            with redirect_to_job_log(log_path):
                # 动态导入各服务模块以避免循环引用
                if kind == "catalog_refresh":
                    from .services.catalog_service import run_catalog_refresh
                    run_catalog_refresh(job_id)
                elif kind == "backtest":
                    from .services.simulation_service import run_backtest_job
                    run_backtest_job(job_id, params)
                elif kind == "correlation":
                    from .services.correlation_service import run_correlation_job
                    run_correlation_job(job_id, params)
                elif kind == "check_submission":
                    from .services.check_service import run_check_job
                    run_check_job(job_id, params)
                elif kind == "alpha_submit":
                    from .services.submit_service import run_submit_job
                    run_submit_job(job_id, params)
                elif kind == "optimization_run":
                    from .services.optimization_run_service import run_optimization_job
                    run_optimization_job(job_id, params)
                elif kind == "template_iteration":
                    from .services.template_iteration import run_template_iteration_job
                    run_template_iteration_job(job_id, params)
                elif kind == "submitted_cleanup":
                    from .services.maintenance_service import run_submitted_cleanup_job
                    run_submitted_cleanup_job(job_id, params)
                elif kind == "reference_fetch":
                    from .services.reference_service import run_reference_fetch_job
                    run_reference_fetch_job(job_id, params)
                elif kind == "sync_alphas":
                    from .services.sync_service import run_sync_alphas_job
                    run_sync_alphas_job(job_id, params)
                elif kind == "alpha_inspection":
                    from .services.sync_service import run_alpha_inspection_job
                    run_alpha_inspection_job(job_id, params)
                else:
                    raise ValueError(f"Unknown job kind: {kind}")
            
            # 执行成功完毕后状态变更
            with self._lock:
                if job_id in self.pause_flags:
                    self.pause_flags.discard(job_id)
                    with connect() as conn:
                        row = conn.execute("SELECT status FROM jobs WHERE id = ?", (job_id,)).fetchone()
                        is_waiting_network = row and row["status"] == "waiting_network"
                    if is_waiting_network:
                        add_job_event(job_id, "info", "任务因网络断开被成功挂起。")
                    else:
                        update_job(job_id, status="paused", message="任务已暂停。")
                        add_job_event(job_id, "info", "Job execution suspended successfully.")
                else:
                    update_job(job_id, status="completed", message="Job completed successfully.", progress_current=100, progress_total=100)
                    add_job_event(job_id, "info", "Job execution finished.")
        
        except JobPausedException:
            # 捕获主动暂停异常
            with self._lock:
                self.pause_flags.discard(job_id)
                with connect() as conn:
                    row = conn.execute("SELECT status FROM jobs WHERE id = ?", (job_id,)).fetchone()
                    is_waiting_network = row and row["status"] == "waiting_network"
                if is_waiting_network:
                    add_job_event(job_id, "info", "任务已因网络断开而挂起。")
                else:
                    update_job(job_id, status="paused", message="Job paused.")
                    add_job_event(job_id, "info", "Job paused by user request.")
                
        except Exception as e:
            # 运行中出错
            err_msg = str(e)
            tb = traceback.format_exc()
            update_job(job_id, status="failed", message=err_msg)
            add_job_event(job_id, "error", f"Job execution failed: {err_msg}", {"traceback": tb})
            add_error(kind, f"Job {job_id} failed: {err_msg}", {"traceback": tb})
            
            # 将错误输出到当前 Job 日志
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"\n[FATAL ERROR] {err_msg}\n{tb}\n")
            except Exception:
                pass
                
        finally:
            with self._lock:
                self.active_jobs.pop(job_id, None)
            import gc
            gc.collect()

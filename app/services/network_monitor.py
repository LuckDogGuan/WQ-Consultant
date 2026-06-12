import time
import logging
import threading
import urllib.request
from pathlib import Path
from typing import Any

from ..storage import connect, update_job, add_job_event, utc_now, get_setting
from ..job_runner import JobRunner

logger = logging.getLogger(__name__)

class NetworkMonitor:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.is_connected = True
                cls._instance.thread = None
                cls._instance.stop_event = threading.Event()
            return cls._instance
            
    def start(self) -> None:
        """启动网络监视器线程"""
        with self._lock:
            if self.thread is None or not self.thread.is_alive():
                self.stop_event.clear()
                self.thread = threading.Thread(target=self._run_monitor, daemon=True, name="NetworkMonitor")
                self.thread.start()
                logger.info("NetworkMonitor background thread started.")
                
    def stop(self) -> None:
        """停止网络监视器线程"""
        with self._lock:
            if self.thread is not None:
                self.stop_event.set()
                self.thread.join(timeout=1.0)
                self.thread = None
                logger.info("NetworkMonitor background thread stopped.")
                
    def _run_monitor(self) -> None:
        runner = JobRunner()
        
        while not self.stop_event.is_set():
            # 检测是否能访问 WorldQuant Brain API
            connected = False
            try:
                # 3 秒超时轻量请求
                urllib.request.urlopen("https://api.worldquantbrain.com", timeout=3.0)
                connected = True
            except Exception:
                connected = False
                
            if connected != self.is_connected:
                self.is_connected = connected
                if not connected:
                    logger.warning("Network connection lost! Suspending active jobs.")
                    # 1. 网络断开：暂停所有活动任务并设为 waiting_network 状态
                    with connect() as conn:
                        running_jobs = conn.execute(
                            "SELECT id, kind, params FROM jobs WHERE status IN ('running', 'waiting_limit', 'waiting_time_window', 'reconnecting')"
                        ).fetchall()
                        
                        for job in running_jobs:
                            job_id = job["id"]
                            # 请求暂停以停止工作线程
                            runner.pause_job(job_id)
                            
                            # 更新任务状态为 waiting_network，并记录事件
                            conn.execute(
                                "UPDATE jobs SET status = 'waiting_network', message = '网络已断开，等待自动重连恢复...', updated_at = ? WHERE id = ?",
                                (utc_now(), job_id)
                            )
                            conn.execute(
                                "INSERT INTO job_events (job_id, level, message, payload, created_at) VALUES (?, 'warning', '网络已断开，任务挂起等待重连。', '{}', ?)",
                                (job_id, utc_now())
                            )
                else:
                    logger.info("Network connection restored! Resuming waiting tasks.")
                    # 2. 网络恢复：重新启动之前被挂起为 waiting_network 的任务
                    with connect() as conn:
                        waiting_jobs = conn.execute(
                            "SELECT id, kind, params FROM jobs WHERE status = 'waiting_network'"
                        ).fetchall()
                        
                        for job in waiting_jobs:
                            job_id = job["id"]
                            import json
                            try:
                                params = json.loads(job["params"])
                            except Exception:
                                params = {}
                                
                            # 重新拉起任务线程
                            runner.start_job(job_id, job["kind"], params)
                            
                            # 记录事件并恢复状态
                            conn.execute(
                                "INSERT INTO job_events (job_id, level, message, payload, created_at) VALUES (?, 'info', '网络已恢复，自动重启任务。', '{}', ?)",
                                (job_id, utc_now())
                            )
                            
            # 每 10 秒进行一次扫描检测
            slept = 0
            while slept < 10 and not self.stop_event.is_set():
                time.sleep(1)
                slept += 1

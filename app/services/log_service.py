from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Generator

from ..paths import LOG_DIR

logger = logging.getLogger(__name__)

def get_job_log_path(job_id: int) -> Path:
    """获取指定 Job 的日志文件路径"""
    return LOG_DIR / f"job_{job_id}.log"

def get_gui_log_path() -> Path:
    """获取 GUI 的系统日志文件路径"""
    return LOG_DIR / "gui.log"

def filter_gui_log(start_time: str | None = None, end_time: str | None = None) -> Generator[str, None, None]:
    """
    根据开始和结束时间过滤 system gui.log 文件。
    start_time, end_time 的格式为 'YYYY-MM-DD HH:MM:SS' 或 'YYYY-MM-DDTHH:MM'。
    """
    log_file = get_gui_log_path()
    if not log_file.exists():
        logger.warning(f"gui.log file not found at {log_file}")
        return

    # 规范化输入的时间格式
    def format_datetime_input(val: str, default_suffix: str) -> str:
        if not val:
            return ""
        val = val.replace("T", " ")
        if len(val) == 16:  # YYYY-MM-DD HH:MM
            val += default_suffix
        return val

    start_str = format_datetime_input(start_time, ":00")
    end_str = format_datetime_input(end_time, ":59")

    timestamp_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")
    keep = True

    with open(log_file, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            match = timestamp_pattern.match(line)
            if match:
                timestamp_part = match.group(1)
                is_after_start = True
                is_before_end = True
                if start_str:
                    is_after_start = (timestamp_part >= start_str)
                if end_str:
                    is_before_end = (timestamp_part <= end_str)
                keep = is_after_start and is_before_end
            if keep:
                yield line

from __future__ import annotations

import logging

from .paths import LOG_DIR, ensure_dirs


class PollingLogFilter(logging.Filter):
    """过滤掉高频的 API 轮询日志，防止控制台日志刷屏"""
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        if "/api/network_status" in msg or "/api/jobs" in msg:
            return False
        return True


def configure_logging() -> None:
    ensure_dirs()
    log_path = LOG_DIR / "gui.log"
    from logging.handlers import RotatingFileHandler
    log_handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            log_handler,
            logging.StreamHandler(),
        ],
    )
    
    # 注册过滤器，屏蔽高频轮询的访问日志
    logging.getLogger("uvicorn.access").addFilter(PollingLogFilter())


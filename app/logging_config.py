from __future__ import annotations

import logging

from .paths import LOG_DIR, ensure_dirs


def configure_logging() -> None:
    ensure_dirs()
    log_path = LOG_DIR / "gui.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


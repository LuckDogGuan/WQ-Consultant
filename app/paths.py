from __future__ import annotations

from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = APP_ROOT.parent
SRC_ROOT = PROJECT_ROOT / "src"
DATA_DIR = APP_ROOT / "data"
CATALOG_DIR = DATA_DIR / "catalog"
CORRELATION_DIR = DATA_DIR / "correlation"
LOG_DIR = APP_ROOT / "logs"
import os
DB_PATH = DATA_DIR / os.environ.get("WQ_DB_NAME", "gui.db")
GUI_VERSION = "v0.1"


def ensure_dirs() -> None:
    for path in (DATA_DIR, CATALOG_DIR, CORRELATION_DIR, LOG_DIR):
        path.mkdir(parents=True, exist_ok=True)


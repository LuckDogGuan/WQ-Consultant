from __future__ import annotations

import logging
import sys
import subprocess
from pathlib import Path
from typing import Any

from ..storage import update_job, add_job_event

logger = logging.getLogger(__name__)


def run_reference_fetch_job(job_id: int, params: dict[str, Any]) -> None:
    region = params.get("region", "USA")
    delay = params.get("delay", "1")
    universe = params.get("universe", "TOP3000")
    
    update_job(job_id, progress_current=10, progress_total=100, message=f"Starting PPA data fetch for {region}/{universe} (delay={delay})...")
    add_job_event(job_id, "info", f"Started reference fetch task for {region}/{universe} (delay={delay})", params)
    
    script_path = Path("reference/code/fetch_ppa_datasets.py").resolve()
    if not script_path.exists():
        raise FileNotFoundError(f"Crawl script not found at {script_path}")
        
    cmd = [
        sys.executable,
        str(script_path),
        "--region", str(region),
        "--delay", str(delay),
        "--universe", str(universe)
    ]
    
    update_job(job_id, progress_current=20, progress_total=100, message="Fetching theme datasets & fields...")
    
    try:
        # Run subprocess. It will write output to sys.stdout and sys.stderr.
        # Since JobRunner redirects standard output/error to a file for this thread,
        # we can pass stdout=None, stderr=None to inherit them, which redirects them to the job's log file.
        subprocess.run(cmd, check=True)
        
        update_job(job_id, progress_current=100, progress_total=100, message="PPA data fetch completed successfully.")
        add_job_event(job_id, "info", "Reference fetch task completed successfully.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Fetch script failed with exit code {e.returncode}")

from __future__ import annotations

import logging
from typing import Any

from ..storage import add_job_event, get_setting, update_job
from ..job_runner import JobRunner

logger = logging.getLogger(__name__)

DAILY_INSPECTION_PRIORITY = 0


def build_daily_inspection_params(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {
        "source": "daily_inspection",
        "stages": ["correlation", "check_submission"],
        "lookback_days": int(get_setting("daily_inspection_lookback_days", get_setting("corr_schedule_lookback_days", "7"))),
        "max_candidates": int(get_setting("daily_inspection_max_candidates", get_setting("corr_schedule_max_candidates", "4000"))),
        "auto_rename": get_setting("auto_rename", "1") == "1",
        "auto_submit": get_setting("daily_inspection_auto_submit", "0") == "1",
    }
    if params["auto_submit"]:
        params["stages"].append("alpha_submit")
    if overrides:
        params.update(overrides)
    return params


def run_daily_inspection_job(job_id: int, params: dict[str, Any]) -> None:
    runner = JobRunner()
    merged = build_daily_inspection_params(params)
    stages = list(merged.get("stages") or ["correlation", "check_submission"])

    update_job(job_id, progress_current=0, progress_total=len(stages), message="Daily factor inspection started.")
    add_job_event(job_id, "info", "Daily factor inspection started.", merged)

    stage_index = 0
    if "correlation" in stages:
        runner.check_paused(job_id)
        update_job(job_id, progress_current=stage_index, progress_total=len(stages), message="Stage 1: correlation inspection.")
        from .correlation_service import run_correlation_job

        run_correlation_job(
            job_id,
            {
                "lookback_days": merged["lookback_days"],
                "limit": str(merged["max_candidates"]),
                "auto_rename": merged["auto_rename"],
            },
        )
        stage_index += 1
        update_job(job_id, progress_current=stage_index, progress_total=len(stages), message="Correlation inspection finished.")

    if "check_submission" in stages:
        runner.check_paused(job_id)
        update_job(job_id, progress_current=stage_index, progress_total=len(stages), message="Stage 2: check submission.")
        from .check_service import run_check_job

        run_check_job(job_id, {"manual_ids": []})
        stage_index += 1
        update_job(job_id, progress_current=stage_index, progress_total=len(stages), message="Check submission finished.")

    if "alpha_submit" in stages:
        runner.check_paused(job_id)
        update_job(job_id, progress_current=stage_index, progress_total=len(stages), message="Stage 3: alpha submit.")
        from .submit_service import run_submit_job

        run_submit_job(
            job_id,
            {
                "source_mode": "local_pass",
                "limit": merged["max_candidates"],
                "max_cycles": 1,
            },
        )
        stage_index += 1
        update_job(job_id, progress_current=stage_index, progress_total=len(stages), message="Alpha submit finished.")

    add_job_event(job_id, "info", "Daily factor inspection completed.", {"stages": stages})

from __future__ import annotations

import json
import logging
import re
from typing import Any

from ..storage import add_job_event, connect, get_setting, update_job, upsert_alpha
from ..job_runner import JobRunner
from .wq_client import login_with_credentials

logger = logging.getLogger(__name__)


def parse_alpha_ids(text: str | list[str] | tuple[str, ...] | None) -> list[str]:
    if text is None:
        return []
    if isinstance(text, (list, tuple)):
        raw_items = [str(item) for item in text]
    else:
        raw_items = re.split(r"[\s,;]+", str(text))

    ids: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        alpha_id = item.strip()
        if not alpha_id or alpha_id in seen:
            continue
        seen.add(alpha_id)
        ids.append(alpha_id)
    return ids


def list_local_submit_candidates(limit: int = 200) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT
                a.alpha_id,
                a.name,
                a.alpha_type,
                a.sharpe,
                a.fitness,
                a.prod_corr,
                a.ppa_corr,
                a.payload,
                MAX(c.created_at) AS checked_at,
                CASE WHEN a.alpha_type IN ('PPA', 'RA', 'ATOM') THEN 0 ELSE 1 END AS tier_rank
            FROM alpha_records a
            INNER JOIN check_results c ON c.alpha_id = a.alpha_id
            WHERE c.result = 'PASS'
              AND UPPER(COALESCE(a.status, '')) NOT IN ('SUBMITTED', 'SUBMIT_SUCCESS')
              AND UPPER(COALESCE(a.status, '')) NOT LIKE 'SUBMITTED_%'
            GROUP BY a.alpha_id
            ORDER BY tier_rank ASC, checked_at DESC, a.sharpe DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()

    candidates: list[dict[str, Any]] = []
    for row in rows:
        payload = {}
        if row["payload"]:
            try:
                payload = json.loads(row["payload"])
            except Exception:
                payload = {}
        candidates.append(
            {
                "alpha_id": row["alpha_id"],
                "target_name": payload.get("target_name") or row["name"] or "",
                "source": "alpha_records",
                "candidate_tier": "priority" if row["alpha_type"] in {"PPA", "RA", "ATOM"} else "checked_pass",
                "alpha_type": row["alpha_type"],
                "sharpe": row["sharpe"],
                "fitness": row["fitness"],
                "prod_corr": row["prod_corr"],
                "ppa_corr": row["ppa_corr"],
            }
        )
    return candidates


def fetch_wq_submit_candidates(session: Any, limit: int) -> list[dict[str, Any]]:
    from consultant_core.machine_lib import get_alphas_full, recent_alpha_date_range

    lookback = int(get_setting("submit_lookback_days", "30"))
    region = get_setting("region", "USA")
    universe = get_setting("universe", "TOP3000")
    timezone_name = get_setting("alpha_date_timezone", "Asia/Shanghai")
    start_date, end_date = recent_alpha_date_range(lookback, timezone_name=timezone_name)
    alpha_df = get_alphas_full(
        start_date=start_date,
        end_date=end_date,
        sharpe_th=float(get_setting("submit_sharpe", "1.58")),
        fitness_th=float(get_setting("submit_fitness", "1.0")),
        region=region,
        limit=limit,
        usage="submit",
        session=session,
        min_instrument_count=101,
        order="-dateCreated",
    )
    if alpha_df.empty:
        return []
    if "universe" in alpha_df.columns:
        alpha_df = alpha_df[alpha_df["universe"] == universe]
    return [
        {
            "alpha_id": str(row["alpha_id"]),
            "target_name": row.get("name") or "",
            "source": "wq_submit_list",
            "alpha_type": row.get("status") or "",
        }
        for _, row in alpha_df.iterrows()
    ]


def build_submit_records(
    source_mode: str = "local_pass",
    manual_ids: str | list[str] | None = None,
    limit: int | None = None,
    session: Any | None = None,
) -> list[dict[str, Any]]:
    limit = int(limit or get_setting("submit_alpha_num", "200"))
    records: list[dict[str, Any]] = []

    if source_mode in {"manual", "mixed"}:
        records.extend({"alpha_id": alpha_id, "source": "manual", "target_name": ""} for alpha_id in parse_alpha_ids(manual_ids))
    if source_mode in {"local_pass", "mixed"}:
        records.extend(list_local_submit_candidates(limit=limit))
    if source_mode == "wq_submit_list":
        if session is None:
            raise ValueError("session is required for wq_submit_list source mode")
        records.extend(fetch_wq_submit_candidates(session, limit=limit))

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for record in records:
        alpha_id = str(record.get("alpha_id") or "").strip()
        if not alpha_id or alpha_id in seen:
            continue
        seen.add(alpha_id)
        deduped.append({**record, "alpha_id": alpha_id})
        if len(deduped) >= limit:
            break
    return deduped


def run_submit_job(job_id: int, params: dict[str, Any]) -> None:
    runner = JobRunner()
    source_mode = str(params.get("source_mode") or "local_pass")
    limit = int(params.get("limit") or get_setting("submit_alpha_num", "200"))
    dry_run = bool(params.get("dry_run", False))

    username = get_setting("wq_username")
    password = get_setting("wq_password")
    if not username or not password:
        raise ValueError("Missing WorldQuant credentials in Settings.")

    update_job(job_id, message="Building alpha submit queue...")
    session = login_with_credentials(username, password)
    try:
        records = build_submit_records(
            source_mode=source_mode,
            manual_ids=params.get("manual_ids") or [],
            limit=limit,
            session=session,
        )
        if not records:
            update_job(job_id, message="No submit candidates found.", progress_current=100, progress_total=100)
            add_job_event(job_id, "info", "No submit candidates found.", {"source_mode": source_mode})
            return

        runner.check_paused(job_id)
        update_job(job_id, progress_current=0, progress_total=len(records), message=f"Submitting {len(records)} alpha candidates...")
        add_job_event(job_id, "info", "Alpha submit queue constructed.", {"count": len(records), "source_mode": source_mode})

        from consultant_core.machine_lib import submit_alpha_queue_until_limit

        summary = submit_alpha_queue_until_limit(
            records,
            session=session,
            daily_limit=int(get_setting("submit_daily_regular_limit", "4")),
            poll_seconds=int(float(get_setting("poll_minutes", "20")) * 60),
            blocked_start=get_setting("blocked_start_cn", "00:00"),
            blocked_end=get_setting("blocked_end_cn", "00:00"),
            timezone_name=get_setting("alpha_date_timezone", "Asia/Shanghai"),
            max_cycles=int(params.get("max_cycles") or 1),
            dry_run=dry_run,
            submit_max_retries=int(params.get("submit_max_retries") or 2),
            submit_retry_sleep=int(params.get("submit_retry_sleep") or 60),
            pause_between_submits=float(params.get("pause_between_submits") or 0),
        )

        submitted = summary.get("submitted", [])
        for alpha_id in submitted:
            upsert_alpha(
                {
                    "alpha_id": alpha_id,
                    "status": "SUBMITTED",
                    "source": "alpha_submit",
                    "payload": {"submit_summary": summary},
                }
            )

        msg = f"Submit job finished. Submitted: {len(submitted)}, failed: {len(summary.get('failed', []))}, pending: {summary.get('pending_count', 0)}."
        update_job(job_id, progress_current=len(records), progress_total=len(records), message=msg)
        add_job_event(job_id, "info", msg, summary)
    finally:
        session.close()

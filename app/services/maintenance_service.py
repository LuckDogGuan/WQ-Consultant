from __future__ import annotations

import json
import logging
from typing import Any, Iterable

from ..storage import add_job_event, connect, get_setting, update_job, utc_now
from .wq_client import login_with_credentials

logger = logging.getLogger(__name__)


def cleanup_submitted_alpha_inputs(alpha_ids: Iterable[str]) -> dict[str, int]:
    submitted_ids = sorted({str(alpha_id).strip() for alpha_id in alpha_ids if str(alpha_id).strip()})
    summary = {
        "submitted_count": len(submitted_ids),
        "updated_alpha_records": 0,
        "deleted_check_results": 0,
    }
    if not submitted_ids:
        return summary

    now = utc_now()
    with connect() as conn:
        for alpha_id in submitted_ids:
            row = conn.execute("SELECT payload FROM alpha_records WHERE alpha_id = ?", (alpha_id,)).fetchone()
            payload: dict[str, Any] = {}
            if row and row["payload"]:
                try:
                    loaded = json.loads(row["payload"])
                    payload = loaded if isinstance(loaded, dict) else {}
                except json.JSONDecodeError:
                    payload = {}
            payload["submitted_cleanup"] = True
            payload["submitted_cleanup_at"] = now

            cur = conn.execute(
                """
                UPDATE alpha_records
                SET status = 'SUBMITTED',
                    source = 'submitted_cleanup',
                    payload = ?,
                    updated_at = ?
                WHERE alpha_id = ?
                """,
                (json.dumps(payload, ensure_ascii=False), now, alpha_id),
            )
            summary["updated_alpha_records"] += cur.rowcount

            cur = conn.execute("DELETE FROM check_results WHERE alpha_id = ?", (alpha_id,))
            summary["deleted_check_results"] += cur.rowcount

    return summary


def prune_old_check_results() -> int:
    with connect() as conn:
        cur = conn.execute(
            """
            DELETE FROM check_results
            WHERE id NOT IN (
                SELECT MAX(id)
                FROM check_results
                GROUP BY alpha_id
            )
            """
        )
        return int(cur.rowcount)


def fetch_submitted_alpha_ids(limit: int = 100, max_pages: int = 20) -> list[str]:
    username = get_setting("wq_username")
    password = get_setting("wq_password")
    if not username or not password:
        raise ValueError("Missing WorldQuant credentials in Settings.")

    session = login_with_credentials(username, password)
    try:
        ids: list[str] = []
        offset = 0
        total = None
        while total is None or offset < total:
            if offset // limit >= max_pages:
                break
            url = (
                "https://api.worldquantbrain.com/users/self/alphas"
                f"?stage=OS&limit={limit}&offset={offset}&order=-dateSubmitted"
            )
            resp = session.get(url, timeout=30)
            if resp.status_code == 429:
                raise RuntimeError("WQ submitted alpha fetch was rate limited (429).")
            if resp.status_code >= 400:
                raise RuntimeError(f"WQ submitted alpha fetch failed: status={resp.status_code} body={resp.text[:300]}")
            data = resp.json()
            total = int(data.get("count") or 0)
            results = data.get("results") or []
            for item in results:
                alpha_id = item.get("id") if isinstance(item, dict) else None
                if alpha_id:
                    ids.append(str(alpha_id))
            if len(results) < limit:
                break
            offset += limit
        return ids
    finally:
        session.close()


def run_submitted_cleanup_job(job_id: int, params: dict[str, Any] | None = None) -> None:
    params = params or {}
    update_job(job_id, status="running", progress_current=0, progress_total=100, message="Fetching submitted alpha ids...")
    add_job_event(job_id, "info", "Fetching submitted alpha ids for local cleanup.", params)

    limit = int(params.get("limit") or 100)
    max_pages = int(params.get("max_pages") or 20)
    submitted_ids = fetch_submitted_alpha_ids(limit=limit, max_pages=max_pages)
    update_job(
        job_id,
        progress_current=40,
        progress_total=100,
        message=f"Fetched {len(submitted_ids)} submitted alphas. Cleaning local candidates...",
    )

    summary = cleanup_submitted_alpha_inputs(submitted_ids)
    summary["deleted_old_check_results"] = prune_old_check_results()
    update_job(job_id, progress_current=100, progress_total=100, message=f"Submitted cleanup finished: {summary}")
    add_job_event(job_id, "info", "Submitted cleanup finished.", summary)

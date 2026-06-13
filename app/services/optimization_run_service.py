from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from ..job_runner import JobRunner
from ..paths import LOG_DIR
from ..storage import add_job_event, connect, get_setting, update_job
from .alpha_enhancement import generate_variants_for_plan
from .job_params import normalize_optimization_params
from .optimization_planner import build_optimization_plan
from .simulation_service import run_simulation_pool_with_control


def parse_alpha_ids(text: str) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for raw in str(text or "").replace(",", "\n").splitlines():
        alpha_id = raw.strip()
        if alpha_id and alpha_id not in seen:
            seen.add(alpha_id)
            ids.append(alpha_id)
    return ids


def collect_optimization_plans(params: dict[str, Any]) -> list[Any]:
    params = normalize_optimization_params(params)
    mode = str(params.get("source_mode") or "recent")
    limit = _positive_int(params.get("candidate_limit"), 20)
    manual_ids = parse_alpha_ids(str(params.get("alpha_ids") or ""))

    query, values = _candidate_query(mode, limit, manual_ids, params)
    with connect() as conn:
        rows = conn.execute(query, values).fetchall()

    plans = []
    for row in rows:
        row_dict = dict(row)
        plan = build_optimization_plan(
            row_dict,
            check_payload=row_dict.get("check_payload"),
            check_message=row_dict.get("check_message") or "",
            check_result=row_dict.get("check_result") or "",
        )
        if plan.should_optimize:
            plans.append(plan)
    return plans[:limit]


def run_optimization_job(job_id: int, params: dict[str, Any]) -> None:
    params = normalize_optimization_params(params)
    runner = JobRunner()
    update_job(job_id, progress_current=0, progress_total=100, message="Collecting optimization candidates...")
    add_job_event(job_id, "info", "Collecting optimization candidates.", params)

    plans = collect_optimization_plans(params)
    if not plans:
        update_job(job_id, progress_current=100, progress_total=100, message="No optimizable candidates found.")
        add_job_event(job_id, "warning", "No optimizable candidates found.")
        return

    variant_tasks: list[tuple[str, int, str]] = []
    for index, plan in enumerate(plans, start=1):
        runner.check_paused(job_id)
        update_job(
            job_id,
            progress_current=index,
            progress_total=len(plans),
            message=f"Generating variants {index}/{len(plans)} for {plan.alpha_id}...",
        )
        variants = generate_variants_for_plan(plan, max_variants=None)
        neutralization = str(getattr(plan, "source_neutralization", "") or "SUBINDUSTRY")
        add_job_event(
            job_id,
            "info",
            f"Generated {len(variants)} variants for {plan.alpha_id}.",
            {
                "alpha_id": plan.alpha_id,
                "name": plan.name,
                "variant_count": len(variants),
                "neutralization": neutralization,
            },
        )
        for variant in variants:
            variant_tasks.append((variant.expression, 0, neutralization))

    if not variant_tasks:
        update_job(job_id, progress_current=100, progress_total=100, message="Candidates produced no valid variants.")
        add_job_event(job_id, "warning", "Candidates produced no valid variants.")
        return

    child_count = _positive_int(params.get("children_per_request"), 1)
    region = str(params.get("region") or get_setting("region", "USA"))
    universe = str(params.get("universe") or get_setting("universe", "TOP3000"))
    grouped_tasks = group_tasks_by_neutralization(variant_tasks)
    total_requests = sum((len(tasks) + child_count - 1) // child_count for tasks in grouped_tasks.values())

    add_job_event(
        job_id,
        "info",
        f"Submitting {len(variant_tasks)} optimization variants in {total_requests} request(s).",
        {
            "variant_count": len(variant_tasks),
            "request_count": total_requests,
            "children_per_request": child_count,
            "neutralizations": sorted(grouped_tasks),
        },
    )
    for neutralization, tasks in grouped_tasks.items():
        runner.check_paused(job_id)
        chunks = [tasks[i:i + child_count] for i in range(0, len(tasks), child_count)]
        alpha_pools = [[chunk] for chunk in chunks]
        log_path = LOG_DIR / f"optimization_progress_{job_id}_{neutralization}.jsonl"
        run_simulation_pool_with_control(
            job_id=job_id,
            alpha_pools=alpha_pools,
            neut=neutralization,
            region=region,
            universe=universe,
            log_path=log_path,
        )


def extract_source_neutralization(payload: Any, default: str = "SUBINDUSTRY") -> str:
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {}
    if not isinstance(payload, dict):
        return default
    settings = payload.get("settings")
    if isinstance(settings, dict):
        value = settings.get("neutralization")
        if value:
            return str(value)
    return default


def group_tasks_by_neutralization(tasks: list[tuple[str, int, str]]) -> dict[str, list[tuple[str, int]]]:
    grouped: dict[str, list[tuple[str, int]]] = {}
    for expression, decay, neutralization in tasks:
        grouped.setdefault(neutralization or "SUBINDUSTRY", []).append((expression, decay))
    return grouped


def _candidate_query(
    mode: str,
    limit: int,
    manual_ids: list[str],
    params: dict[str, Any],
) -> tuple[str, list[Any]]:
    base = """
        SELECT
            a.alpha_id,
            a.name,
            a.fitness,
            a.margin,
            a.payload,
            a.updated_at,
            c.result AS check_result,
            c.message AS check_message,
            c.payload AS check_payload
        FROM alpha_records a
        LEFT JOIN (
            SELECT c1.*
            FROM check_results c1
            INNER JOIN (
                SELECT alpha_id, MAX(id) AS max_id
                FROM check_results
                GROUP BY alpha_id
            ) latest ON latest.max_id = c1.id
        ) c ON c.alpha_id = a.alpha_id
    """
    values: list[Any] = []
    where: list[str] = []
    if mode == "manual" and manual_ids:
        placeholders = ",".join("?" for _ in manual_ids)
        where.append(f"a.alpha_id IN ({placeholders})")
        values.extend(manual_ids)
    elif mode == "range":
        start_date = str(params.get("start_date") or "").strip()
        end_date = str(params.get("end_date") or "").strip()
        if start_date:
            where.append("a.updated_at >= ?")
            values.append(f"{start_date}T00:00:00")
        if end_date:
            where.append("a.updated_at <= ?")
            values.append(f"{end_date}T23:59:59")
    else:
        days = _positive_int(params.get("recent_days"), 14)
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).replace(microsecond=0).isoformat()
        where.append("a.updated_at >= ?")
        values.append(cutoff)

    sql = base
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY a.updated_at DESC LIMIT ?"
    values.append(limit * 3)
    return sql, values


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except Exception:
        return default
    return parsed if parsed > 0 else default

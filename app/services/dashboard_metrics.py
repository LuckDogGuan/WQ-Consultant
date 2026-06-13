from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from ..storage import connect, get_setting
from .optimization_planner import list_optimization_plans


LOCAL_TZ = ZoneInfo("Asia/Shanghai")


def local_daily_start(now: datetime | None = None, reset_hour: int = 0) -> datetime:
    current = now or datetime.now(LOCAL_TZ)
    if current.tzinfo is None:
        current = current.replace(tzinfo=LOCAL_TZ)
    current = current.astimezone(LOCAL_TZ)
    start = current.replace(hour=reset_hour, minute=0, second=0, microsecond=0)
    if current < start:
        start -= timedelta(days=1)
    return start


def get_dashboard_metrics(now: datetime | None = None) -> dict[str, int | str]:
    backtest_start = _utc_iso(local_daily_start(now, reset_hour=12))
    daily_start = _utc_iso(local_daily_start(now, reset_hour=0))
    backtest_limit = _int_setting("backtest_daily_limit", 4500)
    check_limit = _int_setting("check_daily_limit", 4500)
    submit_regular_limit = _int_setting("submit_daily_regular_limit", 4)
    submit_super_limit = _int_setting("submit_daily_super_limit", 1)

    counts: dict[str, int | str] = {
        "backtest_daily_limit": backtest_limit,
        "check_daily_limit": check_limit,
        "submit_daily_regular_limit": submit_regular_limit,
        "submit_daily_super_limit": submit_super_limit,
        "submit_daily_limit": submit_regular_limit + submit_super_limit,
        "backtest_daily_reset": "12:00",
    }

    with connect() as conn:
        counts["alpha_records"] = conn.execute("SELECT COUNT(*) FROM alpha_records").fetchone()[0]
        counts["check_results"] = conn.execute("SELECT COUNT(*) FROM check_results").fetchone()[0]
        counts["errors"] = conn.execute("SELECT COUNT(*) FROM errors").fetchone()[0]
        counts["ppa_count"] = conn.execute("SELECT COUNT(*) FROM alpha_records WHERE alpha_type = 'PPA'").fetchone()[0]
        counts["ra_count"] = conn.execute("SELECT COUNT(*) FROM alpha_records WHERE alpha_type = 'RA'").fetchone()[0]
        counts["atom_count"] = conn.execute("SELECT COUNT(*) FROM alpha_records WHERE alpha_type = 'ATOM'").fetchone()[0]
        counts["backtest_daily_done"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM alpha_records
            WHERE source LIKE 'job_%' AND created_at >= ?
            """,
            (backtest_start,),
        ).fetchone()[0]
        counts["check_daily_done"] = conn.execute(
            "SELECT COUNT(*) FROM check_results WHERE created_at >= ?",
            (daily_start,),
        ).fetchone()[0]
        counts["submit_daily_super"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM alpha_records
            WHERE status = 'SUBMITTED' AND alpha_type = 'PPA' AND updated_at >= ?
            """,
            (daily_start,),
        ).fetchone()[0]
        counts["submit_daily_regular"] = conn.execute(
            """
            SELECT COUNT(*)
            FROM alpha_records
            WHERE status = 'SUBMITTED' AND alpha_type != 'PPA' AND updated_at >= ?
            """,
            (daily_start,),
        ).fetchone()[0]

    counts["submit_daily_total"] = int(counts["submit_daily_regular"]) + int(counts["submit_daily_super"])
    plans = list_optimization_plans(limit=1000)
    counts["optimization_total"] = len(plans)
    counts["optimization_optimizable"] = sum(1 for plan in plans if plan.should_optimize)
    counts["optimization_min_submit"] = sum(
        1 for plan in plans if plan.should_optimize and plan.level in {"marginal", "standard", "premium"}
    )
    counts["backtest_daily_pct"] = _pct(int(counts["backtest_daily_done"]), backtest_limit)
    counts["check_daily_pct"] = _pct(int(counts["check_daily_done"]), check_limit)
    counts["submit_daily_pct"] = _pct(int(counts["submit_daily_total"]), int(counts["submit_daily_limit"]))
    counts["optimization_pct"] = _pct(int(counts["optimization_min_submit"]), max(1, int(counts["optimization_total"])))
    return counts


def _utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def _int_setting(key: str, default: int) -> int:
    try:
        return max(0, int(get_setting(key, str(default))))
    except (TypeError, ValueError):
        return default


def _pct(done: int, limit: int) -> int:
    if limit <= 0:
        return 0
    return max(0, min(100, round(done * 100 / limit)))

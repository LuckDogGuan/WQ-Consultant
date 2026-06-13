from __future__ import annotations

from typing import Any


OPTIMIZATION_PARAMS_SCHEMA_VERSION = 2


def normalize_optimization_params(params: dict[str, Any] | None) -> dict[str, Any]:
    raw = dict(params or {})
    return {
        "schema_version": OPTIMIZATION_PARAMS_SCHEMA_VERSION,
        "source_mode": _one_of(raw.get("source_mode"), {"recent", "range", "manual"}, "recent"),
        "recent_days": _positive_int(raw.get("recent_days"), 14),
        "candidate_limit": _positive_int(raw.get("candidate_limit"), 20),
        "start_date": str(raw.get("start_date") or ""),
        "end_date": str(raw.get("end_date") or ""),
        "alpha_ids": str(raw.get("alpha_ids") or ""),
        "children_per_request": _positive_int(raw.get("children_per_request"), 1),
        "region": str(raw.get("region") or ""),
        "universe": str(raw.get("universe") or ""),
    }


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except Exception:
        return default
    return parsed if parsed > 0 else default


def _one_of(value: Any, allowed: set[str], default: str) -> str:
    parsed = str(value or "")
    return parsed if parsed in allowed else default

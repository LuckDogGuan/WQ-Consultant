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
        "level_filter": _one_of(raw.get("level_filter"), {"S", "A", "B", "C", "all"}, "C"),
        "start_date": str(raw.get("start_date") or ""),
        "end_date": str(raw.get("end_date") or ""),
        "alpha_ids": str(raw.get("alpha_ids") or ""),
        "children_per_request": _positive_int(raw.get("children_per_request"), 1),
        "region": str(raw.get("region") or ""),
        "universe": str(raw.get("universe") or ""),
        "group_neutralization": raw.get("group_neutralization") or ["subindustry"],
        "trade_std_window": _positive_int(raw.get("trade_std_window"), 5),
        "trade_std_threshold": float(raw.get("trade_std_threshold") or 0.01),
        "decay_windows": str(raw.get("decay_windows") or "5,10,20"),
        "max_variants": _positive_int(raw.get("max_variants"), 10),
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

BACKTEST_PARAMS_SCHEMA_VERSION = 1
BACKTEST_REGIONS = ("USA", "ASI", "EUR")
BACKTEST_STAGES = ("FO", "SO", "TH")

# Table-driven on purpose: WQ account/advisor access changes over time, so later
# expansion is one data entry instead of scattered route/template logic.
ADVISOR_LEVEL_DATASET_PREFIXES: dict[str, tuple[str, ...]] = {
    "starter": ("fundamental", "pv"),
    "gold": ("fundamental", "pv", "analyst", "model"),
    "master": ("*",),
}

DEFAULT_STAGE_CONFIG: dict[str, dict[str, int]] = {
    "FO": {"children": 6, "threads": 10},
    "SO": {"children": 5, "threads": 8},
    "TH": {"children": 5, "threads": 8},
}


def normalize_backtest_params(params: dict[str, Any] | None) -> dict[str, Any]:
    raw = dict(params or {})
    advisor_level = _one_of(raw.get("advisor_level"), set(ADVISOR_LEVEL_DATASET_PREFIXES), "gold")
    regions = _region_list(raw.get("regions"), list(BACKTEST_REGIONS))
    region_stage_config = _region_stage_config(raw)
    dataset_ids = [str(item).strip() for item in raw.get("dataset_ids", []) if str(item).strip()]
    allowed_dataset_ids = [item for item in dataset_ids if advisor_level_allows_dataset(advisor_level, item)]

    return {
        "schema_version": BACKTEST_PARAMS_SCHEMA_VERSION,
        "profile": str(raw.get("profile") or "wang_strict"),
        "advisor_level": advisor_level,
        "regions": regions,
        "dataset_ids": dataset_ids,
        "allowed_dataset_ids": allowed_dataset_ids,
        "blocked_dataset_ids": [item for item in dataset_ids if item not in allowed_dataset_ids],
        "run_fo": _bool(raw.get("run_fo"), True),
        "run_so": _bool(raw.get("run_so"), True),
        "run_th": _bool(raw.get("run_th"), True),
        "region_stage_config": region_stage_config,
        "self_corr_safe": _float(raw.get("self_corr_safe"), 0.68),
        "self_corr_hard": _float(raw.get("self_corr_hard"), 0.70),
        "prod_corr_good": _float(raw.get("prod_corr_good"), 0.50),
        "prod_corr_hard": _float(raw.get("prod_corr_hard"), 0.70),
        "turnover_warn": _float(raw.get("turnover_warn"), 0.10),
        "turnover_hard": _float(raw.get("turnover_hard"), 0.15),
        "operator_count_max": _positive_int(raw.get("operator_count_max"), 8),
        "hide_grade_d_local": _bool(raw.get("hide_grade_d_local"), True),
        "retire_grade_d_remote": _bool(raw.get("retire_grade_d_remote"), True),
    }


def advisor_level_allows_dataset(advisor_level: str, dataset_id: str) -> bool:
    prefixes = ADVISOR_LEVEL_DATASET_PREFIXES.get(str(advisor_level or "").lower()) or ADVISOR_LEVEL_DATASET_PREFIXES["gold"]
    dataset = str(dataset_id or "").lower()
    return "*" in prefixes or any(dataset.startswith(prefix.lower()) for prefix in prefixes)


def _region_list(value: Any, default: list[str]) -> list[str]:
    if isinstance(value, str):
        items = [item.strip().upper() for item in value.replace(";", ",").split(",")]
    elif isinstance(value, (list, tuple, set)):
        items = [str(item).strip().upper() for item in value]
    else:
        items = []
    selected = [item for item in items if item in BACKTEST_REGIONS]
    return selected or default


def _region_stage_config(raw: dict[str, Any]) -> dict[str, dict[str, dict[str, int]]]:
    shared = {
        stage: {
            "children": _positive_int(raw.get(f"{stage.lower()}_backtest_children"), fallback["children"]),
            "threads": _positive_int(raw.get(f"{stage.lower()}_backtest_threads"), fallback["threads"]),
        }
        for stage, fallback in DEFAULT_STAGE_CONFIG.items()
    }
    config: dict[str, dict[str, dict[str, int]]] = {}
    for region in BACKTEST_REGIONS:
        config[region] = {stage: dict(shared[stage]) for stage in BACKTEST_STAGES}
    return config


def _bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "on", "yes", "y"}


def _float(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default

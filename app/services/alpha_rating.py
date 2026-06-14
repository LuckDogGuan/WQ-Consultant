from __future__ import annotations

import json
from typing import Any, Mapping


FAILED_RESULTS = {"FAIL", "FAILED", "ERROR"}
WARNING_RESULTS = {"WARNING", "WARN"}

METRIC_LABELS = {
    "elite": "顶级因子",
    "premium": "优质因子",
    "standard": "一般因子",
    "marginal": "边际因子",
    "substandard": "不合格因子",
}

CORRELATION_LABELS = {
    "PPA": "PPA 优秀因子",
    "RA": "RA 优秀因子",
    "ATOM": "ATOM 优秀因子",
    "MARGINAL": "边际相关性因子",
    "SKIP": "跳过因子",
}


def loads_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str) and payload.strip():
        try:
            data = json.loads(payload)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_metric(record: Mapping[str, Any], payload: Mapping[str, Any], key: str) -> float | None:
    value = to_float(record.get(key))
    if value is not None:
        return value

    is_metrics = payload.get("is") if isinstance(payload.get("is"), Mapping) else {}
    return to_float(is_metrics.get(key))


def extract_checks(payload: Any) -> list[dict[str, Any]]:
    data = loads_payload(payload)
    is_data = data.get("is") if isinstance(data.get("is"), dict) else {}
    checks = is_data.get("checks", [])
    return [check for check in checks if isinstance(check, dict)] if isinstance(checks, list) else []


def count_failed_checks(payload: Any) -> int:
    return sum(
        1
        for check in extract_checks(payload)
        if str(check.get("result") or check.get("status") or "").upper() in FAILED_RESULTS
    )


def count_warning_checks(payload: Any) -> int:
    return sum(
        1
        for check in extract_checks(payload)
        if str(check.get("result") or check.get("status") or "").upper() in WARNING_RESULTS
    )


def classify_metric_level(fitness: Any, margin: Any) -> str:
    fit = to_float(fitness) or 0.0
    marg = to_float(margin) or 0.0

    if fit >= 3.0 and marg >= 0.0050:
        return "elite"
    if fit >= 2.5 and marg >= 0.0030:
        return "premium"
    if fit >= 1.5 and marg >= 0.0010:
        return "standard"
    if fit >= 1.0 and marg >= 0.0005:
        return "marginal"
    return "substandard"


def select_checks_payload(alpha_payload: Any, check_payload: Any = None) -> dict[str, Any]:
    check_data = loads_payload(check_payload)
    if extract_checks(check_data):
        return check_data
    return loads_payload(alpha_payload)


def build_alpha_rating(
    alpha_record: Mapping[str, Any],
    latest_check_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    latest_check_result = latest_check_result or {}
    alpha_payload = loads_payload(alpha_record.get("alpha_payload", alpha_record.get("payload")))
    check_payload = loads_payload(latest_check_result.get("check_payload", latest_check_result.get("payload")))
    checks_payload = select_checks_payload(alpha_payload, check_payload)

    fitness = extract_metric(alpha_record, alpha_payload, "fitness")
    margin = extract_metric(alpha_record, alpha_payload, "margin")
    returns = extract_metric(alpha_record, alpha_payload, "returns")
    drawdown = extract_metric(alpha_record, alpha_payload, "drawdown")

    metric_class = classify_metric_level(fitness, margin)
    failed_count = count_failed_checks(checks_payload)
    warning_count = count_warning_checks(checks_payload)
    submission_class = "substandard" if failed_count else metric_class

    raw_type = str(alpha_record.get("alpha_type") or "").upper()
    correlation_label = CORRELATION_LABELS.get(raw_type, "未分类")
    check_result = str(latest_check_result.get("result") or alpha_record.get("result") or "").upper()

    reason = (
        f"checks_failed={failed_count}; metric={metric_class}; source="
        f"{'latest_check' if extract_checks(check_payload) else 'alpha_payload'}"
    )

    return {
        "fitness": fitness,
        "margin": margin,
        "returns": returns,
        "drawdown": drawdown,
        "metric_class": metric_class,
        "metric_label": METRIC_LABELS[metric_class],
        "submission_class": submission_class,
        "submission_label": METRIC_LABELS[submission_class],
        "check_result": check_result,
        "correlation_type": raw_type or "UNKNOWN",
        "correlation_label": correlation_label,
        "correlation_class": raw_type or "secondary",
        "failed_check_count": failed_count,
        "warning_check_count": warning_count,
        "rating_reason": reason,
        "alpha_level": METRIC_LABELS[submission_class],
        "level_class": submission_class,
    }

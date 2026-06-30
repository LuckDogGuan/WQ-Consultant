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
    "S": "S级 黄金优秀",
    "A": "A级 标准候选",
    "B": "B级 需要审核",
    "C": "C级 需要优化",
    "D": "D级 垃圾隐藏",
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


from functools import lru_cache

@lru_cache(maxsize=16384)
def _build_alpha_rating_cached(
    alpha_id: str,
    alpha_type: str,
    name: str,
    region: str,
    universe: str,
    sharpe: float | None,
    fitness: float | None,
    prod_corr: float | None,
    ppa_corr: float | None,
    margin: float | None,
    returns: float | None,
    drawdown: float | None,
    payload_str: str,
    updated_at: str,
    check_result: str | None,
    check_payload_str: str | None,
    check_prod_corr: float | None
) -> dict[str, Any]:
    alpha_record = {
        "alpha_id": alpha_id,
        "alpha_type": alpha_type,
        "name": name,
        "region": region,
        "universe": universe,
        "sharpe": sharpe,
        "fitness": fitness,
        "prod_corr": prod_corr,
        "ppa_corr": ppa_corr,
        "margin": margin,
        "returns": returns,
        "drawdown": drawdown,
        "payload": payload_str,
        "updated_at": updated_at
    }
    latest_check = {
        "result": check_result,
        "payload": check_payload_str,
        "prod_corr": check_prod_corr
    }
    return _build_alpha_rating_impl(alpha_record, latest_check)

def build_alpha_rating(
    alpha_record: Mapping[str, Any],
    latest_check_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    latest_check_result = latest_check_result or {}
    
    alpha_payload = alpha_record.get("alpha_payload") or alpha_record.get("payload") or {}
    if not isinstance(alpha_payload, str):
        try:
            alpha_payload_str = json.dumps(alpha_payload, sort_keys=True)
        except Exception:
            alpha_payload_str = "{}"
    else:
        alpha_payload_str = alpha_payload
        
    check_payload = latest_check_result.get("check_payload") or latest_check_result.get("payload") or {}
    if not isinstance(check_payload, str):
        try:
            check_payload_str = json.dumps(check_payload, sort_keys=True)
        except Exception:
            check_payload_str = "{}"
    else:
        check_payload_str = check_payload

    return _build_alpha_rating_cached(
        str(alpha_record.get("alpha_id") or ""),
        str(alpha_record.get("alpha_type") or ""),
        str(alpha_record.get("name") or ""),
        str(alpha_record.get("region") or ""),
        str(alpha_record.get("universe") or ""),
        alpha_record.get("sharpe"),
        alpha_record.get("fitness"),
        alpha_record.get("prod_corr"),
        alpha_record.get("ppa_corr"),
        alpha_record.get("margin"),
        alpha_record.get("returns"),
        alpha_record.get("drawdown"),
        alpha_payload_str,
        str(alpha_record.get("updated_at") or ""),
        latest_check_result.get("result"),
        check_payload_str,
        latest_check_result.get("prod_corr")
    )

def _build_alpha_rating_impl(
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

    # 引入 S/A/B/C/D 评级诊断模型
    from .template_iteration import grade_candidate_result
    sharpe = extract_metric(alpha_record, alpha_payload, "sharpe")
    turnover = extract_metric(alpha_record, alpha_payload, "turnover") or to_float(alpha_payload.get("is", {}).get("turnover"))
    self_corr = to_float(alpha_record.get("self_corr")) or 0.0
    prod_corr = to_float(alpha_record.get("prod_corr")) or to_float(latest_check_result.get("prod_corr")) or 0.0
    
    grading = grade_candidate_result({
        "sharpe": sharpe,
        "fitness": fitness,
        "margin": margin,
        "turnover": turnover,
        "self_corr": self_corr,
        "prod_corr": prod_corr,
        "failed_checks": count_failed_checks(checks_payload),
        "status": str(latest_check_result.get("result") or alpha_record.get("result") or "").upper(),
        "alpha_type": str(alpha_record.get("alpha_type") or "").upper(),
        "payload": alpha_payload,
    })
    grade = grading.get("grade", "C")
    grade_labels = {
        "S": "S级: 直接提交",
        "A": "A级: 标准候选",
        "B": "B级: 需要审核",
        "C": "C级: 需要优化",
        "D": "D级: 垃圾隐藏",
    }

    # 因子评级是在S级别里面分类的，分三个等级：Premium(优质), Standard(一般), Marginal(边际)
    # 非S级因子评级为 substandard (不合格)
    failed_count = count_failed_checks(checks_payload)
    if grade == "S" and not failed_count:
        s_sharpe = sharpe or 0.0
        s_fit = fitness or 0.0
        s_margin = margin or 0.0
        s_corr = prod_corr or 0.0
        
        # 1. Premium (优质级)
        if s_sharpe >= 1.70 and s_fit >= 1.50 and s_margin >= 0.0015 and s_corr <= 0.35:
            submission_class = "premium"
        # 2. Standard (一般级)
        elif s_sharpe >= 1.58 and s_fit >= 1.20 and s_margin >= 0.0012 and s_corr <= 0.45:
            submission_class = "standard"
        # 3. Marginal (边际级)
        else:
            submission_class = "marginal"
    else:
        submission_class = "substandard"

    failed_count = count_failed_checks(checks_payload)
    warning_count = count_warning_checks(checks_payload)

    raw_type = str(alpha_record.get("alpha_type") or "").upper()
    correlation_label = CORRELATION_LABELS.get(raw_type, "未分类")
    check_result = str(latest_check_result.get("result") or alpha_record.get("result") or "").upper()

    reason = (
        f"checks_failed={failed_count}; grade={grade}; rating={submission_class}; source="
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
        "grade": grade,
        "grade_label": grade_labels.get(grade, "C级: 需要优化"),
    }

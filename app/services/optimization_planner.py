from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Any

from ..storage import connect
from .expression_validator import validate_expression


ACTIONABLE_LEVELS = {"marginal", "standard", "premium"}
FAILED_RESULTS = {"FAIL", "FAILED", "ERROR"}

STRATEGY_BY_CHECK = {
    "SELF_CORRELATION": ("decorrelate", ["group", "trade", "stable"]),
    "PROD_CORRELATION": ("prod_decorrelate", ["group", "template", "stable"]),
    "LOW_SHARPE": ("improve_performance", ["template", "runtime", "basic", "power"]),
    "LOW_FITNESS": ("improve_performance", ["template", "runtime", "basic", "power"]),
    "LOW_MARGIN": ("improve_margin", ["stable", "power"]),
    "HIGH_TURNOVER": ("adjust_turnover", ["trade", "stable"]),
    "LOW_TURNOVER": ("adjust_turnover", ["trade", "stable"]),
}


@dataclass(frozen=True)
class OptimizationPlan:
    alpha_id: str
    name: str
    source_neutralization: str
    expression: str
    level: str
    failed_checks: list[dict[str, Any]]
    error_count: int
    should_optimize: bool
    skip_reason: str
    strategy: str
    suggested_modes: list[str]
    reason: str
    expression_valid: bool = True
    expression_errors: list[dict[str, Any]] | None = None
    expression_warnings: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def classify_alpha_level(fitness: float | None, margin: float | None) -> str:
    fit = _to_float(fitness) or 0.0
    marg = _to_float(margin) or 0.0

    if fit >= 2.5 and marg >= 0.0030:
        return "premium"
    if fit >= 1.5 and marg >= 0.0010:
        return "standard"
    if fit >= 1.0 and marg >= 0.0005:
        return "marginal"
    return "substandard"


def extract_alpha_expression(payload: dict[str, Any] | str | None) -> str:
    data = _loads_payload(payload)
    candidates = [
        data.get("expression"),
        data.get("regular") if isinstance(data.get("regular"), str) else None,
        data.get("regular", {}).get("code") if isinstance(data.get("regular"), dict) else None,
        data.get("raw_payload", {}).get("expression") if isinstance(data.get("raw_payload"), dict) else None,
    ]

    raw_payload = data.get("raw_payload")
    if isinstance(raw_payload, dict) and isinstance(raw_payload.get("regular"), dict):
        candidates.append(raw_payload["regular"].get("code"))

    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def extract_failed_checks(payload: dict[str, Any] | str | None, message: str = "") -> list[dict[str, Any]]:
    data = _loads_payload(payload)
    checks = data.get("is", {}).get("checks", []) if isinstance(data.get("is"), dict) else []
    failed: list[dict[str, Any]] = []

    if isinstance(checks, list):
        for check in checks:
            if not isinstance(check, dict):
                continue
            result = str(check.get("result") or check.get("status") or "").upper()
            if result not in FAILED_RESULTS:
                continue
            name = str(check.get("name") or "UNKNOWN").upper()
            failed.append(
                {
                    "name": name,
                    "result": result,
                    "value": check.get("value"),
                    "limit": check.get("limit"),
                }
            )

    if failed or not message:
        return failed

    return _extract_failed_checks_from_message(message)


def extract_alpha_neutralization(payload: dict[str, Any] | str | None, default: str = "SUBINDUSTRY") -> str:
    data = _loads_payload(payload)
    settings = data.get("settings")
    if isinstance(settings, dict) and settings.get("neutralization"):
        return str(settings["neutralization"])
    raw_payload = data.get("raw_payload")
    if isinstance(raw_payload, dict):
        raw_settings = raw_payload.get("settings")
        if isinstance(raw_settings, dict) and raw_settings.get("neutralization"):
            return str(raw_settings["neutralization"])
    return default


def build_optimization_plan(
    alpha_record: dict[str, Any],
    check_payload: dict[str, Any] | str | None = None,
    check_message: str = "",
    check_result: str = "",
) -> OptimizationPlan:
    payload = _loads_payload(alpha_record.get("payload"))
    alpha_id = str(alpha_record.get("alpha_id") or "")
    name = str(alpha_record.get("name") or payload.get("name") or "")
    source_neutralization = extract_alpha_neutralization(payload)
    expression = extract_alpha_expression(payload)
    level = classify_alpha_level(alpha_record.get("fitness"), alpha_record.get("margin"))
    failed_checks = extract_failed_checks(check_payload, check_message)
    error_count = len(failed_checks)
    has_check_result = bool(check_payload) or bool(check_message) or bool(check_result)

    if not expression:
        return _skip(alpha_id, name, source_neutralization, expression, level, failed_checks, "missing_expression")

    expression_validation = validate_expression(expression)
    if not expression_validation.is_valid:
        return _skip(
            alpha_id,
            name,
            source_neutralization,
            expression,
            level,
            failed_checks,
            "invalid_expression",
            expression_valid=False,
            expression_errors=expression_validation.errors,
            expression_warnings=expression_validation.warnings,
        )

    if error_count >= 2:
        return _skip(
            alpha_id,
            name,
            source_neutralization,
            expression,
            level,
            failed_checks,
            "too_many_failed_checks",
            expression_warnings=expression_validation.warnings,
        )

    if level not in ACTIONABLE_LEVELS and not has_check_result:
        return _skip(
            alpha_id,
            name,
            source_neutralization,
            expression,
            level,
            failed_checks,
            "substandard",
            expression_warnings=expression_validation.warnings,
        )

    strategy, modes, reason = choose_strategy(failed_checks, level, check_result)
    return OptimizationPlan(
        alpha_id=alpha_id,
        name=name,
        source_neutralization=source_neutralization,
        expression=expression,
        level=level,
        failed_checks=failed_checks,
        error_count=error_count,
        should_optimize=True,
        skip_reason="",
        strategy=strategy,
        suggested_modes=modes,
        reason=reason,
        expression_valid=True,
        expression_errors=[],
        expression_warnings=expression_validation.warnings,
    )


def choose_strategy(
    failed_checks: list[dict[str, Any]],
    level: str,
    check_result: str = "",
) -> tuple[str, list[str], str]:
    if failed_checks:
        check_name = str(failed_checks[0].get("name") or "UNKNOWN").upper()
        strategy, modes = STRATEGY_BY_CHECK.get(check_name, ("conservative_explore", ["stable", "template"]))
        return strategy, modes, f"single_failed_check:{check_name}"

    if str(check_result).upper() == "ERROR":
        return "conservative_explore", ["stable", "template"], "check_result_error_without_detail"

    if level == "premium":
        return "stabilize", ["stable"], "premium_metric_candidate"
    if level == "standard":
        return "improve_performance", ["template", "stable"], "standard_metric_candidate"
    return "improve_margin", ["stable", "power"], "marginal_metric_candidate"


def list_optimization_plans(limit: int = 200) -> list[OptimizationPlan]:
    limit = max(1, min(int(limit), 1000))
    with connect() as conn:
        rows = conn.execute(
            """
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
            ORDER BY a.updated_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    plans = []
    for row in rows:
        row_dict = dict(row)
        plans.append(
            build_optimization_plan(
                row_dict,
                check_payload=row_dict.get("check_payload"),
                check_message=row_dict.get("check_message") or "",
                check_result=row_dict.get("check_result") or "",
            )
        )
    return plans


def _skip(
    alpha_id: str,
    name: str,
    source_neutralization: str,
    expression: str,
    level: str,
    failed_checks: list[dict[str, Any]],
    reason: str,
    expression_valid: bool = True,
    expression_errors: list[dict[str, Any]] | None = None,
    expression_warnings: list[dict[str, Any]] | None = None,
) -> OptimizationPlan:
    return OptimizationPlan(
        alpha_id=alpha_id,
        name=name,
        source_neutralization=source_neutralization,
        expression=expression,
        level=level,
        failed_checks=failed_checks,
        error_count=len(failed_checks),
        should_optimize=False,
        skip_reason=reason,
        strategy="",
        suggested_modes=[],
        reason=reason,
        expression_valid=expression_valid,
        expression_errors=expression_errors or [],
        expression_warnings=expression_warnings or [],
    )


def _loads_payload(payload: dict[str, Any] | str | None) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str) and payload.strip():
        try:
            data = json.loads(payload)
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_failed_checks_from_message(message: str) -> list[dict[str, Any]]:
    names = []
    if "Failed checks:" in message:
        tail = message.split("Failed checks:", 1)[1]
        names = re.findall(r"([A-Z][A-Z0-9_]+)(?:\(|,|$)", tail)
    elif message:
        names = re.findall(r"\b([A-Z][A-Z0-9_]{2,})\b", message)

    return [{"name": name.upper(), "result": "FAIL", "value": None, "limit": None} for name in names]

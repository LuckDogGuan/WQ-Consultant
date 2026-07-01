from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field, replace
from itertools import product
from typing import Any

from .expression_validator import validate_expression


PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
SUPPORTED_PLACEHOLDERS = {"field", "field_a", "field_b", "days", "decay", "neutralization", "group"}


@dataclass(frozen=True)
class TemplateSpec:
    name: str
    expression: str
    placeholders: set[str]


@dataclass(frozen=True)
class TemplateIterationOptions:
    regions: list[str]
    max_candidates: int = 100
    operator_count_max: int = 8
    field_count_max: int = 3
    day_values: list[int] = field(default_factory=lambda: [20])
    decay_values: list[int] = field(default_factory=lambda: [0])
    neutralization_values: list[str] = field(default_factory=lambda: ["INDUSTRY"])
    group_values: list[str] = field(default_factory=lambda: ["industry"])
    good_qualities: set[str] = field(default_factory=lambda: {"GOOD", ""})


@dataclass(frozen=True)
class TemplateCandidate:
    template_name: str
    expression: str
    field_id: str = ""
    region: str = ""
    dataset_id: str = ""
    reason_code: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TemplateIterationResult:
    visible: list[TemplateCandidate]
    hidden: list[TemplateCandidate]
    summary: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "visible": [item.to_dict() for item in self.visible],
            "hidden": [item.to_dict() for item in self.hidden],
            "summary": self.summary,
        }


def dedupe_candidates(result: TemplateIterationResult) -> TemplateIterationResult:
    seen: set[str] = set()
    visible: list[TemplateCandidate] = []
    duplicates: list[TemplateCandidate] = []

    for candidate in result.visible:
        key = _expression_key(candidate.expression)
        if key in seen:
            duplicates.append(replace(candidate, reason_code="DUPLICATE_EXPRESSION"))
            continue
        seen.add(key)
        visible.append(candidate)

    summary = dict(result.summary)
    summary["visible_count"] = len(visible)
    summary["hidden_count"] = len(result.hidden) + len(duplicates)
    summary["duplicate_count"] = len(duplicates)
    summary["hidden_reason_counts"] = _hidden_reason_counts([*result.hidden, *duplicates])
    return TemplateIterationResult(
        visible=visible,
        hidden=[*result.hidden, *duplicates],
        summary=summary,
    )


def parse_templates(raw_templates: str | list[str]) -> list[TemplateSpec]:
    if isinstance(raw_templates, str):
        blocks = [block.strip() for block in re.split(r"\n\s*(?:---|\n)\s*\n?", raw_templates)]
    else:
        blocks = [str(block).strip() for block in raw_templates]

    templates: list[TemplateSpec] = []
    for index, expression in enumerate([block for block in blocks if block], start=1):
        templates.append(
            TemplateSpec(
                name=f"template_{index}",
                expression=expression,
                placeholders=set(PLACEHOLDER_RE.findall(expression)),
            )
        )
    return templates


def normalize_template_iteration_options(payload: dict[str, Any] | None) -> TemplateIterationOptions:
    raw = dict(payload or {})
    field_quality_mode = str(raw.get("field_quality_mode") or "GOOD_ONLY").upper()
    good_qualities = {"GOOD", ""}
    if field_quality_mode == "GOOD_AND_REVIEW":
        good_qualities.add("REVIEW")
    return TemplateIterationOptions(
        regions=_region_list(raw.get("regions"), ["USA"]),
        max_candidates=_positive_int(raw.get("max_candidates"), 100),
        operator_count_max=_positive_int(raw.get("operator_count_max"), 8),
        field_count_max=_positive_int(raw.get("field_count_max"), 3),
        day_values=_int_list(raw.get("day_values"), [20]),
        decay_values=_int_list(raw.get("decay_values"), [0]),
        neutralization_values=_str_list(raw.get("neutralization_values"), ["INDUSTRY"], upper=True),
        group_values=_str_list(raw.get("group_values"), ["industry"]),
        good_qualities=good_qualities,
    )


def expand_template_candidates(
    raw_templates: str | list[str],
    fields: list[dict[str, Any]],
    options: TemplateIterationOptions,
) -> TemplateIterationResult:
    templates = parse_templates(raw_templates)
    visible: list[TemplateCandidate] = []
    hidden: list[TemplateCandidate] = []
    truncated_count = 0

    if templates and not fields:
        hidden.append(_candidate(templates[0], {}, templates[0].expression, "NO_MATCHED_FIELDS"))
        return TemplateIterationResult(
            visible=[],
            hidden=hidden,
            summary={
                "template_count": len(templates),
                "visible_count": 0,
                "hidden_count": len(hidden),
                "truncated_count": 0,
                "hidden_reason_counts": _hidden_reason_counts(hidden),
            },
        )

    for template in templates:
        unknown_placeholders = template.placeholders - SUPPORTED_PLACEHOLDERS
        field_sets = _field_sets_for_template(template, fields)
        for field_set in field_sets:
            field_info = field_set[0]
            if not _region_allowed(field_info, options.regions):
                continue
            if unknown_placeholders:
                hidden.append(_candidate(template, field_info, template.expression, "UNKNOWN_PLACEHOLDER"))
                continue
            blocked_quality = next((classify_field_quality(item) for item in field_set if not _quality_allowed(classify_field_quality(item), options.good_qualities)), "")
            if blocked_quality:
                hidden.append(_candidate(template, field_info, template.expression, f"{blocked_quality}_FIELD"))
                continue
            for days, decay, neutralization, group in product(
                options.day_values,
                options.decay_values,
                options.neutralization_values,
                options.group_values,
            ):
                expression = _render_template(template.expression, field_set, days, decay, neutralization, group)
                validation = validate_expression(expression)
                if not validation.is_valid:
                    hidden.append(_candidate(template, field_info, expression, "EXPRESSION_INVALID", field_set))
                    continue
                complexity = count_expression_complexity(expression)
                if (
                    complexity["operator_count"] > options.operator_count_max
                    or complexity["field_count"] > options.field_count_max
                ):
                    hidden.append(_candidate(template, field_info, expression, "COMPLEXITY_LIMIT", field_set))
                    continue
                if len(visible) >= options.max_candidates:
                    truncated_count += 1
                    hidden.append(_candidate(template, field_info, expression, "CANDIDATE_EXPLOSION", field_set))
                    continue
                visible.append(_candidate(template, field_info, expression, "", field_set))

    return TemplateIterationResult(
        visible=visible,
        hidden=hidden,
        summary={
            "template_count": len(templates),
            "visible_count": len(visible),
            "hidden_count": len(hidden),
            "truncated_count": truncated_count,
            "hidden_reason_counts": _hidden_reason_counts(hidden),
        },
    )


def _render_template(
    template: str,
    field_set: tuple[dict[str, Any], ...],
    days: int,
    decay: int,
    neutralization: str,
    group: str,
) -> str:
    field_a = field_set[0] if field_set else {}
    field_b = field_set[1] if len(field_set) > 1 else field_a
    return (
        template.replace("{field_a}", _field_id(field_a))
        .replace("{field_b}", _field_id(field_b))
        .replace("{field}", _field_id(field_a))
        .replace("{days}", str(days))
        .replace("{decay}", str(decay))
        .replace("{neutralization}", neutralization)
        .replace("{group}", group)
    )


def _candidate(
    template: TemplateSpec,
    field_info: dict[str, Any],
    expression: str,
    reason_code: str = "",
    field_set: tuple[dict[str, Any], ...] | None = None,
) -> TemplateCandidate:
    field_set = field_set or (field_info,)
    return TemplateCandidate(
        template_name=template.name,
        expression=expression,
        field_id=",".join(_field_id(item) for item in field_set if _field_id(item)),
        region=str(field_info.get("region") or ""),
        dataset_id=str(field_info.get("dataset") or field_info.get("dataset_id") or ""),
        reason_code=reason_code,
    )


def _field_sets_for_template(template: TemplateSpec, fields: list[dict[str, Any]]) -> list[tuple[dict[str, Any], ...]]:
    if {"field_a", "field_b"} <= template.placeholders:
        return [(fields[index], fields[index + 1]) for index in range(0, len(fields) - 1, 2)]
    return [(field_info,) for field_info in fields]


def _field_id(field_info: dict[str, Any]) -> str:
    return str(field_info.get("id") or field_info.get("field_id") or "")


def _region_allowed(field_info: dict[str, Any], regions: list[str]) -> bool:
    return not regions or not field_info.get("region") or str(field_info["region"]).upper() in {r.upper() for r in regions}


def classify_field_quality(field_info: dict[str, Any]) -> str:
    quality = str(field_info.get("quality") or field_info.get("quality_tag") or "").strip().upper()
    if quality in {"BAD", "REVIEW"}:
        return quality
    return "GOOD"


def count_expression_complexity(expression: str) -> dict[str, int]:
    operators = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", expression)
    identifiers = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expression)
    operator_names = set(operators)
    keywords = {"true", "false", "nan", "dense"}
    fields = [item for item in identifiers if item not in operator_names and item.lower() not in keywords]
    return {"operator_count": len(operators), "field_count": len(set(fields))}


def create_template_iteration_job_params(
    candidates: list[dict[str, Any]],
    settings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    selected = []
    for item in candidates:
        expr = str(item.get("expression") or "")
        if not expr:
            continue
        # 本地表达式校验，防止非法表达式提交至后台回测任务
        validation = validate_expression(expr)
        if not validation.is_valid:
            errors_str = "; ".join(err.get("message", "") for err in validation.errors)
            raise ValueError(f"候选表达式存在语法错误: {expr}. 错误信息: {errors_str}")
        selected.append({
            "expression": expr,
            "region": str(item.get("region") or ""),
            "field_id": str(item.get("field_id") or ""),
            "dataset_id": str(item.get("dataset_id") or ""),
        })

    if not selected:
        raise ValueError("template_iteration job needs at least one selected candidate")

    raw_settings = dict(settings or {})
    return {
        "kind": "template_iteration",
        "universe": str(raw_settings.get("universe") or "TOP3000"),
        "delay": _positive_int(raw_settings.get("delay"), 1),
        "candidates": selected,
    }


def run_template_iteration_job(job_id: int, params: dict[str, Any]) -> None:
    candidates = params.get("candidates") or []
    custom_alphas = [
        str(item.get("expression") or "")
        for item in candidates
        if isinstance(item, dict) and item.get("expression")
    ]
    if not custom_alphas:
        raise ValueError("template_iteration job needs at least one candidate expression")

    from .simulation_service import run_backtest_job

    run_backtest_job(
        job_id,
        {
            "custom_alphas": custom_alphas,
            "neutralization": params.get("neutralization") or "INDUSTRY",
        },
    )


def _extract_yearly_stats(payload: Any) -> list[dict[str, Any]]:
    if not payload:
        return []
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            return []
    if not isinstance(payload, dict):
        return []
        
    # 1. 尝试 recordsets_data 中的 yearly-stats / yearly_stats
    rs_data = payload.get("recordsets_data")
    if isinstance(rs_data, dict):
        for key in ["yearly-stats", "yearly_stats"]:
            if key in rs_data and isinstance(rs_data[key], list):
                return rs_data[key]
                
    # 2. 尝试 raw_payload 中的 yearly-stats / yearly_stats
    raw = payload.get("raw_payload")
    if isinstance(raw, dict):
        for key in ["yearly-stats", "yearly_stats"]:
            if key in raw and isinstance(raw[key], list):
                return raw[key]
        if "is" in raw and isinstance(raw["is"], dict):
            if "year" in raw["is"] and isinstance(raw["is"]["year"], list):
                return raw["is"]["year"]
        rs_data_raw = raw.get("recordsets_data")
        if isinstance(rs_data_raw, dict):
            for key in ["yearly-stats", "yearly_stats"]:
                if key in rs_data_raw and isinstance(rs_data_raw[key], list):
                    return rs_data_raw[key]
                
    # 3. 尝试 top-level yearly-stats / yearly_stats
    for key in ["yearly-stats", "yearly_stats"]:
        if key in payload and isinstance(payload[key], list):
            return payload[key]
            
    # 4. 尝试 top-level is.year
    if "is" in payload and isinstance(payload["is"], dict):
        if "year" in payload["is"] and isinstance(payload["is"]["year"], list):
            return payload["is"]["year"]
            
    return []


def grade_candidate_result(metrics: dict[str, Any]) -> dict[str, Any]:
    sharpe = _float(metrics.get("sharpe"))
    fitness = _float(metrics.get("fitness"))
    margin = _float(metrics.get("margin"))
    turnover = _float(metrics.get("turnover"))
    self_corr = _float(metrics.get("self_corr"))
    prod_corr = _float(metrics.get("prod_corr"))
    failed_checks = int(_float(metrics.get("failed_checks")) or 0)
    status = str(metrics.get("status") or "").upper()
    alpha_type = str(metrics.get("alpha_type") or "").upper()

    reasons: list[str] = []
    if self_corr > 0.70:
        reasons.append("SC_RISK")
    if prod_corr >= 0.70:
        reasons.append("PC_RISK")
    if failed_checks or "FAIL" in status or "ERROR" in status:
        reasons.append("CHECK_FAIL")
    if sharpe is not None and sharpe < 0:
        reasons.append("NEGATIVE_SHARPE")
    if "SKIP" in status or "SKIP" in alpha_type:
        reasons.append("SKIP_STATUS")

    # 检测年化收益与换手率是否在任意年份出现归零情况 (厂字/停牌死因子)
    payload = metrics.get("payload") or {}
    
    # 检测 PnL 收益率交易日覆盖率 (低于 60% 判定为厂字死因子)
    if isinstance(payload, dict):
        pnl_cov = payload.get("pnl_coverage_rate")
        if pnl_cov is not None:
            try:
                if float(pnl_cov) < 0.60:
                    reasons.append("DEAD_ALPHA_RISK")
            except (ValueError, TypeError):
                pass
    
    # 3.5. 表达式未来函数泄漏检测 (如直接引用 \breturns\b)
    expression = metrics.get("expression") or ""
    if not expression and isinstance(payload, dict):
        from .optimization_planner import extract_alpha_expression
        expression = extract_alpha_expression(payload)
        
    if expression and re.search(r'\breturns\b', expression):
        reasons.append("DEAD_ALPHA_RISK")
        
    # 3.6. 交易股票数量检测 (防范超低样本过拟合)
    if isinstance(payload, dict):
        raw_payload = payload.get("raw_payload", {}) if "raw_payload" in payload else payload
        inst_count = raw_payload.get("instrumentCount") or raw_payload.get("instrument_count")
        if inst_count is not None:
            try:
                if int(inst_count) < 30:
                    reasons.append("DEAD_ALPHA_RISK")
            except (ValueError, TypeError):
                pass
                
    if isinstance(payload, dict):
        years = _extract_yearly_stats(payload)
        if isinstance(years, list) and len(years) > 0:
            # 增加 Long Count 和 Short Count 检测，如果任意一年为 0 则判定为厂字/停牌死因子
            has_zero_count = False
            for yr in years:
                try:
                    long_c = yr.get("longCount")
                    short_c = yr.get("shortCount")
                    if long_c is not None and float(long_c) == 0:
                        has_zero_count = True
                        break
                    if short_c is not None and float(short_c) == 0:
                        has_zero_count = True
                        break
                except (ValueError, TypeError):
                    pass
            if has_zero_count:
                reasons.append("DEAD_ALPHA_RISK")
            
            valid_years = []
            for yr in years:
                try:
                    year_val = int(yr.get("year", 0))
                    yr_returns = float(yr.get("returns", 0.0))
                    yr_turnover = float(yr.get("turnover", 0.0))
                    yr_sharpe = float(yr.get("sharpe", 0.0))
                    valid_years.append({
                        "year": year_val,
                        "returns": yr_returns,
                        "turnover": yr_turnover,
                        "sharpe": yr_sharpe
                    })
                except (ValueError, TypeError):
                    pass
            
            if valid_years:
                valid_years = sorted(valid_years, key=lambda y: y["year"], reverse=True)
                total_years = len(valid_years)
                
                # A. 基础检测：年份数量不足 3 年
                if total_years < 3:
                    reasons.append("DEAD_ALPHA_RISK")
                else:
                    # B. 单年零换手 + 零收益检测
                    has_dead_year = False
                    zero_years_count = 0
                    for yr in valid_years:
                        if abs(yr["turnover"]) < 0.0001 and abs(yr["returns"]) < 0.00001:
                            has_dead_year = True
                            zero_years_count += 1
                    
                    if has_dead_year:
                        reasons.append("DEAD_ALPHA_RISK")
                    # C. 零值年份占比过多 (超过 40%)
                    elif zero_years_count / total_years > 0.40:
                        reasons.append("DEAD_ALPHA_RISK")
                    else:
                        # D. 近两年平均 Sharpe 极低 (< 0.10) 或包含 0.0
                        recent_years = valid_years[:2]
                        recent_sharpes = [yr["sharpe"] for yr in recent_years]
                        l2y_sharpe = sum(recent_sharpes) / len(recent_sharpes) if recent_sharpes else 0.0
                        if any(abs(s) < 1e-9 for s in recent_sharpes) or l2y_sharpe < 0.10:
                            reasons.append("DEAD_ALPHA_RISK")
                        # E. 正收益年份占比不足 50%
                        else:
                            pos_years = sum(1 for yr in valid_years if yr["returns"] > 0)
                            if pos_years / total_years < 0.50:
                                reasons.append("DEAD_ALPHA_RISK")

    if turnover and (turnover < 0.01 or turnover > 0.70):
        reasons.append("TURNOVER_RISK")
    if sharpe is None or sharpe < 1.25 or fitness < 1.0 or margin <= 0:
        reasons.append("METRIC_WEAK")

    if any(reason in reasons for reason in {"NEGATIVE_SHARPE", "SKIP_STATUS", "DEAD_ALPHA_RISK"}):
        grade = "D"
        action = "discard"
    elif reasons:
        grade = "C"
        action = "optimize"
    elif self_corr <= 0.68 and prod_corr < 0.50 and sharpe >= 1.58 and fitness >= 1.0 and (margin is not None and margin >= 0.0010):
        grade = "S"
        action = "manual_submit_candidate"
    elif self_corr <= 0.70 and prod_corr < 0.70 and sharpe >= 1.50 and fitness >= 0.80 and (margin is not None and margin >= 0.0008):
        grade = "A"
        action = "manual_submit_candidate"
    elif self_corr <= 0.70 and prod_corr < 0.70 and sharpe >= 1.25 and fitness >= 0.60 and (margin is not None and margin >= 0.0005):
        grade = "B"
        action = "manual_review"
    else:
        grade = "C"
        action = "optimize"
    return {"grade": grade, "action": action, "reasons": reasons}


def _quality_allowed(quality: str, good_qualities: set[str]) -> bool:
    return quality in {item.upper() for item in good_qualities}


def _region_list(value: Any, default: list[str]) -> list[str]:
    return _str_list(value, default, upper=True)


def _int_list(value: Any, default: list[int]) -> list[int]:
    values = value if isinstance(value, list) else str(value or "").split(",")
    parsed: list[int] = []
    for item in values:
        try:
            parsed.append(int(item))
        except Exception:
            continue
    return parsed or default


def _str_list(value: Any, default: list[str], upper: bool = False) -> list[str]:
    values = value if isinstance(value, list) else str(value or "").split(",")
    parsed = [str(item).strip() for item in values if str(item).strip()]
    if upper:
        parsed = [item.upper() for item in parsed]
    return parsed or default


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except Exception:
        return default
    return parsed if parsed > 0 else default


def _float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _expression_key(expression: str) -> str:
    return re.sub(r"\s+", "", expression)


def _hidden_reason_counts(hidden: list[TemplateCandidate]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for candidate in hidden:
        if candidate.reason_code:
            counts[candidate.reason_code] = counts.get(candidate.reason_code, 0) + 1
    return counts

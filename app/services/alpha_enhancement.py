from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .expression_validator import validate_expression
from .optimization_planner import OptimizationPlan, build_optimization_plan
from ..storage import connect


DEFAULT_GROUPS = ["sector", "industry", "subindustry"]


@dataclass(frozen=True)
class AlphaVariant:
    source_alpha_id: str
    mode: str
    expression: str
    reason: str
    validation: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def generate_variants_for_plan(
    plan: OptimizationPlan,
    max_variants: int | None = 30,
    params: dict[str, Any] | None = None
) -> list[AlphaVariant]:
    if not plan.should_optimize or not plan.expression:
        return []

    variants: list[AlphaVariant] = []
    seen: set[str] = {plan.expression.strip()}
    for mode in plan.suggested_modes:
        for expression, reason in _expressions_for_mode(plan.expression, mode, params):
            normalized = expression.strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            validation = validate_expression(normalized).to_dict()
            if not validation["is_valid"]:
                continue
            variants.append(
                AlphaVariant(
                    source_alpha_id=plan.alpha_id,
                    mode=mode,
                    expression=normalized,
                    reason=reason,
                    validation=validation,
                )
            )
            if max_variants is not None and len(variants) >= max_variants:
                return variants
    return variants


def generate_variants_for_alpha_id(
    alpha_id: str,
    max_variants: int = 30,
    params: dict[str, Any] | None = None
) -> tuple[OptimizationPlan | None, list[AlphaVariant]]:
    with connect() as conn:
        row = conn.execute(
            """
            SELECT
                a.alpha_id,
                a.name,
                a.fitness,
                a.margin,
                a.payload,
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
            WHERE a.alpha_id = ?
            """,
            (alpha_id,),
        ).fetchone()

    if not row:
        return None, []

    row_dict = dict(row)
    plan = build_optimization_plan(
        row_dict,
        check_payload=row_dict.get("check_payload"),
        check_message=row_dict.get("check_message") or "",
        check_result=row_dict.get("check_result") or "",
    )
    return plan, generate_variants_for_plan(plan, max_variants=max_variants, params=params)


def _expressions_for_mode(expression: str, mode: str, params: dict[str, Any] | None = None) -> list[tuple[str, str]]:
    exp = expression.strip()
    params = params or {}
    
    # 提取中性化级别
    raw_groups = params.get("group_neutralization") or ["subindustry"]
    if isinstance(raw_groups, str):
        groups = [g.strip() for g in raw_groups.replace(",", "\n").splitlines() if g.strip()]
    elif isinstance(raw_groups, list):
        groups = [str(g).strip() for g in raw_groups if str(g).strip()]
    else:
        groups = ["subindustry"]
    if not groups:
        groups = ["subindustry"]
        
    # 提取 trade_when 参数
    std_window = int(params.get("trade_std_window") or 5)
    std_threshold = float(params.get("trade_std_threshold") or 0.01)
    
    # 提取 Decay 参数
    raw_decays = params.get("decay_windows") or [5, 10, 20]
    if isinstance(raw_decays, str):
        try:
            decays = [int(x.strip()) for x in raw_decays.replace(",", " ").split() if x.strip()]
        except Exception:
            decays = [5, 10, 20]
    elif isinstance(raw_decays, list):
        try:
            decays = [int(x) for x in raw_decays]
        except Exception:
            decays = [5, 10, 20]
    else:
        decays = [5, 10, 20]
    if not decays:
        decays = [5, 10, 20]

    if mode == "decorrelate":
        decorrelate_list = []
        for g in groups:
            decorrelate_list.append((f"group_neutralize({exp}, {g})", f"decorrelate:neutralize_{g}"))
            decorrelate_list.append((f"group_zscore({exp}, {g})", f"decorrelate:zscore_{g}"))
        for d in decays:
            decorrelate_list.append((f"ts_decay_linear({exp}, {d})", f"decorrelate:decay_linear_{d}"))
        decorrelate_list.append(
            (f"trade_when(greater(ts_std_dev({exp}, {std_window}), {std_threshold}), {exp}, -1)", f"decorrelate:vol_std_gate_{std_window}")
        )
        return decorrelate_list

    if mode == "stable":
        return [
            (f"winsorize({exp}, std=4)", "stable:winsorize_std_4"),
            (f"winsorize({exp}, std=6)", "stable:winsorize_std_6"),
            (f"ts_backfill({exp}, 20)", "stable:ts_backfill_20"),
            (f"ts_backfill({exp}, 60)", "stable:ts_backfill_60"),
        ]

    if mode == "group":
        return [
            (f"group_rank({exp}, {group})", f"group:rank_{group}")
            for group in groups
        ] + [
            (f"group_zscore({exp}, {group})", f"group:zscore_{group}")
            for group in groups
        ] + [
            (f"group_neutralize({exp}, {group})", f"group:neutralize_{group}")
            for group in groups
        ]

    if mode == "trade":
        return [
            (f"trade_when(is_not_nan({exp}), {exp}, -1)", "trade:non_nan_gate"),
            (f"trade_when(greater(volume, ts_mean(volume, 20)), {exp}, -1)", "trade:volume_gate"),
            (f"trade_when(greater(ts_std_dev({exp}, {std_window}), {std_threshold}), {exp}, -1)", f"trade:vol_std_gate_{std_window}"),
        ]

    if mode == "template":
        return [
            (f"rank({exp})", "template:rank"),
            (f"zscore({exp})", "template:zscore"),
            (f"normalize({exp})", "template:normalize"),
            (f"ts_rank({exp}, 20)", "template:ts_rank_20"),
            (f"ts_zscore({exp}, 20)", "template:ts_zscore_20"),
        ]

    if mode == "power":
        return [
            (f"signed_power({exp}, 0.5)", "power:signed_power_0_5"),
            (f"signed_power({exp}, 1.5)", "power:signed_power_1_5"),
            (f"signed_power({exp}, 2)", "power:signed_power_2"),
        ]

    if mode in {"runtime", "basic"}:
        return [
            (f"rank(ts_delta({exp}, 1))", f"{mode}:delta_rank"),
            (f"rank(ts_mean({exp}, 20))", f"{mode}:mean_rank_20"),
        ]
    return []

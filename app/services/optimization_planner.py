from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Any

from ..storage import connect
from .alpha_rating import classify_metric_level
from .expression_validator import validate_expression


ACTIONABLE_LEVELS = {"S", "A", "B", "C"}
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
    alpha_class: str = ""
    confidence_score: float = 0.0
    economic_suggestion: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def classify_alpha_level(fitness: float | None, margin: float | None) -> str:
    return classify_metric_level(fitness, margin)


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


def is_high_risk_garbage_alpha(alpha_record: dict[str, Any], check_result: str = "") -> bool:
    """判定因子是否属于负夏普、厂字（SKIP）或已失败的垃圾高危因子"""
    # 1. 负夏普
    sharpe = alpha_record.get("sharpe")
    if sharpe is not None:
        try:
            if float(sharpe) < 0:
                return True
        except (ValueError, TypeError):
            pass
            
    # 2. 厂字 / 跳过
    alpha_type = str(alpha_record.get("alpha_type") or "").upper()
    status = str(alpha_record.get("status") or "").upper()
    if alpha_type in ("SKIP", "C", "D") or status == "SKIP":
        return True
        
    # 3. 失败 / 错误 (相关性超标 CORR_FAIL 除外)
    result_upper = str(check_result or "").upper()
    if status == "CORR_FAIL":
        pass
    else:
        if result_upper in {"FAIL", "FAILED", "ERROR"}:
            return True
        if any(s in status for s in {"FAIL", "ERROR"}):
            return True
            
    # 3.2. PnL 交易覆盖率检测 (低于 60% 判定为厂字垃圾)
    payload_check = _loads_payload(alpha_record.get("payload")) or _loads_payload(alpha_record.get("alpha_payload"))
    if isinstance(payload_check, dict):
        pnl_cov = payload_check.get("pnl_coverage_rate")
        if pnl_cov is not None:
            try:
                if float(pnl_cov) < 0.60:
                    return True
            except (ValueError, TypeError):
                pass
        
    # 3.5. 表达式未来函数泄漏检测 (如直接引用 \breturns\b)
    payload = _loads_payload(alpha_record.get("payload"))
    if not payload:
        payload = _loads_payload(alpha_record.get("alpha_payload"))
        
    expression = extract_alpha_expression(payload)
    if expression:
        if re.search(r'\breturns\b', expression):
            return True
            
    # 3.6. 交易股票数量检测 (通常 WQ 最低要求 30 只以上，低于该值判定为过拟合垃圾)
    if payload:
        raw_payload = payload.get("raw_payload", {}) if "raw_payload" in payload else payload
        inst_count = raw_payload.get("instrumentCount") or raw_payload.get("instrument_count")
        if inst_count is not None:
            try:
                if int(inst_count) < 30:
                    return True
            except (ValueError, TypeError):
                pass
                
    # 4. 厂字 / 停牌死因子 (检测年化收益与换手率是否在任意年份出现归零情况)
    if payload:
        years = _extract_yearly_stats(payload)
        if isinstance(years, list) and len(years) > 0:
            # 增加 Long Count 和 Short Count 检测，如果任意一年为 0 则判定为厂字/停牌死因子
            for yr in years:
                try:
                    long_c = yr.get("longCount")
                    short_c = yr.get("shortCount")
                    if long_c is not None and float(long_c) == 0:
                        return True
                    if short_c is not None and float(short_c) == 0:
                        return True
                except (ValueError, TypeError):
                    pass

            # 整理年度数据
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
                # 按照年份降序排列
                valid_years = sorted(valid_years, key=lambda y: y["year"], reverse=True)
                total_years = len(valid_years)
                
                # A. 基础：年份数量不足 3 年 
                if total_years < 3:
                    return True
                
                # B. 单年零换手 + 零收益检测
                has_dead_year = False
                zero_years_count = 0
                for yr in valid_years:
                    if abs(yr["turnover"]) < 0.0001 and abs(yr["returns"]) < 0.00001:
                        has_dead_year = True
                        zero_years_count += 1
                if has_dead_year:
                    return True
                    
                # C. 零值年份占比过多 (超过 40%)
                if zero_years_count / total_years > 0.40:
                    return True
                    
                # D. 近两年平均 Sharpe 极低 (< 0.10) 或包含 0.0
                recent_years = valid_years[:2]
                recent_sharpes = [yr["sharpe"] for yr in recent_years]
                l2y_sharpe = sum(recent_sharpes) / len(recent_sharpes) if recent_sharpes else 0.0
                if any(abs(s) < 1e-9 for s in recent_sharpes) or l2y_sharpe < 0.10:
                    return True
                    
                # E. 正收益年份占比不足 50%
                pos_years = sum(1 for yr in valid_years if yr["returns"] > 0)
                if pos_years / total_years < 0.50:
                    return True
                    
    return False





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
    expression = extract_alpha_expression(payload) or str(alpha_record.get("expression") or "")
    level = alpha_record.get("alpha_type") or "C"
    failed_checks = extract_failed_checks(check_payload, check_message)
    error_count = len(failed_checks)
    has_check_result = bool(check_payload) or bool(check_message) or bool(check_result)

    if not expression:
        return _skip(alpha_id, name, source_neutralization, expression, level, failed_checks, "missing_expression")

    expression_validation = validate_expression(expression)
    
    # 垃圾因子/高危因子直接跳过并且屏蔽优化
    if is_high_risk_garbage_alpha(alpha_record, check_result):
        return _skip(
            alpha_id,
            name,
            source_neutralization,
            expression,
            level,
            failed_checks,
            "high_risk_garbage_alpha",
            expression_warnings=expression_validation.warnings,
        )

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

    if level not in ACTIONABLE_LEVELS:
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

    status_val = str(alpha_record.get("status") or "").upper()
    has_group = any(op in expression for op in ["group_neutralize", "group_zscore", "group_rank", "group_normalize", "group_scale"])
    has_trade = "trade_when" in expression
    
    alpha_class = alpha_record.get("alpha_class")
    if not alpha_class:
        alpha_class = "Class A"
        if has_group and has_trade:
            alpha_class = "Class C"
        elif has_group:
            alpha_class = "Class B"
        
    is_corr_fail = (status_val == "CORR_FAIL") or any(str(chk.get("name")).upper() in ["SELF_CORRELATION", "PROD_CORRELATION"] for chk in failed_checks)
    
    pre_strategy = alpha_record.get("optimization_strategy")
    if pre_strategy:
        strategy = pre_strategy
        if strategy == "decorrelate":
            if alpha_class == "Class A":
                modes = ["decorrelate", "group", "stable"]
                reason = "Class A: 未消偏特征因子，自相关性过高"
            elif alpha_class == "Class B":
                modes = ["decorrelate", "trade", "stable"]
                reason = "Class B: 中性化风控因子，自相关性过高"
            else:
                strategy = "settings_only"
                modes = []
                reason = "Class C: 满载完成因子，不建议添加算子优化"
        elif strategy == "settings_only":
            modes = []
            reason = f"{alpha_class}: 满载完成因子，不建议添加算子优化"
        else:
            _, modes, raw_reason = choose_strategy(failed_checks, level, check_result)
            reason = f"{alpha_class}: {raw_reason}"
    else:
        if is_corr_fail:
            strategy = "decorrelate"
            if alpha_class == "Class A":
                modes = ["decorrelate", "group", "stable"]
                reason = "Class A: 未消偏特征因子，自相关性过高"
            elif alpha_class == "Class B":
                modes = ["decorrelate", "trade", "stable"]
                reason = "Class B: 中性化风控因子，自相关性过高"
            else:
                strategy = "settings_only"
                modes = []
                reason = "Class C: 满载完成因子，不建议添加算子优化"
        else:
            strategy, modes, raw_reason = choose_strategy(failed_checks, level, check_result)
            reason = f"{alpha_class}: {raw_reason}"
    # 计算确定性得分 (Certainty/Confidence Score)
    confidence_score = 50.0
    sharpe_val = float(alpha_record.get("sharpe") or 0.0)
    fitness_val = float(alpha_record.get("fitness") or 0.0)
    margin_val = float(alpha_record.get("margin") or 0.0)
    
    if sharpe_val >= 1.50:
        confidence_score += 15.0
    elif sharpe_val >= 1.25:
        confidence_score += 5.0
        
    if fitness_val >= 1.50:
        confidence_score += 10.0
        
    if margin_val >= 0.0020:
        confidence_score += 10.0
        
    for chk in failed_checks:
        chk_name = str(chk.get("name")).upper()
        if chk_name in ["SELF_CORRELATION", "PROD_CORRELATION"]:
            prod_corr = float(alpha_record.get("prod_corr") or 0.0)
            if prod_corr > 0.85:
                confidence_score -= 25.0
            else:
                confidence_score -= 10.0
        elif chk_name == "PASTEURIZATION":
            confidence_score += 10.0  # 极易通过 rank 拯救
        elif chk_name == "HIGH_TURNOVER":
            confidence_score -= 10.0
        elif chk_name in ["LOW_SHARPE", "LOW_FITNESS"]:
            confidence_score -= 15.0
            
    confidence_score = max(0.0, min(100.0, confidence_score))

    # 映射物理与经济学优化建议 (Physical & Economic Salvage Meanings)
    economic_suggestion = ""
    if strategy == "decorrelate":
        economic_suggestion = "剥离行业风格共性。从经济学来看，该因子暴露了行业风格 Beta，利用 group_neutralize 强制进行板块中性化，可将持仓完全对称于各子板块，从而过滤宏观冲击以提取特异性超额收益 (Pure Idiosyncratic Alpha)。"
    elif strategy == "improve_performance":
        economic_suggestion = "资产估值截面比较。从微观结构来看，因子的绝对强度较弱。通过 ts_rank 时序/截面均匀分位化，可抹平异常绝对值暴露，使策略能够更稳健地基于全市场进行相对强弱比较，显著提升夏普与拟合度。"
    elif strategy == "adjust_turnover":
        economic_suggestion = "流动性平滑与信息显著度门槛。从微观结构来看，频繁的调仓产生高昂的交易滑点与冲击成本 (Slippage)。利用 trade_when 算子仅在波动率偏离显著时换仓，可锁定核心信号，实现换手率大幅骤减。"
    elif strategy == "improve_margin":
        economic_suggestion = "交易滑点摩擦平摊。从执行层面看，每笔交易的盈利空间无法抵抗交易摩擦。在最外层叠加 ts_decay_linear 时序线性衰减，能将单日突发信号在时序上进行平滑平摊，从而平滑持仓并大幅改善成交 Margin。"
    elif strategy == "settings_only":
        economic_suggestion = "已达满载极限，不宜继续叠加算子。当前因子表达式的算子数量过多，继续添加算子易导致过拟合。建议在 Settings 层面调参，利用 Universe 或 Decay 进行网格扫频优化。"
    else:
        economic_suggestion = "基础优化诊断中，建议结合 Settings 网格参数扫频来降低 Turnover 并改善绩效。"

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
        alpha_class=alpha_class,
        confidence_score=confidence_score,
        economic_suggestion=economic_suggestion,
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

    if level in {"S", "A"}:
        return "stabilize", ["stable"], "premium_metric_candidate"
    if level == "B":
        return "improve_performance", ["template", "stable"], "standard_metric_candidate"
    return "improve_margin", ["stable", "power"], "marginal_metric_candidate"


def list_optimization_plans(limit: int = 200) -> list[OptimizationPlan]:
    limit = max(1, min(int(limit), 5000))
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT
                a.alpha_id,
                a.name,
                a.alpha_type,
                a.sharpe,
                a.fitness,
                a.margin,
                a.returns,
                a.drawdown,
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
    has_group = any(op in expression for op in ["group_neutralize", "group_zscore", "group_rank", "group_normalize", "group_scale"])
    has_trade = "trade_when" in expression
    alpha_class = "Class A"
    if has_group and has_trade:
        alpha_class = "Class C"
    elif has_group:
        alpha_class = "Class B"

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
        alpha_class=alpha_class,
        confidence_score=0.0,
        economic_suggestion="",
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

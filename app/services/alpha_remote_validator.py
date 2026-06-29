"""
alpha_remote_validator.py
--------------------------
A 级 / S 级因子远端二次验证服务。

触发条件：因子本地评级为 Grade A 或 Grade S。
验证内容：
  1. 拉取 WQ 平台年度统计 (yearly-stats) — 判断厂字/OS崩塌
  2. 拉取逐日 PNL (recordsets/pnl) — 检测末端平坦（可选，较慢）
  3. 综合打分，输出 grade_adjustment: 'D' | 'C' | 'keep'

结果字段：
  - is_valid          : bool
  - confidence        : float (0~1)
  - grade_adjustment  : 'D' | 'C' | 'keep'
  - issues            : list[str]  各项不合格标签
  - l2y_sharpe        : float      近2年均值夏普
  - flat_pnl_detected : bool       PNL末端厂字检测结果
"""
from __future__ import annotations

import logging
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# 常量
# --------------------------------------------------------------------------- #
WQ_API_BASE = "https://api.worldquantbrain.com"

# 厂字 PNL 末端连续相同值阈值（交易日数）
FLAT_PNL_THRESHOLD = 250

# 综合评分阈值
CONFIDENCE_THRESHOLD_D = 0.50   # 低于此值 → 降级 D
CONFIDENCE_THRESHOLD_C = 0.70   # 低于此值 → 降级 C（否则 keep）


# --------------------------------------------------------------------------- #
# 网络工具
# --------------------------------------------------------------------------- #

def _safe_get(session: requests.Session, url: str, timeout: int = 30) -> dict[str, Any] | None:
    """发送 GET 请求，失败时返回 None 而非抛出异常；自动处理 Retry-After。"""
    for attempt in range(3):
        try:
            resp = session.get(url, timeout=timeout)
            retry_after = resp.headers.get("Retry-After")
            if retry_after:
                wait = float(retry_after)
                logger.warning(f"[RemoteValidator] Retry-After {wait}s for {url}")
                time.sleep(wait)
                continue
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code in (404, 403):
                logger.warning(f"[RemoteValidator] {resp.status_code} for {url}")
                return None
            logger.warning(f"[RemoteValidator] HTTP {resp.status_code} for {url}, attempt {attempt+1}")
        except Exception as exc:
            logger.error(f"[RemoteValidator] Request error {url}: {exc}")
        time.sleep(2 ** attempt)
    return None


def _parse_schema_records(data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    将 WQ API 返回的 {schema:{properties:[{name}]}, records:[[...],...]} 结构
    转换为 [{col_name: value, ...}, ...] 列表。
    """
    schema = data.get("schema", {})
    properties = schema.get("properties", [])
    col_names = [p["name"] for p in properties if isinstance(p, dict) and "name" in p]
    records = data.get("records", [])
    result = []
    for row in records:
        if isinstance(row, (list, tuple)) and len(row) >= len(col_names):
            result.append({col_names[i]: row[i] for i in range(len(col_names))})
        elif isinstance(row, dict):
            result.append(row)
    return result


# --------------------------------------------------------------------------- #
# 数据拉取
# --------------------------------------------------------------------------- #

def fetch_yearly_stats(session: requests.Session, alpha_id: str) -> list[dict[str, Any]]:
    """
    拉取年度统计，返回解析后的记录列表。
    每条记录包含 year, sharpe, returns, drawdown, turnover 等字段（视平台返回而定）。
    """
    url = f"{WQ_API_BASE}/alphas/{alpha_id}/recordsets/yearly-stats"
    data = _safe_get(session, url)
    if not data:
        return []
    return _parse_schema_records(data)


def fetch_pnl_series(session: requests.Session, alpha_id: str) -> list[Any]:
    """
    拉取逐日 PNL，返回 pnl 数值序列（仅 pnl 列）。
    若无法获取则返回空列表。
    """
    url = f"{WQ_API_BASE}/alphas/{alpha_id}/recordsets/pnl"
    data = _safe_get(session, url)
    if not data:
        return []
    records = _parse_schema_records(data)
    # 找 pnl 列（通常名为 'pnl' 或 alpha_id 本身）
    pnl_col = None
    for rec in records[:1]:
        for k in rec.keys():
            if k.lower() == "pnl" or k == alpha_id:
                pnl_col = k
                break
    if pnl_col is None and records:
        # 取第二列（第一列通常是 date）
        keys = list(records[0].keys())
        pnl_col = keys[1] if len(keys) > 1 else keys[0]
    return [rec.get(pnl_col) for rec in records if pnl_col and pnl_col in rec]


# --------------------------------------------------------------------------- #
# 厂字检测
# --------------------------------------------------------------------------- #

def detect_flat_pnl(pnl_values: list[Any], threshold: int = FLAT_PNL_THRESHOLD) -> bool:
    """
    检测 PNL 序列中的"厂字"特征（停牌/无收益/过拟合死因子）。
    返回 True 表示检测到异常厂字特征，应该被剔除/隐藏。
    """
    if not pnl_values:
        return True  # 无数据视为不合法
        
    valid_values = [v for v in pnl_values if v is not None]
    if not valid_values:
        return True
        
    # 1. 全零检测
    if all(v == 0 for v in valid_values):
        return True
        
    # 2. 历史跨度检查：如果总数据交易日数不足 3 年 (756天)，视为数据严重不足
    if len(pnl_values) < 756:
        return True

    # 3. 末端绝对静止检测：检查最后 threshold 个交易日是否完全等值
    if len(pnl_values) >= threshold:
        tail = pnl_values[-threshold:]
        tail_valid = [v for v in tail if v is not None]
        if len(tail_valid) >= threshold // 2:
            last_val = tail_valid[-1]
            if all(v == last_val for v in tail_valid):
                return True

    # 4. 中途非零冻结检测 & 长周期零值断带检测
    current_non_zero_streak = 0
    current_non_zero_val = None
    current_zero_streak = 0
    
    for v in pnl_values:
        if v is None:
            # 遇到 None，重置连续非零值计数
            current_non_zero_streak = 0
            current_non_zero_val = None
            continue
            
        if v != 0:
            current_zero_streak = 0
            if v == current_non_zero_val:
                current_non_zero_streak += 1
            else:
                current_non_zero_val = v
                current_non_zero_streak = 1
                
            if current_non_zero_streak >= threshold:
                return True
        else:
            # v == 0
            current_non_zero_streak = 0
            current_non_zero_val = None
            current_zero_streak += 1
            if current_zero_streak >= 756:  # 连续 3 年 (756交易日) 零值
                return True
                
    return False


# --------------------------------------------------------------------------- #
# 综合评分
# --------------------------------------------------------------------------- #

def _to_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def compute_remote_validation_score(
    yearly_stats: list[dict[str, Any]],
    is_sharpe: float = 0.0,
    is_fitness: float = 0.0,
) -> dict[str, Any]:
    """
    根据年度统计数据计算远端验证综合评分。

    Args:
        yearly_stats : 年度统计记录列表，每项含 year/sharpe/returns/turnover/drawdown
        is_sharpe    : 本地 IS 夏普（用于 L2Y vs IS 对比）
        is_fitness   : 本地 IS 适应度（用于过拟合检测）

    Returns:
        {
            'is_valid'        : bool,
            'confidence'      : float,
            'grade_adjustment': 'D' | 'C' | 'keep',
            'issues'          : list[str],
            'l2y_sharpe'      : float,
        }
    """
    total_years = len(yearly_stats)
    issues: list[str] = []
    score = 100.0

    # ── 基础：年份数量不足 ──────────────────────────────────────────────── #
    if total_years < 3:
        return {
            "is_valid": False,
            "confidence": 0.0,
            "grade_adjustment": "D",
            "issues": ["insufficient_years"],
            "l2y_sharpe": 0.0,
        }

    # ── 按年份降序排列 ──────────────────────────────────────────────────── #
    sorted_stats = sorted(yearly_stats, key=lambda r: _to_float(r.get("year", 0)), reverse=True)

    sharpe_list = [_to_float(r.get("sharpe")) for r in sorted_stats]
    returns_list = [_to_float(r.get("returns")) for r in sorted_stats]
    turnover_list = [_to_float(r.get("turnover")) for r in sorted_stats]

    l2y_sharpe = sum(sharpe_list[:2]) / 2 if len(sharpe_list) >= 2 else sharpe_list[0] if sharpe_list else 0.0

    # ── 厂字检测 1：单年零换手 + 零收益 ─────────────────────────────────── #
    has_dead_year = False
    for i in range(total_years):
        if abs(turnover_list[i]) < 0.0001 and abs(returns_list[i]) < 0.00001:
            has_dead_year = True
            break
    if has_dead_year:
        issues.append("DEAD_ALPHA_RISK")
        score -= 40

    # ── 厂字检测 2：零值年份占比过多 (超过 40%) ─────────────────────────── #
    zero_years = sum(
        1 for i in range(total_years)
        if abs(turnover_list[i]) < 0.0001 and abs(returns_list[i]) < 0.00001
    )
    if zero_years / total_years > 0.40:
        if "DEAD_ALPHA_RISK" not in issues:
            issues.append("DEAD_ALPHA_RISK")
        score -= 20

    # ── 近2年有 Sharpe == 0 或整体 L2Y Sharpe 极低 (< 0.10) ───────────── #
    recent_sharpes = sharpe_list[:2]
    if any(abs(s) < 1e-9 for s in recent_sharpes) or l2y_sharpe < 0.10:
        issues.append("DEAD_ALPHA_RISK_RECENT")
        score -= 30

    # ── 负收益年份占比超过 35% ───────────────────────────────────────────── #
    neg_years = sum(1 for r in returns_list if r < 0)
    neg_ratio = neg_years / total_years
    if neg_ratio > 0.35:
        issues.append("high_negative_years")
        score -= 25
    elif neg_ratio > 0.10:
        issues.append("moderate_negative_years")
        score -= 10

    # ── 正收益年份占比不足 50% ───────────────────────────────────────────── #
    pos_years = sum(1 for r in returns_list if r > 0)
    if pos_years / total_years < 0.50:
        issues.append("unstable_returns")
        score -= 20

    # ── L2Y Sharpe vs IS Sharpe 对比 ─────────────────────────────────────── #
    if is_sharpe > 0 and l2y_sharpe < is_sharpe * 0.50:
        issues.append("os_decay_warning")
        score -= 20
    if l2y_sharpe < 0.50:
        issues.append("l2y_sharpe_too_low")
        score -= 15
    elif l2y_sharpe < 1.00:
        issues.append("l2y_sharpe_weak")
        score -= 5

    # ── 过拟合预警：fitness >> 2 × sharpe ────────────────────────────────── #
    if is_sharpe > 0 and is_fitness > 2 * is_sharpe:
        issues.append("overfitting_warning")
        score -= 15

    # ── 最大回撤 ─────────────────────────────────────────────────────────── #
    drawdowns = [_to_float(r.get("drawdown")) for r in sorted_stats]
    if drawdowns and max(abs(d) for d in drawdowns) > 0.15:
        issues.append("high_drawdown")
        score -= 5

    # ── 综合评分 → 档位 ──────────────────────────────────────────────────── #
    confidence = max(0.0, min(1.0, score / 100.0))
    dead_tags = {"DEAD_ALPHA_RISK", "DEAD_ALPHA_RISK_RECENT"}
    if confidence < CONFIDENCE_THRESHOLD_D or dead_tags & set(issues):
        grade_adjustment = "D"
    elif confidence < CONFIDENCE_THRESHOLD_C:
        grade_adjustment = "C"
    else:
        grade_adjustment = "keep"

    return {
        "is_valid": grade_adjustment == "keep",
        "confidence": round(confidence, 4),
        "grade_adjustment": grade_adjustment,
        "issues": issues,
        "l2y_sharpe": round(l2y_sharpe, 4),
    }


# --------------------------------------------------------------------------- #
# 完整流程入口
# --------------------------------------------------------------------------- #

def run_remote_validation(
    session: requests.Session,
    alpha_id: str,
    is_sharpe: float = 0.0,
    is_fitness: float = 0.0,
    check_pnl: bool = False,
) -> dict[str, Any]:
    """
    对单个 alpha 执行完整远端验证。

    Args:
        session    : 已登录的 WQ requests.Session
        alpha_id   : Alpha / Simulation ID
        is_sharpe  : 本地 IS Sharpe 值（用于 L2Y 对比）
        is_fitness : 本地 IS Fitness 值（用于过拟合检测）
        check_pnl  : 是否额外拉取逐日 PNL 进行末端厂字检测（较慢，默认 False）

    Returns:
        {
            'alpha_id'         : str,
            'is_valid'         : bool,
            'confidence'       : float,
            'grade_adjustment' : 'D' | 'C' | 'keep',
            'issues'           : list[str],
            'l2y_sharpe'       : float,
            'flat_pnl_detected': bool,
            'total_years'      : int,
            'error'            : str | None,
        }
    """
    base = {
        "alpha_id": alpha_id,
        "is_valid": False,
        "confidence": 0.0,
        "grade_adjustment": "C",
        "issues": [],
        "l2y_sharpe": 0.0,
        "flat_pnl_detected": False,
        "total_years": 0,
        "error": None,
    }

    # Step 1: 拉取年度统计
    try:
        yearly_stats = fetch_yearly_stats(session, alpha_id)
    except Exception as exc:
        base["error"] = f"yearly_stats fetch failed: {exc}"
        return base

    if not yearly_stats:
        base["error"] = "No yearly-stats returned from platform"
        base["issues"] = ["no_yearly_data"]
        return base

    base["total_years"] = len(yearly_stats)

    # Step 2: 综合评分
    score_result = compute_remote_validation_score(yearly_stats, is_sharpe, is_fitness)
    base.update(score_result)

    # Step 3: 可选 PNL 末端厂字检测
    if check_pnl:
        try:
            pnl_values = fetch_pnl_series(session, alpha_id)
            base["flat_pnl_detected"] = detect_flat_pnl(pnl_values)
            if base["flat_pnl_detected"]:
                if "flat_pnl" not in base["issues"]:
                    base["issues"].append("flat_pnl")
                # 若检测到端点厂字，直接降级 D（覆盖）
                base["grade_adjustment"] = "D"
                base["is_valid"] = False
                base["confidence"] = min(base["confidence"], 0.3)
        except Exception as exc:
            logger.warning(f"[RemoteValidator] PNL check failed for {alpha_id}: {exc}")

    return base

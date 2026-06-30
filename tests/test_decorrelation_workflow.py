import json
from app.services.template_iteration import grade_candidate_result
from app.services.optimization_planner import is_high_risk_garbage_alpha, build_optimization_plan
from app.services.alpha_enhancement import generate_variants_for_plan

def test_grade_candidate_result_with_correlation():
    # 1. 自相关超标但指标优异 -> 应评定为 C 级 (可优化)
    res_corr = grade_candidate_result({
        "sharpe": 1.6,
        "fitness": 1.2,
        "margin": 0.002,
        "turnover": 0.3,
        "self_corr": 0.75,  # 超出 0.70
        "prod_corr": 0.3,
        "failed_checks": 0,
        "status": "PASS",
        "payload": {}
    })
    assert res_corr["grade"] == "C"
    assert "SC_RISK" in res_corr["reasons"]
    
    # 2. PnL 覆盖率过低 -> 应判定为 DEAD_ALPHA_RISK 并评定为 D 级 (垃圾因子)
    res_dead = grade_candidate_result({
        "sharpe": 1.6,
        "fitness": 1.2,
        "margin": 0.002,
        "turnover": 0.3,
        "self_corr": 0.1,
        "prod_corr": 0.1,
        "failed_checks": 0,
        "status": "PASS",
        "payload": {
            "pnl_coverage_rate": 0.45  # 低于 60%
        }
    })
    assert res_dead["grade"] == "D"
    assert "DEAD_ALPHA_RISK" in res_dead["reasons"]


def test_is_high_risk_garbage_alpha_rules():
    # 1. 正常的 FAIL 因子是垃圾因子
    record_fail = {"alpha_type": "C", "status": "FAIL"}
    assert is_high_risk_garbage_alpha(record_fail, "FAIL") is True
    
    # 2. 自相关超标的 CORR_FAIL 状态不是垃圾因子，不会被隐藏
    record_corr = {"alpha_type": "C", "status": "CORR_FAIL"}
    assert is_high_risk_garbage_alpha(record_corr, "") is False
    
    # 3. 覆盖率过低的因子是垃圾因子
    record_dead = {
        "alpha_type": "C",
        "status": "PASS",
        "payload": json.dumps({"pnl_coverage_rate": 0.50})
    }
    assert is_high_risk_garbage_alpha(record_dead, "") is True


def test_build_optimization_plan_classification():
    # 1. Class A 因子 (无 group_，无 trade_when)
    record_a = {
        "alpha_id": "A1",
        "expression": "ts_delta(close, 5)",
        "alpha_type": "C",
        "status": "CORR_FAIL",
        "sharpe": 1.5,
        "fitness": 1.1,
        "margin": 0.001
    }
    plan_a = build_optimization_plan(record_a, check_result="FAIL")
    assert plan_a.strategy == "decorrelate"
    assert "Class A" in plan_a.reason
    assert "group" in plan_a.suggested_modes
    
    # 2. Class B 因子 (有 group_，无 trade_when)
    record_b = {
        "alpha_id": "B1",
        "expression": "group_neutralize(ts_delta(close, 5), subindustry)",
        "alpha_type": "C",
        "status": "CORR_FAIL",
        "sharpe": 1.5,
        "fitness": 1.1,
        "margin": 0.001
    }
    plan_b = build_optimization_plan(record_b, check_result="FAIL")
    assert plan_b.strategy == "decorrelate"
    assert "Class B" in plan_b.reason
    assert "trade" in plan_b.suggested_modes
    
    # 3. Class C 因子 (有 group_，有 trade_when)
    record_c = {
        "alpha_id": "C1",
        "expression": "trade_when(volume > 10, group_neutralize(close, subindustry), -1)",
        "alpha_type": "C",
        "status": "CORR_FAIL",
        "sharpe": 1.5,
        "fitness": 1.1,
        "margin": 0.001
    }
    plan_c = build_optimization_plan(record_c, check_result="FAIL")
    assert plan_c.strategy == "settings_only"
    assert "Class C" in plan_c.reason
    assert len(plan_c.suggested_modes) == 0


def test_generate_decorrelate_variants():
    record = {
        "alpha_id": "VAR1",
        "expression": "close",
        "alpha_type": "C",
        "status": "CORR_FAIL",
        "sharpe": 1.5,
        "fitness": 1.1,
        "margin": 0.001
    }
    plan = build_optimization_plan(record, check_result="FAIL")
    variants = generate_variants_for_plan(plan, max_variants=10)
    expressions = [v.expression for v in variants]
    
    # 应包含 group_neutralize 改写以降低自相关性
    assert any("group_neutralize" in exp for exp in expressions)
    # 应包含 ts_decay_linear 改写
    assert any("ts_decay_linear" in exp for exp in expressions)

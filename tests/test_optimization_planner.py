import unittest

from app.services.optimization_planner import (
    build_optimization_plan,
    classify_alpha_level,
    extract_alpha_expression,
    extract_alpha_neutralization,
    extract_failed_checks,
)


class OptimizationPlannerTests(unittest.TestCase):
    def test_extract_failed_checks_reads_check_payload(self):
        payload = {
            "is": {
                "checks": [
                    {"name": "LOW_SHARPE", "result": "PASS"},
                    {"name": "SELF_CORRELATION", "result": "FAIL", "value": 0.73, "limit": 0.7},
                    {"name": "PROD_CORRELATION", "status": "ERROR"},
                ]
            }
        }

        failed = extract_failed_checks(payload)

        self.assertEqual([item["name"] for item in failed], ["SELF_CORRELATION", "PROD_CORRELATION"])

    def test_self_correlation_uses_decorrelation_strategy(self):
        plan = build_optimization_plan(
            {
                "alpha_id": "abc123",
                "fitness": 1.8,
                "margin": 0.0012,
                "payload": {"regular": {"code": "rank(close)"}},
            },
            check_payload={
                "is": {
                    "checks": [
                        {"name": "SELF_CORRELATION", "result": "FAIL", "value": 0.72, "limit": 0.7}
                    ]
                }
            },
        )

        self.assertTrue(plan.should_optimize)
        self.assertEqual(plan.strategy, "decorrelate")
        self.assertEqual(plan.suggested_modes, ["group", "trade", "stable"])

    def test_two_or_more_failed_checks_skip_automatic_optimization(self):
        plan = build_optimization_plan(
            {
                "alpha_id": "abc123",
                "fitness": 1.8,
                "margin": 0.0012,
                "payload": {"regular": {"code": "rank(close)"}},
            },
            check_payload={
                "is": {
                    "checks": [
                        {"name": "SELF_CORRELATION", "result": "FAIL"},
                        {"name": "LOW_SHARPE", "result": "ERROR"},
                    ]
                }
            },
        )

        self.assertFalse(plan.should_optimize)
        self.assertEqual(plan.skip_reason, "too_many_failed_checks")

    def test_only_marginal_standard_premium_are_metric_candidates(self):
        self.assertEqual(classify_alpha_level(1.0, 0.0005), "marginal")
        self.assertEqual(classify_alpha_level(1.5, 0.0010), "standard")
        self.assertEqual(classify_alpha_level(2.5, 0.0030), "premium")
        self.assertEqual(classify_alpha_level(0.9, 0.0005), "substandard")

    def test_substandard_without_check_result_is_not_optimized(self):
        plan = build_optimization_plan(
            {
                "alpha_id": "abc123",
                "fitness": 0.9,
                "margin": 0.0005,
                "payload": {"regular": {"code": "rank(close)"}},
            }
        )

        self.assertFalse(plan.should_optimize)
        self.assertEqual(plan.skip_reason, "substandard")

    def test_extract_alpha_expression_supports_common_payload_shapes(self):
        self.assertEqual(extract_alpha_expression({"regular": "rank(close)"}), "rank(close)")
        self.assertEqual(extract_alpha_expression({"regular": {"code": "rank(close)"}}), "rank(close)")
        self.assertEqual(
            extract_alpha_expression({"raw_payload": {"regular": {"code": "ts_rank(close, 20)"}}}),
            "ts_rank(close, 20)",
        )

    def test_extract_alpha_neutralization_reads_settings(self):
        self.assertEqual(
            extract_alpha_neutralization({"settings": {"neutralization": "INDUSTRY"}}),
            "INDUSTRY",
        )

    def test_plan_serializes_for_api_response(self):
        plan = build_optimization_plan(
            {
                "alpha_id": "abc123",
                "name": "pv63 margin candidate",
                "fitness": 2.8,
                "margin": 0.0035,
                "payload": {"regular": {"code": "rank(close)"}},
            }
        )

        data = plan.to_dict()

        self.assertEqual(data["alpha_id"], "abc123")
        self.assertEqual(data["name"], "pv63 margin candidate")
        self.assertEqual(data["level"], "premium")
        self.assertEqual(data["suggested_modes"], ["stable"])
        self.assertTrue(data["should_optimize"])
        self.assertTrue(data["expression_valid"])

    def test_invalid_expression_is_skipped_before_optimization(self):
        plan = build_optimization_plan(
            {
                "alpha_id": "abc123",
                "fitness": 2.8,
                "margin": 0.0035,
                "payload": {"regular": {"code": "rank(ts_mean(close, 20)"}},
            }
        )

        self.assertFalse(plan.should_optimize)
        self.assertEqual(plan.skip_reason, "invalid_expression")
        self.assertFalse(plan.expression_valid)


if __name__ == "__main__":
    unittest.main()

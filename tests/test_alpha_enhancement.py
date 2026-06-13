import unittest

from app.services.alpha_enhancement import generate_variants_for_plan
from app.services.optimization_planner import build_optimization_plan


class AlphaEnhancementTests(unittest.TestCase):
    def test_generate_variants_for_self_correlation_plan(self):
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

        variants = generate_variants_for_plan(plan, max_variants=20)
        modes = {variant.mode for variant in variants}

        self.assertIn("group", modes)
        self.assertIn("trade", modes)
        self.assertIn("stable", modes)
        self.assertTrue(all(variant.validation["is_valid"] for variant in variants))

    def test_invalid_or_skipped_plan_has_no_variants(self):
        plan = build_optimization_plan(
            {
                "alpha_id": "abc123",
                "fitness": 0.5,
                "margin": 0.0,
                "payload": {"regular": {"code": "rank(close)"}},
            }
        )

        self.assertEqual(generate_variants_for_plan(plan), [])

    def test_variant_generation_deduplicates_expressions(self):
        plan = build_optimization_plan(
            {
                "alpha_id": "abc123",
                "fitness": 1.5,
                "margin": 0.001,
                "payload": {"regular": {"code": "rank(close)"}},
            }
        )

        variants = generate_variants_for_plan(plan, max_variants=50)
        expressions = [variant.expression for variant in variants]

        self.assertEqual(len(expressions), len(set(expressions)))


if __name__ == "__main__":
    unittest.main()

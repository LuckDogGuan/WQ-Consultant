import unittest

from app.services.alpha_rating import (
    build_alpha_rating,
    classify_metric_level,
    count_failed_checks,
)


class AlphaRatingTests(unittest.TestCase):
    def test_uses_alpha_metrics_when_check_payload_has_no_metric_fields(self):
        alpha_record = {
            "alpha_id": "rKWbp7jm",
            "alpha_type": "MARGINAL",
            "fitness": 1.2,
            "margin": 0.0006,
            "payload": {"is": {"checks": []}},
        }
        check_result = {
            "result": "PASS",
            "payload": {"is": {"checks": [{"name": "LOW_SHARPE", "result": "PASS"}]}},
        }

        rating = build_alpha_rating(alpha_record, check_result)

        self.assertEqual(rating["metric_class"], "marginal")
        self.assertEqual(rating["submission_class"], "marginal")
        self.assertEqual(rating["alpha_level"], rating["submission_label"])
        self.assertEqual(rating["level_class"], rating["submission_class"])

    def test_failed_latest_check_only_changes_submission_level(self):
        alpha_record = {
            "alpha_id": "alpha_fail",
            "alpha_type": "PPA",
            "fitness": 2.7,
            "margin": 0.0035,
            "payload": {"is": {"checks": []}},
        }
        check_result = {
            "result": "PASS",
            "payload": {"is": {"checks": [{"name": "SELF_CORRELATION", "result": "FAIL"}]}},
        }

        rating = build_alpha_rating(alpha_record, check_result)

        self.assertEqual(rating["metric_class"], "premium")
        self.assertEqual(rating["submission_class"], "substandard")
        self.assertEqual(rating["failed_check_count"], 1)

    def test_adds_extended_quality_and_type_labels(self):
        self.assertEqual(classify_metric_level(3.0, 0.005), "elite")
        self.assertEqual(classify_metric_level(2.5, 0.003), "premium")

        labels = {
            t: build_alpha_rating({"alpha_type": t})["correlation_label"]
            for t in ["PPA", "RA", "ATOM", "MARGINAL", "SKIP", ""]
        }

        self.assertEqual(labels["PPA"], "PPA 优秀因子")
        self.assertEqual(labels["RA"], "RA 优秀因子")
        self.assertEqual(labels["ATOM"], "ATOM 优秀因子")
        self.assertEqual(labels["MARGINAL"], "边际相关性因子")
        self.assertEqual(labels["SKIP"], "跳过因子")
        self.assertEqual(labels[""], "未分类")

    def test_count_failed_checks_accepts_status_variants(self):
        payload = {
            "is": {
                "checks": [
                    {"result": "PASS"},
                    {"status": "failed"},
                    {"result": "ERROR"},
                ]
            }
        }

        self.assertEqual(count_failed_checks(payload), 2)


if __name__ == "__main__":
    unittest.main()

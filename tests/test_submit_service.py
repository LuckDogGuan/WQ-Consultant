import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class SubmitServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "gui.db"
        patchers = [
            patch("app.paths.DB_PATH", self.db_path),
            patch("app.storage.DB_PATH", self.db_path),
        ]
        for patcher in patchers:
            self.addCleanup(patcher.stop)
            patcher.start()

        from app.storage import init_db

        init_db()

    def tearDown(self):
        self.tmp.cleanup()

    def test_parse_alpha_ids_accepts_lines_commas_and_deduplicates(self):
        from app.services.submit_service import parse_alpha_ids

        self.assertEqual(parse_alpha_ids("a1\na2, a3\n a2 "), ["a1", "a2", "a3"])

    def test_list_local_submit_candidates_requires_pass_and_keeps_priority_types(self):
        from app.services.submit_service import list_local_submit_candidates
        from app.storage import add_check_result, upsert_alpha

        upsert_alpha({"alpha_id": "ppa1", "alpha_type": "PPA", "status": "CHECKED_PASS", "sharpe": 1.8, "fitness": 1.1})
        upsert_alpha({"alpha_id": "ra1", "alpha_type": "RA", "status": "CHECKED_PASS", "sharpe": 1.7, "fitness": 1.0})
        upsert_alpha({"alpha_id": "plain1", "alpha_type": "", "status": "CHECKED_PASS", "sharpe": 2.1, "fitness": 1.4})
        upsert_alpha({"alpha_id": "skip_pass", "alpha_type": "SKIP", "status": "CHECKED_PASS", "sharpe": 1.9, "fitness": 1.3})
        upsert_alpha({"alpha_id": "skip1", "alpha_type": "SKIP", "status": "CHECKED_PASS", "sharpe": 3.0, "fitness": 2.0})
        upsert_alpha({"alpha_id": "fail1", "alpha_type": "PPA", "status": "CHECKED_FAIL", "sharpe": 2.0, "fitness": 1.1})
        upsert_alpha({"alpha_id": "done1", "alpha_type": "ATOM", "status": "SUBMITTED", "sharpe": 2.5, "fitness": 1.2})
        add_check_result("ppa1", "PASS", 0.2, "", source="test", payload={})
        add_check_result("ra1", "PASS", 0.3, "", source="test", payload={})
        add_check_result("plain1", "PASS", 0.4, "", source="test", payload={})
        add_check_result("skip_pass", "PASS", 0.68, "", source="test", payload={})
        add_check_result("skip1", "PASS", 0.1, "", source="test", payload={})
        add_check_result("fail1", "FAIL", 0.8, "", source="test", payload={})
        add_check_result("done1", "PASS", 0.1, "", source="test", payload={})

        candidates = list_local_submit_candidates(limit=10)

        self.assertEqual([item["alpha_id"] for item in candidates[:2]], ["ppa1", "ra1"])
        self.assertEqual(
            {item["alpha_id"] for item in candidates[2:]},
            {"plain1", "skip_pass", "skip1"},
        )
        self.assertEqual(candidates[0]["source"], "alpha_records")
        self.assertEqual(candidates[0]["candidate_tier"], "priority")
        self.assertEqual(candidates[2]["candidate_tier"], "checked_pass")

    def test_daily_inspection_defaults_have_highest_scheduler_priority(self):
        from app.services.daily_inspection_service import DAILY_INSPECTION_PRIORITY, build_daily_inspection_params

        params = build_daily_inspection_params()

        self.assertEqual(DAILY_INSPECTION_PRIORITY, 0)
        self.assertEqual(params["source"], "daily_inspection")
        self.assertIn("correlation", params["stages"])
        self.assertIn("check_submission", params["stages"])


if __name__ == "__main__":
    unittest.main()

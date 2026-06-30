import json
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import app.main as main
from app.storage import connect, get_settings


class BacktestProfilePageTests(unittest.TestCase):
    def setUp(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"

    def tearDown(self):
        main.app.dependency_overrides.clear()

    def test_backtest_page_renders_profile_controls(self):
        client = TestClient(main.app)
        with patch("app.main.get_cached_scopes", return_value={"USA": {}, "ASI": {}}):
            response = client.get("/backtest")

        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")
        self.assertIn("王哥严格版", html)
        self.assertIn("顾问等级", html)
        self.assertIn("槽位与线程", html)
        self.assertIn("运行效果统计", html)
        self.assertIn("USA, ASI", html)
        self.assertIn("fo_backtest_children", html)
        self.assertNotIn('name="regions"', html)
        self.assertNotIn("usa_fo_children", html)

    def test_backtest_post_stores_strict_profile_and_shared_stage_config(self):
        client = TestClient(main.app)
        payload = {
            "dataset_ids": "fundamental6\nanalyst4",
            "advisor_level": "gold",
            "run_fo": "true",
            "run_so": "true",
            "run_th": "true",
            "fo_corr_enable": "true",
            "fo_backtest_children": "4",
            "fo_backtest_threads": "2",
            "so_backtest_children": "3",
            "so_backtest_threads": "1",
        }

        with patch("app.main.get_cached_scopes", return_value={"USA": {}, "ASI": {}}), patch("app.main.JobRunner") as runner_cls:
            response = client.post("/api/jobs/backtest", data=payload, follow_redirects=False)

        self.assertEqual(response.status_code, 303)
        runner_cls.return_value.start_job.assert_called_once()
        _, kind, params = runner_cls.return_value.start_job.call_args.args
        self.assertEqual(kind, "backtest")
        self.assertEqual(params["profile"], "wang_strict")
        self.assertEqual(params["advisor_level"], "gold")
        self.assertEqual(params["regions"], ["USA", "ASI"])
        self.assertEqual(params["allowed_dataset_ids"], ["fundamental6", "analyst4"])
        self.assertEqual(params["region_stage_config"]["USA"]["FO"]["children"], 4)
        self.assertEqual(params["region_stage_config"]["USA"]["FO"]["threads"], 2)
        self.assertEqual(params["region_stage_config"]["ASI"]["SO"]["children"], 3)
        self.assertEqual(params["region_stage_config"]["ASI"]["SO"]["threads"], 1)
        self.assertEqual(params["turnover_hard"], 0.15)
        self.assertTrue(params["retire_grade_d_remote"])

        settings = get_settings()
        self.assertEqual(settings.get("advisor_level"), "gold")
        self.assertEqual(settings.get("fo_backtest_children"), "4")
        self.assertEqual(settings.get("so_backtest_threads"), "1")

        with connect() as conn:
            row = conn.execute("SELECT params FROM jobs WHERE kind = 'backtest' ORDER BY id DESC LIMIT 1").fetchone()
        stored = json.loads(row["params"])
        self.assertEqual(stored["region_stage_config"]["USA"]["FO"]["children"], 4)

    def test_job_summary_counts_run_effectiveness(self):
        client = TestClient(main.app)
        with connect() as conn:
            conn.execute("DELETE FROM alpha_records WHERE source = 'job_777'")
            conn.execute("DELETE FROM jobs WHERE id = 777")
            conn.execute(
                """
                INSERT INTO jobs(id, kind, status, title, params, progress_current, progress_total, message, created_at, updated_at)
                VALUES (777, 'backtest', 'completed', 'summary test', '{}', 2, 2, '', '2026-06-30T10:00:00+00:00', '2026-06-30T10:10:00+00:00')
                """
            )
            conn.execute(
                """
                INSERT INTO alpha_records(alpha_id, alpha_type, sharpe, fitness, status, source, payload, is_garbage, created_at, updated_at)
                VALUES
                    ('summary_s', 'S', 2.1, 1.4, 'CHECKED_PASS', 'job_777', '{}', 0, '2026-06-30T10:01:00+00:00', '2026-06-30T10:02:00+00:00'),
                    ('summary_d', 'D', -0.2, 0.1, 'UNSUBMITTED', 'job_777', '{}', 1, '2026-06-30T10:03:00+00:00', '2026-06-30T10:04:00+00:00')
                """
            )

        response = client.get("/api/jobs/777/summary")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 2)
        self.assertEqual(data["passed"], 1)
        self.assertEqual(data["hidden"], 1)
        self.assertEqual(data["grade_counts"]["S"], 1)
        self.assertEqual(data["grade_counts"]["D"], 1)
        self.assertEqual(data["duration_seconds"], 600)
        self.assertAlmostEqual(data["alphas_per_minute"], 0.2)


if __name__ == "__main__":
    unittest.main()
from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo


class DashboardMetricsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "gui.db"
        path_patcher = patch("app.paths.DB_PATH", self.db_path)
        storage_patcher = patch("app.storage.DB_PATH", self.db_path)
        self.addCleanup(path_patcher.stop)
        self.addCleanup(storage_patcher.stop)
        path_patcher.start()
        storage_patcher.start()

        from app.storage import init_db

        init_db()

    def tearDown(self):
        self.tmp.cleanup()

    def test_backtest_daily_window_resets_at_noon_in_china_time(self):
        from app.services.dashboard_metrics import local_daily_start

        tz = ZoneInfo("Asia/Shanghai")

        before_noon = local_daily_start(datetime(2026, 6, 13, 11, 59, tzinfo=tz), reset_hour=12)
        after_noon = local_daily_start(datetime(2026, 6, 13, 12, 1, tzinfo=tz), reset_hour=12)

        self.assertEqual(before_noon.isoformat(), "2026-06-12T12:00:00+08:00")
        self.assertEqual(after_noon.isoformat(), "2026-06-13T12:00:00+08:00")

    def test_collects_dashboard_quota_and_optimization_counts(self):
        from app.services.dashboard_metrics import get_dashboard_metrics
        from app.storage import add_check_result, connect, update_settings, upsert_alpha

        update_settings(
            {
                "backtest_daily_limit": "100",
                "check_daily_limit": "200",
                "submit_daily_regular_limit": "4",
                "submit_daily_super_limit": "1",
            }
        )
        upsert_alpha(
            {
                "alpha_id": "bt_today",
                "alpha_type": "RA",
                "fitness": 1.2,
                "margin": 0.0006,
                "status": "UNSUBMITTED",
                "source": "job_1",
                "payload": {"regular": {"code": "rank(close)"}},
            }
        )
        upsert_alpha(
            {
                "alpha_id": "bt_old",
                "alpha_type": "RA",
                "fitness": 1.2,
                "margin": 0.0006,
                "status": "UNSUBMITTED",
                "source": "job_2",
                "payload": {"regular": {"code": "rank(volume)"}},
            }
        )
        upsert_alpha(
            {
                "alpha_id": "sub_regular",
                "alpha_type": "RA",
                "fitness": 1.2,
                "margin": 0.0006,
                "status": "SUBMITTED",
                "source": "submitted_cleanup",
                "payload": {"regular": {"code": "rank(open)"}},
            }
        )
        upsert_alpha(
            {
                "alpha_id": "sub_super",
                "alpha_type": "PPA",
                "fitness": 2.6,
                "margin": 0.0031,
                "status": "SUBMITTED",
                "source": "submitted_cleanup",
                "payload": {"regular": {"code": "rank(high)"}},
            }
        )
        upsert_alpha(
            {
                "alpha_id": "sub_old",
                "alpha_type": "PPA",
                "status": "SUBMITTED",
                "source": "submitted_cleanup",
                "payload": {"regular": {"code": "rank(low)"}},
            }
        )
        add_check_result("bt_today", "PASS", 0.1, "today", source="manual", payload={})
        add_check_result("bt_old", "PASS", 0.1, "old", source="manual", payload={})

        with connect() as conn:
            conn.execute("UPDATE alpha_records SET created_at = ?, updated_at = ? WHERE alpha_id = ?", ("2026-06-13T12:30:00+00:00", "2026-06-13T12:30:00+00:00", "bt_today"))
            conn.execute("UPDATE alpha_records SET created_at = ?, updated_at = ? WHERE alpha_id = ?", ("2026-06-12T03:00:00+00:00", "2026-06-12T03:00:00+00:00", "bt_old"))
            conn.execute("UPDATE alpha_records SET updated_at = ? WHERE alpha_id = ?", ("2026-06-13T01:00:00+00:00", "sub_regular"))
            conn.execute("UPDATE alpha_records SET updated_at = ? WHERE alpha_id = ?", ("2026-06-13T02:00:00+00:00", "sub_super"))
            conn.execute("UPDATE alpha_records SET updated_at = ? WHERE alpha_id = ?", ("2026-06-12T02:00:00+00:00", "sub_old"))
            conn.execute("UPDATE check_results SET created_at = ? WHERE message = ?", ("2026-06-13T01:00:00+00:00", "today"))
            conn.execute("UPDATE check_results SET created_at = ? WHERE message = ?", ("2026-06-12T01:00:00+00:00", "old"))

        metrics = get_dashboard_metrics(datetime(2026, 6, 13, 21, 0, tzinfo=ZoneInfo("Asia/Shanghai")))

        self.assertEqual(metrics["backtest_daily_done"], 1)
        self.assertEqual(metrics["backtest_daily_limit"], 100)
        self.assertEqual(metrics["check_daily_done"], 1)
        self.assertEqual(metrics["check_daily_limit"], 200)
        self.assertEqual(metrics["submit_daily_total"], 2)
        self.assertEqual(metrics["submit_daily_regular"], 1)
        self.assertEqual(metrics["submit_daily_super"], 1)
        self.assertEqual(metrics["submit_daily_limit"], 5)
        self.assertGreaterEqual(metrics["optimization_total"], 5)
        self.assertGreaterEqual(metrics["optimization_optimizable"], 2)
        self.assertGreaterEqual(metrics["optimization_min_submit"], 2)


if __name__ == "__main__":
    unittest.main()

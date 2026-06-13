import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class MaintenanceServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "gui.db"
        patcher = patch("app.paths.DB_PATH", self.db_path)
        self.addCleanup(patcher.stop)
        patcher.start()

        storage_patcher = patch("app.storage.DB_PATH", self.db_path)
        self.addCleanup(storage_patcher.stop)
        storage_patcher.start()

        from app.storage import init_db

        init_db()

    def tearDown(self):
        self.tmp.cleanup()

    def test_cleanup_submitted_alpha_keeps_alpha_record_but_removes_candidate_inputs(self):
        from app.services.maintenance_service import cleanup_submitted_alpha_inputs
        from app.storage import add_check_result, connect, upsert_alpha

        upsert_alpha(
            {
                "alpha_id": "abc123",
                "name": "candidate",
                "status": "CHECKED_PASS",
                "source": "corr_check_1",
                "payload": {"regular": {"code": "rank(close)"}},
            }
        )
        add_check_result("abc123", "PASS", 0.12, "", source="recent_submit", payload={"is": {"checks": []}})

        summary = cleanup_submitted_alpha_inputs(["abc123"])

        self.assertEqual(summary["submitted_count"], 1)
        self.assertEqual(summary["updated_alpha_records"], 1)
        self.assertEqual(summary["deleted_check_results"], 1)
        with connect() as conn:
            alpha = conn.execute("SELECT status, source, payload FROM alpha_records WHERE alpha_id = 'abc123'").fetchone()
            checks = conn.execute("SELECT COUNT(*) FROM check_results WHERE alpha_id = 'abc123'").fetchone()[0]

        self.assertEqual(alpha["status"], "SUBMITTED")
        self.assertEqual(alpha["source"], "submitted_cleanup")
        self.assertEqual(checks, 0)
        self.assertEqual(json.loads(alpha["payload"])["submitted_cleanup"], True)

    def test_prune_old_check_results_keeps_latest_per_alpha(self):
        from app.services.maintenance_service import prune_old_check_results
        from app.storage import add_check_result, connect

        add_check_result("abc123", "FAIL", 0.5, "old", source="manual", payload={})
        add_check_result("abc123", "PASS", 0.1, "new", source="manual", payload={})

        deleted = prune_old_check_results()

        self.assertEqual(deleted, 1)
        with connect() as conn:
            rows = conn.execute("SELECT result, message FROM check_results WHERE alpha_id = 'abc123'").fetchall()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["result"], "PASS")
        self.assertEqual(rows[0]["message"], "new")


if __name__ == "__main__":
    unittest.main()

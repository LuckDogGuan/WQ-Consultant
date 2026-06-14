import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

import app.main as main
import app.storage as storage


class CheckAlphaDetailTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.original_db_path = storage.DB_PATH
        storage.DB_PATH = Path(self.tmpdir.name) / "gui.db"
        storage.init_db()
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"

    def tearDown(self):
        main.app.dependency_overrides.clear()
        storage.DB_PATH = self.original_db_path
        self.tmpdir.cleanup()

    def test_detail_keeps_submission_level_separate_from_correlation_type(self):
        payload = {
            "is": {
                "fitness": 1.2,
                "margin": 0.0006,
                "checks": [{"name": "LOW_SHARPE", "result": "FAIL", "message": "too low"}],
            },
            "settings": {"region": "USA", "universe": "TOP3000"},
        }
        storage.upsert_alpha(
            {
                "alpha_id": "alpha_fail_pass",
                "alpha_type": "MARGINAL",
                "region": "USA",
                "universe": "TOP3000",
                "fitness": 1.2,
                "margin": 0.0006,
                "status": "CHECKED_PASS",
                "payload": payload,
            }
        )
        storage.add_check_result(
            "alpha_fail_pass",
            "PASS",
            0.1,
            "pass result with failing checks",
            source="manual",
            payload=payload,
        )

        client = TestClient(main.app)
        check_response = client.get("/check?type_filter=PASS&level_filter=substandard")
        detail_response = client.get("/alphas/alpha_fail_pass")

        self.assertEqual(check_response.status_code, 200)
        self.assertIn("不合格因子", check_response.text)
        self.assertEqual(detail_response.status_code, 200)
        self.assertIn("提交判定: 不合格因子", detail_response.text)
        self.assertIn("相关性分类: MARGINAL", detail_response.text)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import app.main as main
from app.storage import connect, init_db, upsert_alpha


class AlphaPagePerformanceTests(unittest.TestCase):
    def setUp(self):
        init_db()
        with connect() as conn:
            conn.execute("DELETE FROM check_results")
            conn.execute("DELETE FROM alpha_records")

    def test_alpha_page_rates_only_current_page(self):
        for i in range(25):
            alpha_id = f"perf_alpha_{i:02d}"
            upsert_alpha(
                {
                    "alpha_id": alpha_id,
                    "alpha_type": "S",
                    "name": alpha_id,
                    "region": "USA",
                    "universe": "TOP3000",
                    "sharpe": 1.8,
                    "fitness": 1.8,
                    "margin": 0.002,
                    "prod_corr": 0.2,
                    "ppa_corr": 0.2,
                    "status": "UNSUBMITTED",
                    "source": "test",
                    "payload": {"regular": "rank(close)"},
                }
            )

        rating = {
            "submission_class": "premium",
            "submission_label": "优质因子",
            "alpha_level": "优质因子",
            "grade": "S",
            "grade_label": "S级: 直接提交",
        }
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        try:
            client = TestClient(main.app)
            with patch("app.main.build_alpha_rating", return_value=rating) as mocked_rating:
                response = client.get("/alphas?page=2")
        finally:
            main.app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(mocked_rating.call_count, 12)
        self.assertIn("总共记录: <strong>25</strong>", response.text)


if __name__ == "__main__":
    unittest.main()

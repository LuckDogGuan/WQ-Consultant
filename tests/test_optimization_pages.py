import unittest

from fastapi.testclient import TestClient

import app.main as main


class OptimizationPageTests(unittest.TestCase):
    def test_optimization_page_shows_name_and_variant_action(self):
        from app.storage import init_db, upsert_alpha
        init_db()
        upsert_alpha({
            "alpha_id": "test_opt_alpha",
            "alpha_type": "C",
            "name": "因子名称",
            "region": "USA",
            "universe": "TOP3000",
            "sharpe": 1.3,
            "fitness": 1.5,
            "margin": 0.0020,
            "prod_corr": 0.3,
            "ppa_corr": 0.3,
            "status": "UNSUBMITTED",
            "source": "test",
            "payload": {"expression": "close", "regular": "close"}
        })

        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        try:
            client = TestClient(main.app)
            response = client.get("/optimization?status_filter=optimizable")
        finally:
            main.app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 200)
        self.assertIn("因子名称", response.text)
        self.assertIn("生成变体", response.text)


    def test_optimization_page_shows_run_controls(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        try:
            client = TestClient(main.app)
            response = client.get("/optimization")
        finally:
            main.app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 200)
        self.assertIn("source_mode", response.text)
        self.assertIn("/api/jobs/optimization", response.text)
        self.assertIn("最近的优化任务", response.text)




if __name__ == "__main__":
    unittest.main()

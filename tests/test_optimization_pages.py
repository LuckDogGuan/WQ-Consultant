import unittest

from fastapi.testclient import TestClient

import app.main as main


class OptimizationPageTests(unittest.TestCase):
    def test_optimization_page_shows_name_and_variant_action(self):
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

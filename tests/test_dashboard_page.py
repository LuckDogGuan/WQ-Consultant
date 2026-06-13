import unittest

from fastapi.testclient import TestClient

import app.main as main


class DashboardPageTests(unittest.TestCase):
    def test_dashboard_adds_daily_metrics_without_removing_system_overview(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        try:
            client = TestClient(main.app)
            response = client.get("/dashboard")
        finally:
            main.app.dependency_overrides.clear()

        html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("今日回测个数", html)
        self.assertIn("今日检查提交", html)
        self.assertIn("优化规划", html)
        self.assertIn("今日正式提交", html)
        self.assertIn("Alpha 记录总数", html)
        self.assertIn("检测合格 Alpha", html)


if __name__ == "__main__":
    unittest.main()

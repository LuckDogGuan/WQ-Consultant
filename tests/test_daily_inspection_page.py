import unittest

from fastapi.testclient import TestClient

import app.main as main


class DailyInspectionPageTests(unittest.TestCase):
    def test_daily_inspection_page_exposes_priority_task_and_submit_mode(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        try:
            client = TestClient(main.app)
            response = client.get("/daily-inspection")
        finally:
            main.app.dependency_overrides.clear()

        html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("每日因子巡检", html)
        self.assertIn("最高优先级自动任务", html)
        self.assertIn("提交因子", html)
        self.assertIn("WQ 可提交因子列表", html)


if __name__ == "__main__":
    unittest.main()

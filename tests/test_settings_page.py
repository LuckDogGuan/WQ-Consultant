import unittest
from fastapi.testclient import TestClient
import app.main as main
from app.storage import get_settings


class SettingsPageTests(unittest.TestCase):
    def setUp(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"

    def tearDown(self):
        main.app.dependency_overrides.clear()

    def test_settings_page_get_renders_successfully(self):
        client = TestClient(main.app)
        response = client.get("/settings")
        self.assertEqual(response.status_code, 200)
        
        html = response.content.decode("utf-8")
        # Ensure our dynamic elements or region label/select exists
        self.assertIn("回测地区 (Region)", html)
        self.assertIn("股票池 (Universe)", html)
        self.assertIn("交易延迟 (Delay)", html)
        # Ensure the script block with day1_scopes is included
        self.assertIn("scopeMapping", html)
        self.assertIn("delayMapping", html)

    def test_settings_page_post_saves_successfully(self):
        client = TestClient(main.app)
        # Post new settings
        payload = {
            "region": "USA",
            "universe": "TOPSP500",
            "delay": "1",
            "daily_alpha_count_usage": "track"
        }
        response = client.post("/settings", data=payload)
        self.assertEqual(response.status_code, 200)

        html = response.content.decode("utf-8")
        self.assertIn("配置已成功保存", html)

        # Check in DB
        db_settings = get_settings()
        self.assertEqual(db_settings.get("region"), "USA")
        self.assertEqual(db_settings.get("universe"), "TOPSP500")
        self.assertEqual(db_settings.get("delay"), "1")


if __name__ == "__main__":
    unittest.main()

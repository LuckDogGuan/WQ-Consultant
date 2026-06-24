import unittest
from fastapi.testclient import TestClient
import app.main as main


class ReferencePageTests(unittest.TestCase):
    def test_reference_page_renders_successfully(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        try:
            client = TestClient(main.app)
            response = client.get("/reference")
        finally:
            main.app.dependency_overrides.clear()

        html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("社区参考库", html)
        self.assertIn("关于 &amp; 进阶指南", html)
        self.assertIn("主题数据集 (PPA)", html)
        self.assertIn("PPA 爬取同步工具", html)

    def test_post_reference_fetch_creates_job(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        try:
            client = TestClient(main.app)
            response = client.post("/api/jobs/reference_fetch", data={
                "region": "USA",
                "universe": "TOP3000",
                "delay": "1"
            })
        finally:
            main.app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("job_id", data)


if __name__ == "__main__":
    unittest.main()

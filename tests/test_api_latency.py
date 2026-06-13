import unittest

from fastapi.testclient import TestClient

import app.main as main


class ApiLatencyTests(unittest.TestCase):
    def test_api_response_includes_process_time_header(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        try:
            client = TestClient(main.app)
            response = client.post(
                "/api/expressions/validate",
                json={"expression": "rank(close)"},
            )
        finally:
            main.app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 200)
        self.assertIn("x-process-time-ms", response.headers)
        self.assertGreaterEqual(float(response.headers["x-process-time-ms"]), 0.0)


if __name__ == "__main__":
    unittest.main()

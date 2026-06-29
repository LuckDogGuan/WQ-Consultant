import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import app.main as main
from app.services.template_iteration import run_template_iteration_job


class TemplateIterationJobTests(unittest.TestCase):
    def setUp(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        self.client = TestClient(main.app)

    def tearDown(self):
        main.app.dependency_overrides.clear()

    def test_template_iteration_job_route_creates_manual_job(self):
        started = {}

        with patch("app.main.create_job", return_value=123) as create_job:
            with patch("app.main.JobRunner") as runner_cls:
                runner_cls.return_value.start_job.side_effect = lambda job_id, kind, params: started.update(
                    {"job_id": job_id, "kind": kind, "params": params}
                )

                response = self.client.post(
                    "/api/jobs/template_iteration",
                    json={
                        "candidates": [{"expression": "rank(close)", "region": "USA", "field_id": "close"}],
                        "universe": "TOP3000",
                        "delay": 1,
                    },
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["job_id"], 123)
        self.assertEqual(started["kind"], "template_iteration")
        self.assertEqual(started["params"]["custom_alphas"], ["rank(close)"])
        create_job.assert_called_once()

    def test_template_iteration_job_route_rejects_empty_candidates(self):
        response = self.client.post("/api/jobs/template_iteration", json={"candidates": []})

        self.assertEqual(response.status_code, 400)

    def test_run_template_iteration_job_reuses_backtest_custom_alphas(self):
        with patch("app.services.simulation_service.run_backtest_job") as run_backtest:
            run_template_iteration_job(
                7,
                {
                    "candidates": [
                        {"expression": "rank(close)"},
                        {"expression": "ts_rank(volume, 20)"},
                    ],
                    "neutralization": "INDUSTRY",
                },
            )

        run_backtest.assert_called_once()
        job_id, params = run_backtest.call_args.args
        self.assertEqual(job_id, 7)
        self.assertEqual(params["custom_alphas"], ["rank(close)", "ts_rank(volume, 20)"])
        self.assertEqual(params["neutralization"], "INDUSTRY")


if __name__ == "__main__":
    unittest.main()

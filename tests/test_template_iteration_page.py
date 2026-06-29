import unittest

from fastapi.testclient import TestClient

import app.main as main


class TemplateIterationPageTests(unittest.TestCase):
    def setUp(self):
        main.app.dependency_overrides[main.get_current_admin] = lambda: "admin"
        self.client = TestClient(main.app)

    def tearDown(self):
        main.app.dependency_overrides.clear()

    def test_template_iteration_page_loads(self):
        response = self.client.get("/template-iteration")

        self.assertEqual(response.status_code, 200)
        self.assertIn("/api/template-iteration/preview", response.text)
        self.assertIn("USA", response.text)
        self.assertIn("template-quality-mode", response.text)
        self.assertIn("hidden-reason-list", response.text)
        self.assertIn("exportTemplateCandidatesCsv", response.text)
        self.assertIn("startTemplateIterationJob", response.text)

    def test_template_iteration_preview_api_returns_candidates(self):
        response = self.client.post(
            "/api/template-iteration/preview",
            json={
                "templates": "rank({field})",
                "fields": [{"id": "good_field", "quality": "GOOD", "region": "USA"}],
                "regions": ["USA"],
                "max_candidates": 10,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["visible"][0]["expression"], "rank(good_field)")

    def test_template_iteration_preview_api_can_use_local_catalog(self):
        original_datasets = main.load_datasets_from_cache
        original_fields = main.load_fields_from_cache
        main.load_datasets_from_cache = lambda region, universe, delay: [{"id": "dataset1"}]
        main.load_fields_from_cache = lambda region, universe, delay, dataset_id: [
            {"id": "catalog_field", "quality": "GOOD", "region": region, "dataset": dataset_id}
        ]
        try:
            response = self.client.post(
                "/api/template-iteration/preview",
                json={"templates": "rank({field})", "regions": ["USA"], "max_candidates": 10},
            )
        finally:
            main.load_datasets_from_cache = original_datasets
            main.load_fields_from_cache = original_fields

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["visible"][0]["expression"], "rank(catalog_field)")

    def test_template_iteration_preview_api_accepts_sweep_values(self):
        response = self.client.post(
            "/api/template-iteration/preview",
            json={
                "templates": "ts_decay_linear({field}, {decay})",
                "fields": [{"id": "close", "quality": "GOOD", "region": "USA"}],
                "regions": ["USA"],
                "decay_values": [3, 5],
                "max_candidates": 10,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["expression"] for item in response.json()["visible"]],
            ["ts_decay_linear(close, 3)", "ts_decay_linear(close, 5)"],
        )

    def test_template_iteration_preview_api_includes_review_fields_when_requested(self):
        response = self.client.post(
            "/api/template-iteration/preview",
            json={
                "templates": "rank({field})",
                "fields": [
                    {"id": "review_field", "quality": "REVIEW", "region": "USA"},
                    {"id": "bad_field", "quality": "BAD", "region": "USA"},
                ],
                "regions": ["USA"],
                "field_quality_mode": "GOOD_AND_REVIEW",
                "max_candidates": 10,
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual([item["expression"] for item in payload["visible"]], ["rank(review_field)"])
        self.assertEqual(payload["hidden"][0]["reason_code"], "BAD_FIELD")

    def test_template_iteration_preview_api_deduplicates_visible_candidates(self):
        response = self.client.post(
            "/api/template-iteration/preview",
            json={
                "templates": "rank({field})\n\nrank( {field} )",
                "fields": [{"id": "close", "quality": "GOOD", "region": "USA"}],
                "regions": ["USA"],
                "max_candidates": 10,
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual([item["expression"] for item in payload["visible"]], ["rank(close)"])
        self.assertEqual(payload["hidden"][0]["reason_code"], "DUPLICATE_EXPRESSION")
        self.assertEqual(payload["summary"]["duplicate_count"], 1)


if __name__ == "__main__":
    unittest.main()

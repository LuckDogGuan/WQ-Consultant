import json
import unittest

from app.services.optimization_run_service import extract_source_neutralization, group_tasks_by_neutralization, parse_alpha_ids


class OptimizationRunServiceTests(unittest.TestCase):
    def test_parse_alpha_ids_accepts_lines_and_commas(self):
        self.assertEqual(parse_alpha_ids("a1\na2, a3\n a2 "), ["a1", "a2", "a3"])

    def test_extract_source_neutralization_reads_alpha_payload_settings(self):
        payload = json.dumps({"settings": {"neutralization": "INDUSTRY"}})

        self.assertEqual(extract_source_neutralization(payload), "INDUSTRY")

    def test_extract_source_neutralization_falls_back_to_default(self):
        self.assertEqual(extract_source_neutralization("{}"), "SUBINDUSTRY")

    def test_group_tasks_by_neutralization_keeps_source_neutralization(self):
        tasks = [
            ("expr1", 0, "INDUSTRY"),
            ("expr2", 0, "SUBINDUSTRY"),
            ("expr3", 0, "INDUSTRY"),
        ]

        self.assertEqual(
            group_tasks_by_neutralization(tasks),
            {
                "INDUSTRY": [("expr1", 0), ("expr3", 0)],
                "SUBINDUSTRY": [("expr2", 0)],
            },
        )


if __name__ == "__main__":
    unittest.main()

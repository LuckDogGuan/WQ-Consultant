import unittest

from app.services.job_params import normalize_optimization_params


class JobParamsTests(unittest.TestCase):
    def test_normalize_optimization_params_fills_old_job_defaults(self):
        params = normalize_optimization_params({"source_mode": "manual", "alpha_ids": "a1"})

        self.assertEqual(params["schema_version"], 2)
        self.assertEqual(params["source_mode"], "manual")
        self.assertEqual(params["alpha_ids"], "a1")
        self.assertEqual(params["recent_days"], 14)
        self.assertEqual(params["candidate_limit"], 20)
        self.assertEqual(params["children_per_request"], 1)

    def test_normalize_optimization_params_clamps_invalid_numbers(self):
        params = normalize_optimization_params({"recent_days": 0, "candidate_limit": -5, "children_per_request": 0})

        self.assertEqual(params["recent_days"], 14)
        self.assertEqual(params["candidate_limit"], 20)
        self.assertEqual(params["children_per_request"], 1)


if __name__ == "__main__":
    unittest.main()

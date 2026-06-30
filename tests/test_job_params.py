import unittest

from app.services.job_params import normalize_optimization_params, normalize_backtest_params, advisor_level_allows_dataset


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


    def test_normalize_backtest_params_uses_strict_advisor_defaults(self):
        params = normalize_backtest_params({"dataset_ids": ["fundamental6"], "advisor_level": "gold"})

        self.assertEqual(params["schema_version"], 1)
        self.assertEqual(params["profile"], "wang_strict")
        self.assertEqual(params["advisor_level"], "gold")
        self.assertEqual(params["self_corr_safe"], 0.68)
        self.assertEqual(params["self_corr_hard"], 0.70)
        self.assertEqual(params["turnover_warn"], 0.10)
        self.assertEqual(params["turnover_hard"], 0.15)
        self.assertEqual(params["operator_count_max"], 8)
        self.assertTrue(params["hide_grade_d_local"])
        self.assertTrue(params["retire_grade_d_remote"])

    def test_normalize_backtest_params_reuses_shared_stage_slots_for_regions(self):
        params = normalize_backtest_params({
            "dataset_ids": ["fundamental6"],
            "fo_backtest_children": "4",
            "fo_backtest_threads": "2",
            "so_backtest_children": "3",
            "so_backtest_threads": "1",
            "th_backtest_children": "2",
            "th_backtest_threads": "1",
        })

        self.assertEqual(params["region_stage_config"]["USA"]["FO"]["children"], 4)
        self.assertEqual(params["region_stage_config"]["USA"]["FO"]["threads"], 2)
        self.assertEqual(params["region_stage_config"]["ASI"]["SO"]["children"], 3)
        self.assertEqual(params["region_stage_config"]["ASI"]["SO"]["threads"], 1)
        self.assertEqual(params["region_stage_config"]["EUR"]["TH"]["children"], 2)
        self.assertEqual(params["region_stage_config"]["EUR"]["TH"]["threads"], 1)

    def test_advisor_level_allows_dataset_keeps_future_expansion_table_driven(self):
        self.assertTrue(advisor_level_allows_dataset("gold", "fundamental6"))
        self.assertFalse(advisor_level_allows_dataset("starter", "analyst4"))
        self.assertTrue(advisor_level_allows_dataset("master", "analyst4"))
if __name__ == "__main__":
    unittest.main()

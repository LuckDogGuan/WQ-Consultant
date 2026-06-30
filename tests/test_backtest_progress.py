import unittest

from app.services.simulation_service import (
    build_backtest_stage_plan,
    describe_missing_location_response,
    format_backtest_progress_message,
    format_backtest_stage_detail_message,
    normalize_simulation_post_payload,
    rate_limit_retry_seconds,
    stage_detail_progress_values,
    should_emit_stage_progress_event,
    stage_pool_settings,
)


class BacktestProgressTests(unittest.TestCase):
    def test_build_stage_plan_counts_enabled_stage_per_dataset(self):
        plan = build_backtest_stage_plan(
            dataset_ids=["macro38", "analyst4"],
            run_fo=True,
            run_so=False,
            run_th=True,
        )

        self.assertEqual(
            plan,
            [
                ("macro38", "FO", 1, 2, 1, 2, 1, 4),
                ("macro38", "TH", 1, 2, 2, 2, 2, 4),
                ("analyst4", "FO", 2, 2, 1, 2, 3, 4),
                ("analyst4", "TH", 2, 2, 2, 2, 4, 4),
            ],
        )

    def test_format_progress_message_includes_numbers_for_events(self):
        message = format_backtest_progress_message(
            dataset_id="macro38",
            stage_name="SO",
            dataset_index=2,
            total_datasets=3,
            stage_index=2,
            stages_per_dataset=3,
            stage_current=5,
            stage_total=9,
            action="completed",
        )

        self.assertEqual(
            message,
            "[macro38] SO 已完成。数据集 2/3，当前阶段 2/3，总进度 5/9。",
        )

    def test_format_stage_detail_message_includes_inner_progress(self):
        message = format_backtest_stage_detail_message(
            dataset_id="pv63",
            stage_name="FO",
            stage_index=1,
            stages_per_dataset=3,
            completed_pools=3,
            total_pools=12,
            group_label="分组 1/2: MARKET",
        )

        self.assertEqual(
            message,
            "[pv63] FO 小阶段进度：分组 1/2: MARKET，Pool 3/12，当前阶段 1/3。",
        )

    def test_stage_detail_progress_values_use_inner_pool_counts(self):
        self.assertEqual(stage_detail_progress_values(0, 12), (0, 12))
        self.assertEqual(stage_detail_progress_values(3, 12), (3, 12))
        self.assertEqual(stage_detail_progress_values(-1, 12), (0, 12))
        self.assertEqual(stage_detail_progress_values(15, 12), (12, 12))
        self.assertEqual(stage_detail_progress_values(3, 0), (0, 0))

    def test_missing_location_response_message_includes_status_and_body(self):
        class Response:
            status_code = 400
            headers = {"Retry-After": "5"}
            text = '{"detail":"bad alpha expression"}'

        message = describe_missing_location_response(Response())

        self.assertIn("status=400", message)
        self.assertIn("Retry-After=5", message)
        self.assertIn("bad alpha expression", message)

    def test_normalize_simulation_post_payload_unwraps_single_simulation(self):
        simulation = {"type": "REGULAR", "regular": "rank(close)"}

        self.assertIs(normalize_simulation_post_payload([simulation]), simulation)

    def test_normalize_simulation_post_payload_keeps_multi_simulations(self):
        simulations = [
            {"type": "REGULAR", "regular": "rank(close)"},
            {"type": "REGULAR", "regular": "rank(volume)"},
        ]

        self.assertIs(normalize_simulation_post_payload(simulations), simulations)

    def test_normalize_simulation_post_payload_keeps_existing_object(self):
        simulation = {"type": "REGULAR", "regular": "rank(close)"}

        self.assertIs(normalize_simulation_post_payload(simulation), simulation)

    def test_rate_limit_retry_seconds_uses_retry_after_with_floor(self):
        self.assertEqual(
            rate_limit_retry_seconds(
                failure_count=1,
                short_seconds=30,
                long_seconds=600,
            ),
            30,
        )

    def test_rate_limit_retry_seconds_uses_long_wait_each_fifth_429(self):
        self.assertEqual(rate_limit_retry_seconds(4, short_seconds=30, long_seconds=600), 30)
        self.assertEqual(rate_limit_retry_seconds(5, short_seconds=30, long_seconds=600), 600)
        self.assertEqual(rate_limit_retry_seconds(6, short_seconds=30, long_seconds=600), 30)
        self.assertEqual(rate_limit_retry_seconds(10, short_seconds=30, long_seconds=600), 600)

    def test_rate_limit_retry_seconds_does_not_allow_invalid_counts(self):
        self.assertEqual(rate_limit_retry_seconds(0, short_seconds=30, long_seconds=600), 30)

    def test_stage_progress_events_only_emit_at_milestones(self):
        emitted = set()

        self.assertFalse(should_emit_stage_progress_event(1, 10, emitted))
        self.assertTrue(should_emit_stage_progress_event(3, 10, emitted))
        self.assertEqual(emitted, {25})
        self.assertFalse(should_emit_stage_progress_event(4, 10, emitted))
        self.assertTrue(should_emit_stage_progress_event(5, 10, emitted))
        self.assertEqual(emitted, {25, 50})
        self.assertTrue(should_emit_stage_progress_event(10, 10, emitted))
        self.assertEqual(emitted, {25, 50, 100})


    def test_stage_pool_settings_uses_region_specific_values(self):
        params = {
            "region_stage_config": {
                "USA": {"FO": {"children": 4, "threads": 2}},
                "ASI": {"SO": {"children": 3, "threads": 1}},
            }
        }

        self.assertEqual(stage_pool_settings(params, "USA", "FO", 6, 10), (4, 2))
        self.assertEqual(stage_pool_settings(params, "ASI", "SO", 5, 8), (3, 1))
        self.assertEqual(stage_pool_settings(params, "EUR", "TH", 5, 8), (5, 8))
class BacktestParameterResolutionTests(unittest.TestCase):
    def test_get_bool_param_prioritizes_params(self):
        from app.services.simulation_service import get_bool_param
        params = {"test_key_bool": False}
        self.assertFalse(get_bool_param(params, "test_key_bool", True))
        
        params = {"test_key_bool": "true"}
        self.assertTrue(get_bool_param(params, "test_key_bool", False))
        
        self.assertTrue(get_bool_param({}, "missing_bool_key", True))
        self.assertFalse(get_bool_param({}, "missing_bool_key2", False))

    def test_get_int_param_prioritizes_params(self):
        from app.services.simulation_service import get_int_param
        params = {"test_key_int": 42}
        self.assertEqual(get_int_param(params, "test_key_int", 10), 42)
        
        params = {"test_key_int": "123"}
        self.assertEqual(get_int_param(params, "test_key_int", 10), 123)
        
        self.assertEqual(get_int_param({}, "missing_int_key", 10), 10)

    def test_get_float_param_prioritizes_params(self):
        from app.services.simulation_service import get_float_param
        params = {"test_key_float": 3.14}
        self.assertEqual(get_float_param(params, "test_key_float", 1.0), 3.14)
        
        params = {"test_key_float": "2.718"}
        self.assertEqual(get_float_param(params, "test_key_float", 1.0), 2.718)
        
        self.assertEqual(get_float_param({}, "missing_float_key", 1.0), 1.0)

    def test_get_str_param_prioritizes_params(self):
        from app.services.simulation_service import get_str_param
        params = {"test_key_str": "hello"}
        self.assertEqual(get_str_param(params, "test_key_str", "default"), "hello")
        
        self.assertEqual(get_str_param({}, "missing_str_key", "default"), "default")


if __name__ == "__main__":
    unittest.main()

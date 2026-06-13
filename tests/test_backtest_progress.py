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


if __name__ == "__main__":
    unittest.main()

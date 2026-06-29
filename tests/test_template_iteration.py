import unittest

from app.services.template_iteration import (
    TemplateIterationOptions,
    classify_field_quality,
    count_expression_complexity,
    create_template_iteration_job_params,
    dedupe_candidates,
    expand_template_candidates,
    grade_candidate_result,
    normalize_template_iteration_options,
    parse_templates,
)


class TemplateIterationTests(unittest.TestCase):
    def test_parse_templates_splits_non_empty_blocks(self):
        templates = parse_templates("rank({field})\n\n-ts_rank({field}, {days})")

        self.assertEqual([item.name for item in templates], ["template_1", "template_2"])
        self.assertEqual(templates[0].placeholders, {"field"})
        self.assertEqual(templates[1].placeholders, {"field", "days"})

    def test_parse_templates_accepts_dash_separator(self):
        templates = parse_templates("rank({field})\n---\nts_rank({field}, {days})")

        self.assertEqual(len(templates), 2)
        self.assertEqual(templates[1].expression, "ts_rank({field}, {days})")

    def test_expand_uses_good_fields_and_hides_bad_fields(self):
        fields = [
            {"id": "good_field", "dataset": "fundamental6", "quality": "GOOD", "region": "USA"},
            {"id": "bad_field", "dataset": "model16", "quality": "BAD", "region": "USA"},
        ]

        result = expand_template_candidates(
            ["rank({field})"],
            fields,
            TemplateIterationOptions(regions=["USA"], max_candidates=10),
        )

        self.assertEqual([item.expression for item in result.visible], ["rank(good_field)"])
        self.assertEqual(result.hidden[0].reason_code, "BAD_FIELD")

    def test_review_fields_are_hidden_by_default(self):
        fields = [{"id": "review_field", "quality": "REVIEW", "region": "USA"}]

        result = expand_template_candidates(
            ["rank({field})"],
            fields,
            TemplateIterationOptions(regions=["USA"]),
        )

        self.assertEqual(result.visible, [])
        self.assertEqual(result.hidden[0].reason_code, "REVIEW_FIELD")

    def test_review_fields_can_be_included_explicitly(self):
        fields = [{"id": "review_field", "quality": "REVIEW", "region": "USA"}]

        result = expand_template_candidates(
            ["rank({field})"],
            fields,
            TemplateIterationOptions(regions=["USA"], good_qualities={"GOOD", "REVIEW", ""}),
        )

        self.assertEqual([item.expression for item in result.visible], ["rank(review_field)"])

    def test_classify_field_quality_accepts_quality_tag_alias(self):
        self.assertEqual(classify_field_quality({"quality_tag": "review"}), "REVIEW")
        self.assertEqual(classify_field_quality({"quality": "bad"}), "BAD")
        self.assertEqual(classify_field_quality({"quality": "good"}), "GOOD")
        self.assertEqual(classify_field_quality({}), "GOOD")

    def test_expand_limits_candidate_count(self):
        fields = [
            {"id": "f1", "quality": "GOOD", "region": "USA"},
            {"id": "f2", "quality": "GOOD", "region": "USA"},
            {"id": "f3", "quality": "GOOD", "region": "USA"},
        ]

        result = expand_template_candidates(
            ["rank({field})"],
            fields,
            TemplateIterationOptions(regions=["USA"], max_candidates=2),
        )

        self.assertEqual(len(result.visible), 2)
        self.assertEqual(result.summary["visible_count"], 2)
        self.assertEqual(result.summary["truncated_count"], 1)
        self.assertEqual(result.hidden[0].reason_code, "CANDIDATE_EXPLOSION")

    def test_dedupe_candidates_keeps_first_expression_and_marks_duplicates(self):
        result = expand_template_candidates(
            ["rank({field})", "rank( {field} )"],
            [{"id": "close", "quality": "GOOD", "region": "USA"}],
            TemplateIterationOptions(regions=["USA"], max_candidates=10),
        )

        deduped = dedupe_candidates(result)

        self.assertEqual([item.expression for item in deduped.visible], ["rank(close)"])
        self.assertEqual([item.reason_code for item in deduped.hidden], ["DUPLICATE_EXPRESSION"])
        self.assertEqual(deduped.summary["duplicate_count"], 1)

    def test_expand_sweeps_supported_template_parameters(self):
        fields = [{"id": "close", "quality": "GOOD", "region": "USA"}]

        result = expand_template_candidates(
            ["ts_decay_linear(group_rank({field}, {group}), {decay}, dense=false)"],
            fields,
            TemplateIterationOptions(
                regions=["USA"],
                max_candidates=10,
                decay_values=[3, 5],
                group_values=["sector", "industry"],
            ),
        )

        self.assertEqual(
            [item.expression for item in result.visible],
            [
                "ts_decay_linear(group_rank(close, sector), 3, dense=false)",
                "ts_decay_linear(group_rank(close, industry), 3, dense=false)",
                "ts_decay_linear(group_rank(close, sector), 5, dense=false)",
                "ts_decay_linear(group_rank(close, industry), 5, dense=false)",
            ],
        )

    def test_expand_supports_two_field_templates(self):
        fields = [
            {"id": "assets", "quality": "GOOD", "region": "USA"},
            {"id": "liabilities", "quality": "GOOD", "region": "USA"},
        ]

        result = expand_template_candidates(
            ["rank(divide({field_a}, {field_b}))"],
            fields,
            TemplateIterationOptions(regions=["USA"], max_candidates=10),
        )

        self.assertEqual([item.expression for item in result.visible], ["rank(divide(assets, liabilities))"])
        self.assertEqual(result.visible[0].field_id, "assets,liabilities")

    def test_unknown_placeholder_is_hidden(self):
        fields = [{"id": "close", "quality": "GOOD", "region": "USA"}]

        result = expand_template_candidates(
            ["rank({missing})"],
            fields,
            TemplateIterationOptions(regions=["USA"]),
        )

        self.assertEqual(result.visible, [])
        self.assertEqual(result.hidden[0].reason_code, "UNKNOWN_PLACEHOLDER")

    def test_invalid_expression_is_hidden(self):
        result = expand_template_candidates(
            ["rank("],
            [{"id": "close", "quality": "GOOD", "region": "USA"}],
            TemplateIterationOptions(regions=["USA"]),
        )

        self.assertEqual(result.visible, [])
        self.assertEqual(result.hidden[0].reason_code, "EXPRESSION_INVALID")

    def test_no_matched_fields_is_reported(self):
        result = expand_template_candidates(
            ["rank({field})"],
            [],
            TemplateIterationOptions(regions=["USA"]),
        )

        self.assertEqual(result.visible, [])
        self.assertEqual(result.hidden[0].reason_code, "NO_MATCHED_FIELDS")
        self.assertEqual(result.summary["hidden_count"], 1)

    def test_count_expression_complexity_counts_ops_and_fields(self):
        complexity = count_expression_complexity("rank(ts_mean(close, 20))")

        self.assertEqual(complexity["operator_count"], 2)
        self.assertEqual(complexity["field_count"], 1)

    def test_complex_expression_is_hidden(self):
        result = expand_template_candidates(
            ["rank(ts_mean(ts_delta({field}, 1), 20))"],
            [{"id": "close", "quality": "GOOD", "region": "USA"}],
            TemplateIterationOptions(regions=["USA"], operator_count_max=2),
        )

        self.assertEqual(result.visible, [])
        self.assertEqual(result.hidden[0].reason_code, "COMPLEXITY_LIMIT")
        self.assertEqual(result.summary["hidden_reason_counts"], {"COMPLEXITY_LIMIT": 1})

    def test_normalize_template_iteration_options_accepts_strings_and_lists(self):
        options = normalize_template_iteration_options(
            {
                "regions": ["usa", "EUR"],
                "max_candidates": "25",
                "day_values": "5,20,bad",
                "decay_values": [0, "3", "x"],
                "neutralization_values": "MARKET, INDUSTRY",
                "group_values": ["sector", "industry"],
            }
        )

        self.assertEqual(options.regions, ["USA", "EUR"])
        self.assertEqual(options.max_candidates, 25)
        self.assertEqual(options.day_values, [5, 20])
        self.assertEqual(options.decay_values, [0, 3])
        self.assertEqual(options.neutralization_values, ["MARKET", "INDUSTRY"])
        self.assertEqual(options.group_values, ["sector", "industry"])

    def test_normalize_template_iteration_options_uses_safe_defaults(self):
        options = normalize_template_iteration_options(
            {
                "regions": [],
                "max_candidates": "-1",
                "day_values": "bad",
                "decay_values": "",
                "neutralization_values": "",
                "group_values": "",
            }
        )

        self.assertEqual(options.regions, ["USA"])
        self.assertEqual(options.max_candidates, 100)
        self.assertEqual(options.day_values, [20])
        self.assertEqual(options.decay_values, [0])
        self.assertEqual(options.neutralization_values, ["INDUSTRY"])
        self.assertEqual(options.group_values, ["industry"])

    def test_create_template_iteration_job_params_uses_selected_candidates_only(self):
        params = create_template_iteration_job_params(
            [{"expression": "rank(close)", "region": "USA", "field_id": "close"}],
            {"universe": "TOP3000", "delay": 1},
        )

        self.assertEqual(params["kind"], "template_iteration")
        self.assertEqual(params["universe"], "TOP3000")
        self.assertEqual(params["delay"], 1)
        self.assertEqual(params["candidates"][0]["expression"], "rank(close)")
        self.assertNotIn("submit", params)
        self.assertNotIn("ppa", params)
        self.assertNotIn("sa", params)

    def test_create_template_iteration_job_params_rejects_empty_candidates(self):
        with self.assertRaises(ValueError):
            create_template_iteration_job_params([], {})

    def test_create_template_iteration_job_params_rejects_invalid_expression(self):
        with self.assertRaises(ValueError):
            create_template_iteration_job_params(
                [{"expression": "rank(close", "region": "USA", "field_id": "close"}],
                {}
            )

    def test_grade_candidate_result_marks_safe_strong_candidate(self):
        grade = grade_candidate_result(
            {"sharpe": 1.7, "fitness": 1.2, "margin": 0.001, "turnover": 0.2, "self_corr": 0.5, "prod_corr": 0.4}
        )

        self.assertEqual(grade["grade"], "S")
        self.assertEqual(grade["action"], "manual_submit_candidate")

    def test_grade_candidate_result_rejects_high_self_corr(self):
        grade = grade_candidate_result({"sharpe": 2.0, "fitness": 2.0, "self_corr": 0.72})
        self.assertEqual(grade["grade"], "D")
        self.assertIn("SC_RISK", grade["reasons"])

    def test_grade_candidate_result_rejects_negative_sharpe(self):
        grade = grade_candidate_result({"sharpe": -0.5, "fitness": 1.0, "margin": 0.002, "self_corr": 0.3})
        self.assertEqual(grade["grade"], "D")
        self.assertIn("NEGATIVE_SHARPE", grade["reasons"])

    def test_grade_candidate_result_rejects_skip_status(self):
        grade = grade_candidate_result({"sharpe": 1.5, "fitness": 1.0, "status": "SKIP", "self_corr": 0.3})
        self.assertEqual(grade["grade"], "D")
        self.assertIn("SKIP_STATUS", grade["reasons"])


if __name__ == "__main__":
    unittest.main()

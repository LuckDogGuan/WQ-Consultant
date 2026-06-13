import unittest

from app.services.expression_validator import validate_expression


class ExpressionValidatorTests(unittest.TestCase):
    def test_valid_expression_passes_without_api(self):
        result = validate_expression("group_rank(ts_rank(close, 20), sector)")

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_unbalanced_parentheses_is_error(self):
        result = validate_expression("rank(ts_mean(close, 20)")

        self.assertFalse(result.is_valid)
        self.assertIn("unclosed_delimiter", [issue["code"] for issue in result.errors])

    def test_wrong_argument_count_is_error_for_known_operator(self):
        result = validate_expression("ts_rank(close)")

        self.assertFalse(result.is_valid)
        self.assertIn("invalid_argument_count", [issue["code"] for issue in result.errors])

    def test_unknown_operator_is_warning_not_error(self):
        result = validate_expression("new_platform_operator(close, 5)")

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])
        self.assertIn("unknown_operator", [issue["code"] for issue in result.warnings])


if __name__ == "__main__":
    unittest.main()

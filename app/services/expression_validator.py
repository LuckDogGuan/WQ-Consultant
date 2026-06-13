from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any


OPERATOR_SIGNATURES: dict[str, tuple[int, int]] = {
    "abs": (1, 1),
    "add": (2, 2),
    "bucket": (1, 2),
    "divide": (2, 2),
    "group_neutralize": (2, 2),
    "group_rank": (2, 2),
    "group_zscore": (2, 2),
    "greater": (2, 2),
    "is_not_nan": (1, 1),
    "hump": (1, 2),
    "hump_decay": (1, 2),
    "if_else": (3, 3),
    "log": (1, 1),
    "multiply": (2, 2),
    "normalize": (1, 3),
    "power": (2, 2),
    "quantile": (1, 3),
    "rank": (1, 2),
    "signed_power": (2, 2),
    "subtract": (2, 2),
    "trade_when": (3, 3),
    "ts_backfill": (2, 2),
    "ts_corr": (3, 3),
    "ts_count_nans": (2, 2),
    "ts_covariance": (3, 3),
    "ts_decay_linear": (2, 3),
    "ts_delta": (2, 2),
    "ts_delay": (2, 2),
    "ts_max": (2, 2),
    "ts_mean": (2, 2),
    "ts_min": (2, 2),
    "ts_product": (2, 2),
    "ts_rank": (2, 3),
    "ts_regression": (3, 5),
    "ts_scale": (2, 3),
    "ts_std_dev": (2, 2),
    "ts_sum": (2, 2),
    "ts_zscore": (2, 2),
    "vec_avg": (1, 1),
    "vec_sum": (1, 1),
    "winsorize": (1, 3),
    "zscore": (1, 1),
}


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: list[dict[str, Any]]
    warnings: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_expression(expression: str, operator_signatures: dict[str, tuple[int, int]] | None = None) -> ValidationResult:
    signatures = operator_signatures or OPERATOR_SIGNATURES
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    expr = (expression or "").strip()

    if not expr:
        errors.append(_issue("empty_expression", "表达式为空。"))
        return ValidationResult(False, errors, warnings)

    delimiter_errors = _validate_delimiters(expr)
    errors.extend(delimiter_errors)
    if delimiter_errors:
        return ValidationResult(False, errors, warnings)

    for name, args_text, position in _iter_function_calls(expr):
        name_lower = name.lower()
        args = split_top_level_args(args_text)
        if name_lower not in signatures:
            warnings.append(_issue("unknown_operator", f"本地规则未知 operator: {name}", position=position))
            continue

        min_args, max_args = signatures[name_lower]
        if not (min_args <= len(args) <= max_args):
            errors.append(
                _issue(
                    "invalid_argument_count",
                    f"{name} 参数数量为 {len(args)}，期望 {min_args}-{max_args}。",
                    position=position,
                    operator=name_lower,
                )
            )

    return ValidationResult(not errors, errors, warnings)


def split_top_level_args(args_text: str) -> list[str]:
    text = args_text.strip()
    if not text:
        return []

    args: list[str] = []
    start = 0
    depth = 0
    quote = ""
    for index, char in enumerate(text):
        if quote:
            if char == quote and text[index - 1:index] != "\\":
                quote = ""
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char in "([{":
            depth += 1
            continue
        if char in ")]}":
            depth -= 1
            continue
        if char == "," and depth == 0:
            args.append(text[start:index].strip())
            start = index + 1
    args.append(text[start:].strip())
    return [arg for arg in args if arg]


def _validate_delimiters(expression: str) -> list[dict[str, Any]]:
    pairs = {")": "(", "]": "[", "}": "{"}
    opening = set(pairs.values())
    stack: list[tuple[str, int]] = []
    quote = ""
    errors: list[dict[str, Any]] = []

    for index, char in enumerate(expression):
        if quote:
            if char == quote and expression[index - 1:index] != "\\":
                quote = ""
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char in opening:
            stack.append((char, index))
            continue
        if char in pairs:
            if not stack or stack[-1][0] != pairs[char]:
                errors.append(_issue("mismatched_delimiter", f"括号不匹配: {char}", position=index))
                continue
            stack.pop()

    if quote:
        errors.append(_issue("unclosed_quote", "字符串引号未闭合。"))
    for char, position in stack:
        errors.append(_issue("unclosed_delimiter", f"括号未闭合: {char}", position=position))
    return errors


def _iter_function_calls(expression: str) -> list[tuple[str, str, int]]:
    calls: list[tuple[str, str, int]] = []
    for match in re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", expression):
        name = match.group(1)
        open_index = expression.find("(", match.start())
        close_index = _find_matching_paren(expression, open_index)
        if close_index == -1:
            continue
        calls.append((name, expression[open_index + 1:close_index], match.start()))
    return calls


def _find_matching_paren(expression: str, open_index: int) -> int:
    depth = 0
    quote = ""
    for index in range(open_index, len(expression)):
        char = expression[index]
        if quote:
            if char == quote and expression[index - 1:index] != "\\":
                quote = ""
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    return -1


def _issue(code: str, message: str, **extra: Any) -> dict[str, Any]:
    issue = {"code": code, "message": message}
    issue.update(extra)
    return issue

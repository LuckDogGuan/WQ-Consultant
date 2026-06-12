"""Reusable HTML report helpers for WorldQuant Brain alpha analysis."""

from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path
from typing import Any

import pandas as pd


METRIC_FORMATS = {
    "sharpe": "number",
    "fitness": "number",
    "turnover": "percent",
    "returns": "percent",
    "drawdown": "percent",
    "margin": "permille",
    "longCount": "integer",
    "shortCount": "integer",
    "pnl": "currency",
}


def normalize_date_filter(value: Any) -> str | None:
    """Normalize notebook date input. Empty values mean no date filter."""
    if value is None:
        return None
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    if not text:
        return None
    if text.lower() in {"today", "now"}:
        return date.today().isoformat()
    return text


def alpha_platform_url(alpha_id: str) -> str:
    return f"https://platform.worldquantbrain.com/alpha/{alpha_id}"


def format_value(value: Any, style: str = "auto") -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "-"
    if style == "auto":
        style = "number"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return escape(str(value))
    if style == "percent":
        return f"{number * 100:.2f}%"
    if style == "permille":
        return f"{number * 1000:.3f} permil"
    if style == "integer":
        return f"{int(round(number)):,}"
    if style == "currency":
        return f"{number:,.0f}"
    return f"{number:.2f}"


def _text(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, (list, tuple, set)):
        return ", ".join(_text(item) for item in value) or "-"
    if isinstance(value, dict):
        return ", ".join(f"{key}: {_text(val)}" for key, val in value.items()) or "-"
    return str(value)


def extract_aggregate_metrics(detail: dict[str, Any]) -> list[dict[str, str]]:
    metrics = detail.get("is") or {}
    rows = []
    for key in ["sharpe", "turnover", "fitness", "returns", "drawdown", "margin", "longCount", "shortCount", "pnl"]:
        rows.append(
            {
                "label": _label(key),
                "value": format_value(metrics.get(key), METRIC_FORMATS.get(key, "number")),
                "raw_key": key,
            }
        )
    return rows


def extract_simulation_settings(detail: dict[str, Any]) -> dict[str, Any]:
    settings = detail.get("settings") or {}
    return {
        "Instrument Type": settings.get("instrumentType"),
        "Region": settings.get("region"),
        "Universe": settings.get("universe"),
        "Language": settings.get("language"),
        "Decay": settings.get("decay"),
        "Delay": settings.get("delay"),
        "Truncation": settings.get("truncation"),
        "Neutralization": settings.get("neutralization"),
        "Pasteurization": settings.get("pasteurization"),
        "NaN Handling": settings.get("nanHandling"),
        "Unit Handling": settings.get("unitHandling"),
        "Max Trade": settings.get("maxTrade"),
        "Max Position": settings.get("maxPosition"),
    }


def extract_properties(detail: dict[str, Any]) -> dict[str, Any]:
    regular = detail.get("regular") or {}
    return {
        "Name": detail.get("name"),
        "Category": detail.get("category"),
        "Tags": detail.get("tags"),
        "Color": detail.get("color"),
        "Description": regular.get("description") or detail.get("description"),
        "Status": detail.get("status"),
        "Stage": detail.get("stage"),
        "Grade": detail.get("grade"),
        "Hidden": detail.get("hidden"),
        "Favorite": detail.get("favorite"),
        "Date Created": detail.get("dateCreated"),
        "Date Modified": detail.get("dateModified"),
        "Date Submitted": detail.get("dateSubmitted"),
    }


def extract_failed_checks(detail: dict[str, Any]) -> list[dict[str, str]]:
    checks = ((detail.get("is") or {}).get("checks")) or []
    failed = []
    for check in checks:
        result = str(check.get("result") or check.get("status") or "").upper()
        if result in {"PASS", "PASSED", "SUCCESS", "OK", "PENDING"}:
            continue
        failed.append(
            {
                "name": str(check.get("name") or check.get("check") or "Unknown Check"),
                "result": result or "ATTENTION",
                "message": _check_message(check),
            }
        )
    return failed


def group_attention_checks(checks: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped = {"failed": [], "warning": [], "other": []}
    for check in checks:
        result = check.get("result", "").upper()
        if result in {"FAIL", "FAILED", "ERROR"}:
            grouped["failed"].append(check)
        elif result in {"WARNING", "WARN"}:
            grouped["warning"].append(check)
        else:
            grouped["other"].append(check)
    return grouped


def recordsets_summary(recordsets_df: pd.DataFrame) -> list[str]:
    if recordsets_df.empty or "name" not in recordsets_df.columns:
        return []
    return [str(value) for value in recordsets_df["name"].dropna().tolist()]


def render_alpha_report(
    alpha_id: str,
    detail: dict[str, Any],
    recordsets_df: pd.DataFrame,
    series_frames: dict[str, pd.DataFrame],
    selected_row: pd.Series | dict[str, Any] | None = None,
) -> str:
    expression = _expression_from_detail(detail, selected_row)
    aggregate_metrics = extract_aggregate_metrics(detail)
    settings = extract_simulation_settings(detail)
    properties = extract_properties(detail)
    failed_checks = extract_failed_checks(detail)
    yearly_stats = series_frames.get("yearly-stats", pd.DataFrame())

    return "\n".join(
        [
            report_css(),
            "<div class='wqb-report'>",
            _header(alpha_id, detail),
            _code_panel(expression),
            _metric_cards("Aggregate Data", aggregate_metrics),
            _settings_table(settings),
            _checks_panel(failed_checks),
            _chart_panel(series_frames),
            _yearly_table(yearly_stats),
            _properties_panel(properties),
            _recordsets_panel(recordsets_summary(recordsets_df)),
            "</div>",
        ]
    )


def report_css() -> str:
    return """
<style>
.wqb-report{font-family:Inter,Segoe UI,Arial,sans-serif;color:#263342;background:#f5f7fa;padding:12px;border:1px solid #e2e8f0;border-radius:8px}
.wqb-top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:10px}
.wqb-title{display:flex;align-items:center;gap:10px;min-width:0}
.wqb-status{background:#42c7c7;color:#fff;font-weight:700;font-size:11px;padding:4px 7px;border-radius:4px}
.wqb-id{font-size:18px;font-weight:700;white-space:nowrap}
.wqb-muted{color:#64748b;font-size:12px}
.wqb-link{color:#1976d2;text-decoration:none;font-weight:600}
.wqb-grid{display:grid;grid-template-columns:repeat(9,minmax(86px,1fr));gap:6px;margin:6px 0 8px}
.wqb-card{background:#fff;border:1px solid #e2e8f0;border-radius:6px;padding:7px 8px;box-shadow:0 1px 2px rgba(15,23,42,.035)}
.wqb-card-label{color:#7c8aa0;font-size:11px;margin-bottom:3px;white-space:nowrap}
.wqb-card-value{font-size:17px;font-weight:700;color:#1f2937}
.wqb-section{background:#fff;border:1px solid #e2e8f0;border-radius:7px;margin:8px 0;padding:10px;box-shadow:0 1px 2px rgba(15,23,42,.035)}
.wqb-section h3{margin:0 0 8px;font-size:16px;color:#263342}
.wqb-code{background:#242b3a;color:#f8fafc;border-radius:6px;padding:9px 11px;overflow:auto;font:12px/1.45 Consolas,Monaco,monospace}
.wqb-table{width:100%;border-collapse:collapse;font-size:12px}
.wqb-table th{background:#53677e;color:#fff;text-align:left;padding:7px 8px;border:0}
.wqb-table td{border-bottom:1px solid #e5e7eb;padding:6px 8px;vertical-align:top}
.wqb-table tr:nth-child(even) td{background:#f1f5f9}
.wqb-kv-grid{display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));gap:6px}
.wqb-kv{background:#f8fafc;border:1px solid #e5e7eb;border-radius:6px;padding:6px 8px;min-width:0}
.wqb-kv-label{font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0;margin-bottom:2px}
.wqb-kv-value{font-size:12px;color:#1f2937;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wqb-check-group{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.wqb-check-title{font-weight:700;font-size:13px;margin:0 0 6px}
.wqb-check{border-left:4px solid #f59e0b;background:#fff7ed;padding:7px 9px;border-radius:6px;margin:6px 0;font-size:12px}
.wqb-check.failed{border-left-color:#ef4444;background:#fef2f2}
.wqb-check.failed strong{color:#991b1b}
.wqb-check.warning strong{color:#9a3412}
.wqb-ok{border-left:4px solid #22c55e;background:#f0fdf4;padding:8px 10px;border-radius:6px;font-size:12px}
.wqb-badges{display:flex;flex-wrap:wrap;gap:8px}
.wqb-badge{background:#e0f2fe;color:#075985;border:1px solid #bae6fd;border-radius:999px;padding:4px 8px;font-size:11px}
.wqb-chart{width:100%;height:260px;background:#fff;border:1px solid #e2e8f0;border-radius:7px}
@media(max-width:1100px){.wqb-grid{grid-template-columns:repeat(3,minmax(120px,1fr))}.wqb-check-group{grid-template-columns:1fr}.wqb-kv-grid{grid-template-columns:repeat(2,minmax(150px,1fr))}}
@media(max-width:720px){.wqb-grid{grid-template-columns:repeat(2,minmax(120px,1fr))}.wqb-top{align-items:flex-start;flex-direction:column}}
</style>
"""


def render_line_chart(df: pd.DataFrame, title: str, x_col: str = "date", y_cols: list[str] | None = None) -> str:
    if df.empty:
        return f"<div class='wqb-muted'>{escape(title)}: no data</div>"
    if y_cols is None:
        y_cols = [col for col in df.columns if col != x_col and pd.api.types.is_numeric_dtype(df[col])]
    y_cols = y_cols[:3]
    if not y_cols:
        return f"<div class='wqb-muted'>{escape(title)}: no numeric columns</div>"

    plot = df.copy()
    for col in y_cols:
        plot[col] = pd.to_numeric(plot[col], errors="coerce")
    y_values = pd.concat([plot[col] for col in y_cols]).dropna()
    if y_values.empty:
        return f"<div class='wqb-muted'>{escape(title)}: no numeric values</div>"

    width, height = 980, 320
    left, right, top, bottom = 60, 24, 36, 46
    chart_w = width - left - right
    chart_h = height - top - bottom
    y_min, y_max = float(y_values.min()), float(y_values.max())
    if y_min == y_max:
        y_min -= 0.5
        y_max += 0.5
    n = max(1, len(plot) - 1)

    def sx(index: int) -> float:
        return left + index / n * chart_w

    def sy(value: float) -> float:
        return top + chart_h - (value - y_min) / (y_max - y_min) * chart_h

    colors = ["#38c7d7", "#93c94d", "#2f80ed"]
    parts = [
        f"<svg class='wqb-chart' viewBox='0 0 {width} {height}' role='img'>",
        f"<text x='{left}' y='22' style='font-size:16px;font-weight:700;fill:#263342'>{escape(title)}</text>",
    ]
    for i in range(5):
        y = top + chart_h * i / 4
        value = y_max - (y_max - y_min) * i / 4
        parts.append(f"<line x1='{left}' x2='{width-right}' y1='{y:.1f}' y2='{y:.1f}' stroke='#e5e7eb'/>")
        parts.append(f"<text x='8' y='{y+4:.1f}' font-size='11' fill='#64748b'>{value:.3g}</text>")
    for col_i, col in enumerate(y_cols):
        points = []
        for index, (_, row) in enumerate(plot.iterrows()):
            value = row[col]
            if pd.notna(value):
                points.append(f"{sx(index):.1f},{sy(float(value)):.1f}")
        if points:
            color = colors[col_i % len(colors)]
            parts.append(f"<polyline points='{' '.join(points)}' fill='none' stroke='{color}' stroke-width='2'/>")
            parts.append(f"<text x='{left + col_i * 190}' y='{height-14}' fill='{color}' font-size='12'>{escape(col)}</text>")
    parts.append("</svg>")
    return "".join(parts)


def _header(alpha_id: str, detail: dict[str, Any]) -> str:
    status = escape(str(detail.get("status") or "UNKNOWN"))
    created = escape(str(detail.get("dateCreated") or "-"))
    url = alpha_platform_url(alpha_id)
    return (
        "<div class='wqb-top'>"
        "<div class='wqb-title'>"
        f"<span class='wqb-status'>{status}</span>"
        f"<span class='wqb-id'>{escape(alpha_id)}</span>"
        f"<span class='wqb-muted'>Created {created}</span>"
        "</div>"
        f"<a class='wqb-link' href='{escape(url)}' target='_blank'>Open on WorldQuant Brain</a>"
        "</div>"
    )


def _code_panel(expression: str) -> str:
    return f"<div class='wqb-section'><h3>Code</h3><pre class='wqb-code'>{escape(expression or '-')}</pre></div>"


def _metric_cards(title: str, metrics: list[dict[str, str]]) -> str:
    cards = []
    for metric in metrics:
        cards.append(
            "<div class='wqb-card'>"
            f"<div class='wqb-card-label'>{escape(metric['label'])}</div>"
            f"<div class='wqb-card-value'>{escape(metric['value'])}</div>"
            "</div>"
        )
    return f"<div class='wqb-section'><h3>{escape(title)}</h3><div class='wqb-grid'>{''.join(cards)}</div></div>"


def _settings_table(settings: dict[str, Any]) -> str:
    return _key_value_section("Simulation Settings", settings)


def _properties_panel(properties: dict[str, Any]) -> str:
    return _key_value_section("Properties", properties)


def _key_value_section(title: str, values: dict[str, Any]) -> str:
    items = []
    for key, value in values.items():
        items.append(
            "<div class='wqb-kv'>"
            f"<div class='wqb-kv-label'>{escape(str(key))}</div>"
            f"<div class='wqb-kv-value' title='{escape(_text(value))}'>{escape(_text(value))}</div>"
            "</div>"
        )
    grid = f"<div class='wqb-kv-grid'>{''.join(items)}</div>"
    return f"<div class='wqb-section'><h3>{escape(title)}</h3>{grid}</div>"


def _checks_panel(failed_checks: list[dict[str, str]]) -> str:
    if not failed_checks:
        body = "<div class='wqb-ok'>No failed or warning checks found.</div>"
    else:
        grouped = group_attention_checks(failed_checks)
        failed_body = _check_list(grouped["failed"], "failed") or "<div class='wqb-muted'>No failed checks.</div>"
        warning_items = grouped["warning"] + grouped["other"]
        warning_body = _check_list(warning_items, "warning") or "<div class='wqb-muted'>No warning checks.</div>"
        body = (
            "<div class='wqb-check-group'>"
            f"<div><div class='wqb-check-title'>Failed ({len(grouped['failed'])})</div>{failed_body}</div>"
            f"<div><div class='wqb-check-title'>Warning / Attention ({len(warning_items)})</div>{warning_body}</div>"
            "</div>"
        )
    return f"<div class='wqb-section'><h3>IS Testing Status</h3>{body}</div>"


def _check_list(items: list[dict[str, str]], level: str) -> str:
    return "".join(
        f"<div class='wqb-check {escape(level)}'>"
        f"<strong>{escape(item['result'])}: {escape(item['name'])}</strong>"
        f"<div>{escape(item['message'])}</div>"
        "</div>"
        for item in items
    )


def _recordsets_panel(names: list[str]) -> str:
    badges = "".join(f"<span class='wqb-badge'>{escape(name)}</span>" for name in names)
    if not badges:
        badges = "<span class='wqb-muted'>No recordsets listed.</span>"
    return f"<div class='wqb-section'><h3>Available Recordsets</h3><div class='wqb-badges'>{badges}</div></div>"


def _chart_panel(series_frames: dict[str, pd.DataFrame]) -> str:
    charts = []
    chart_specs = [
        ("pnl", ["pnl", "risk-neutralized-pnl", "investability-constrained-pnl"]),
        ("daily-pnl", ["pnl"]),
        ("sharpe", ["sharpe"]),
        ("turnover", ["turnover"]),
    ]
    for name, preferred_cols in chart_specs:
        df = series_frames.get(name)
        if df is None or df.empty:
            continue
        y_cols = [col for col in preferred_cols if col in df.columns]
        charts.append(render_line_chart(df, title=name, y_cols=y_cols))
    body = "".join(charts) or "<div class='wqb-muted'>No chart recordsets loaded.</div>"
    return f"<div class='wqb-section'><h3>Chart</h3>{body}</div>"


def _yearly_table(yearly_stats: pd.DataFrame) -> str:
    if yearly_stats.empty:
        return "<div class='wqb-section'><h3>Yearly Aggregate Data</h3><div class='wqb-muted'>No yearly-stats loaded.</div></div>"
    columns = [col for col in ["year", "sharpe", "turnover", "fitness", "returns", "drawdown", "margin", "longCount", "shortCount"] if col in yearly_stats.columns]
    return f"<div class='wqb-section'><h3>Yearly Aggregate Data</h3>{_dataframe_table(yearly_stats[columns])}</div>"


def _dataframe_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    headers = "".join(f"<th>{escape(_label(col))}</th>" for col in df.columns)
    body_rows = []
    for _, row in df.head(max_rows).iterrows():
        cells = []
        for col in df.columns:
            style = METRIC_FORMATS.get(str(col), "auto")
            value = row[col]
            if style == "auto":
                rendered = escape(_text(value))
            else:
                rendered = escape(format_value(value, style))
            cells.append(f"<td>{rendered}</td>")
        body_rows.append(f"<tr>{''.join(cells)}</tr>")
    return f"<table class='wqb-table'><thead><tr>{headers}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


def _expression_from_detail(detail: dict[str, Any], selected_row: pd.Series | dict[str, Any] | None) -> str:
    regular = detail.get("regular") or {}
    expression = regular.get("code")
    if expression:
        return str(expression)
    if selected_row is not None:
        try:
            return str(selected_row.get("expression") or "")
        except AttributeError:
            return ""
    return ""


def _check_message(check: dict[str, Any]) -> str:
    for key in ["message", "description", "display", "name"]:
        value = check.get(key)
        if value:
            return _text(value)
    parts = []
    for key in ["value", "limit", "cutoff", "result"]:
        if key in check:
            parts.append(f"{key}={check.get(key)}")
    return ", ".join(parts) or _text(check)


def _label(value: Any) -> str:
    text = str(value)
    labels = {
        "longCount": "Long Count",
        "shortCount": "Short Count",
        "dateCreated": "Date Created",
        "daily-pnl": "Daily PnL",
        "yearly-stats": "Yearly Stats",
        "pnl": "PnL",
    }
    if text in labels:
        return labels[text]
    return text.replace("_", " ").replace("-", " ").title()

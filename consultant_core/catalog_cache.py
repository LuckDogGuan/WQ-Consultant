from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, cast
import json
from pathlib import Path
import re
import shutil
from typing import Iterable

import pandas as pd

from .machine_lib import get_datafield_count, get_datafields, get_datasets


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG_ROOT = PROJECT_ROOT / "data_catalog"
STANDARD_THEME_GROUPS = {
    "Analyst",
    "Broker",
    "Earnings",
    "Fundamental",
    "Imbalance",
    "Insiders",
    "Institutions",
    "Macro",
    "Model",
    "News",
    "Option",
    "Other",
}

DATASET_ID_THEME_PREFIXES = [
    ("analyst", "Analyst"),
    ("broker", "Broker"),
    ("earnings", "Earnings"),
    ("fundamental", "Fundamental"),
    ("imbalance", "Imbalance"),
    ("insider", "Insiders"),
    ("institution", "Institutions"),
    ("macro", "Macro"),
    ("model", "Model"),
    ("news", "News"),
    ("option", "Option"),
]


@dataclass(frozen=True)
class CatalogPaths:
    root: Path
    scope_excel: Path
    operator_guide_excel: Path
    datasets_excel: Path
    all_fields_excel: Path
    all_fields_full_excel: Path
    by_dataset_dir: Path
    manifest_json: Path
    readme: Path


def build_catalog_paths(
    output_root=DEFAULT_CATALOG_ROOT,
    instrument_type="EQUITY",
    region="USA",
    universe="TOP3000",
    delay=1,
) -> CatalogPaths:
    root = Path(output_root) / instrument_type / region / universe / f"delay_{delay}"
    return CatalogPaths(
        root=root,
        scope_excel=root / "scope.xlsx",
        operator_guide_excel=root / "operator_parameter_guide.xlsx",
        datasets_excel=root / "datasets.xlsx",
        all_fields_excel=root / "all_datafields.xlsx",
        all_fields_full_excel=root / "all_datafields_full.xlsx",
        by_dataset_dir=root / "by_dataset",
        manifest_json=root / "catalog_manifest.json",
        readme=root / "README.md",
    )


def safe_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value)).strip("._")
    return value or "unknown"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_manifest(path: Path) -> dict:
    if not path.exists():
        return {"datasets": {}, "last_refresh_at": None}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def normalize_records(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    records = cast(list[dict[str, Any]], df.to_dict(orient="records"))
    normalized = pd.json_normalize(records, sep=".")
    return normalized


def normalize_datafields(fields: pd.DataFrame, dataset_id: str) -> pd.DataFrame:
    normalized = normalize_records(fields)
    if "dataset_id" not in normalized.columns:
        normalized.insert(0, "dataset_id", dataset_id)
    else:
        normalized["dataset_id"] = normalized["dataset_id"].fillna(dataset_id)
    return normalized


def classify_dataset_theme(record: dict) -> str:
    category = str(record.get("category.name") or record.get("category") or "").strip()
    for theme in STANDARD_THEME_GROUPS:
        if category.lower() == theme.lower():
            return theme

    dataset_id = str(record.get("id") or record.get("dataset_id") or "").lower()
    dataset_name = str(record.get("name") or record.get("dataset.name") or "").lower()
    text = f"{dataset_id} {dataset_name}"
    for prefix, theme in DATASET_ID_THEME_PREFIXES:
        if prefix in text:
            return theme
    return "Other"


def enrich_datasets_for_classification(datasets: pd.DataFrame) -> pd.DataFrame:
    enriched = datasets.copy()
    if enriched.empty:
        return enriched
    enriched["theme_group"] = [classify_dataset_theme(record) for record in enriched.to_dict(orient="records")]
    return enriched


def enrich_datafields_for_usage(fields: pd.DataFrame) -> pd.DataFrame:
    enriched = fields.copy()
    if enriched.empty:
        return enriched

    field_type = enriched.get("type", pd.Series([""] * len(enriched))).fillna("").astype(str).str.upper()
    field_id = enriched.get("id", pd.Series([""] * len(enriched))).fillna("").astype(str)
    enriched["field_type"] = field_type
    enriched["field_usage"] = field_type.map(
        {
            "MATRIX": "direct_matrix",
            "VECTOR": "vector_to_matrix",
        }
    ).fillna("check_platform_docs")
    enriched["recommended_transform"] = field_type.map(
        {
            "MATRIX": "",
            "VECTOR": "vec_avg / vec_sum",
        }
    ).fillna("")
    enriched["alpha_input_expression"] = [
        value if kind == "MATRIX" else f"vec_avg({value})" if kind == "VECTOR" else value
        for value, kind in zip(field_id, field_type)
    ]
    enriched["vector_transform_options"] = [
        "" if kind == "MATRIX" else f"vec_avg({value}); vec_sum({value})" if kind == "VECTOR" else ""
        for value, kind in zip(field_id, field_type)
    ]
    enriched["cross_sectional_templates"] = [
        f"rank({expr}); zscore({expr}); normalize({expr})"
        for expr in enriched["alpha_input_expression"]
    ]
    enriched["time_series_templates"] = [
        f"ts_rank({expr}, 20); ts_mean({expr}, 20); ts_delta({expr}, 1)"
        for expr in enriched["alpha_input_expression"]
    ]
    enriched["group_templates"] = [
        f"group_rank({expr}, sector); group_zscore({expr}, industry)"
        for expr in enriched["alpha_input_expression"]
    ]
    enriched["recommended_expression"] = [
        f"rank({value})" if kind == "MATRIX" else f"rank(vec_avg({value}))" if kind == "VECTOR" else value
        for value, kind in zip(field_id, field_type)
    ]
    return enriched


def datafield_usage_guide() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "field_type": "MATRIX",
                "how_to_fill_alpha_parameter": "Use the field id directly as x.",
                "alpha_input_expression": "field_id",
                "cross_sectional_example": "rank(field_id)",
                "time_series_example": "ts_rank(field_id, 20)",
                "group_example": "group_rank(field_id, sector)",
                "notes": "Matrix fields are already one value per stock per day.",
            },
            {
                "field_type": "VECTOR",
                "how_to_fill_alpha_parameter": "Convert to Matrix first, then use the converted expression as x.",
                "alpha_input_expression": "vec_avg(field_id)",
                "cross_sectional_example": "rank(vec_avg(field_id))",
                "time_series_example": "ts_rank(vec_avg(field_id), 20)",
                "group_example": "group_rank(vec_avg(field_id), sector)",
                "notes": "Common transforms are vec_avg(field_id) and vec_sum(field_id). Choose based on field meaning.",
            },
        ]
    )


def operator_parameter_guide() -> pd.DataFrame:
    rows = [
        {
            "operator": "rank",
            "signature": "rank(x)",
            "category": "Cross Sectional",
            "parameter": "x",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Input signal to rank across stocks on the same day.",
            "example": "rank(close)",
            "notes": "If the source field is VECTOR, convert it first, for example rank(vec_avg(field)).",
        },
        {
            "operator": "zscore",
            "signature": "zscore(x)",
            "category": "Cross Sectional",
            "parameter": "x",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Input signal to standardize across stocks on the same day.",
            "example": "zscore(returns)",
            "notes": "Useful when magnitude matters but needs cross-sectional normalization.",
        },
        {
            "operator": "normalize",
            "signature": "normalize(x)",
            "category": "Cross Sectional",
            "parameter": "x",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Input signal to normalize across stocks.",
            "example": "normalize(cap)",
            "notes": "Often used after raw value signals.",
        },
        {
            "operator": "ts_rank",
            "signature": "ts_rank(x, d)",
            "category": "Time Series",
            "parameter": "x",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Input signal to compare with its own history.",
            "example": "ts_rank(close, 20)",
            "notes": "Use alpha_input_expression from the datafields sheet as x.",
        },
        {
            "operator": "ts_rank",
            "signature": "ts_rank(x, d)",
            "category": "Time Series",
            "parameter": "d",
            "accepted_type": "INTEGER",
            "returns_type": "MATRIX",
            "purpose": "Lookback window length in trading days.",
            "example": "20",
            "notes": "Common values: 5, 20, 60, 120, 240.",
        },
        {
            "operator": "ts_mean",
            "signature": "ts_mean(x, d)",
            "category": "Time Series",
            "parameter": "x",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Input signal whose rolling average is calculated.",
            "example": "ts_mean(volume, 20)",
            "notes": "Use after Vector fields have been converted to Matrix.",
        },
        {
            "operator": "ts_mean",
            "signature": "ts_mean(x, d)",
            "category": "Time Series",
            "parameter": "d",
            "accepted_type": "INTEGER",
            "returns_type": "MATRIX",
            "purpose": "Lookback window length in trading days.",
            "example": "20",
            "notes": "Common values: 5, 20, 60, 120, 240.",
        },
        {
            "operator": "ts_delta",
            "signature": "ts_delta(x, d)",
            "category": "Time Series",
            "parameter": "x",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Input signal whose current value is compared with its past value.",
            "example": "ts_delta(close, 1)",
            "notes": "A short d captures recent changes; a long d captures slower changes.",
        },
        {
            "operator": "ts_delta",
            "signature": "ts_delta(x, d)",
            "category": "Time Series",
            "parameter": "d",
            "accepted_type": "INTEGER",
            "returns_type": "MATRIX",
            "purpose": "Lag length in trading days.",
            "example": "1",
            "notes": "Common values: 1, 5, 20.",
        },
        {
            "operator": "group_rank",
            "signature": "group_rank(x, group)",
            "category": "Group",
            "parameter": "x",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Input signal to rank within each group.",
            "example": "group_rank(eps, sector)",
            "notes": "Use alpha_input_expression from the datafields sheet as x.",
        },
        {
            "operator": "group_rank",
            "signature": "group_rank(x, group)",
            "category": "Group",
            "parameter": "group",
            "accepted_type": "GROUP",
            "returns_type": "MATRIX",
            "purpose": "Grouping key used to compare similar stocks.",
            "example": "sector",
            "notes": "Common groups: market, sector, industry, subindustry.",
        },
        {
            "operator": "group_zscore",
            "signature": "group_zscore(x, group)",
            "category": "Group",
            "parameter": "x",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Input signal to standardize within each group.",
            "example": "group_zscore(eps, industry)",
            "notes": "Useful when sector or industry effects should be neutralized.",
        },
        {
            "operator": "group_zscore",
            "signature": "group_zscore(x, group)",
            "category": "Group",
            "parameter": "group",
            "accepted_type": "GROUP",
            "returns_type": "MATRIX",
            "purpose": "Grouping key used for within-group standardization.",
            "example": "industry",
            "notes": "Common groups: market, sector, industry, subindustry.",
        },
        {
            "operator": "vec_avg",
            "signature": "vec_avg(x)",
            "category": "Vector",
            "parameter": "x",
            "accepted_type": "VECTOR",
            "returns_type": "MATRIX",
            "purpose": "Vector field to compress into one average value per stock per day.",
            "example": "vec_avg(analyst_vector)",
            "notes": "Use this when each vector element contributes similarly.",
        },
        {
            "operator": "vec_sum",
            "signature": "vec_sum(x)",
            "category": "Vector",
            "parameter": "x",
            "accepted_type": "VECTOR",
            "returns_type": "MATRIX",
            "purpose": "Vector field to compress into one summed value per stock per day.",
            "example": "vec_sum(news_scores)",
            "notes": "Use this when total intensity or count-like magnitude matters.",
        },
        {
            "operator": "trade_when",
            "signature": "trade_when(event, alpha, exit_event)",
            "category": "Trade Control",
            "parameter": "event",
            "accepted_type": "BOOLEAN_MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Condition that controls when the alpha is active.",
            "example": "volume > ts_mean(volume, 20)",
            "notes": "The event should evaluate per stock per day.",
        },
        {
            "operator": "trade_when",
            "signature": "trade_when(event, alpha, exit_event)",
            "category": "Trade Control",
            "parameter": "alpha",
            "accepted_type": "MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Alpha signal used while event is true.",
            "example": "rank(eps)",
            "notes": "This is usually a normal alpha expression.",
        },
        {
            "operator": "trade_when",
            "signature": "trade_when(event, alpha, exit_event)",
            "category": "Trade Control",
            "parameter": "exit_event",
            "accepted_type": "BOOLEAN_MATRIX",
            "returns_type": "MATRIX",
            "purpose": "Condition that controls when to exit or stop holding the alpha.",
            "example": "abs(returns) > 0.1",
            "notes": "Use -1 when no explicit exit condition is needed.",
        },
    ]
    return pd.DataFrame(rows)


def optimize_datafields_for_excel(fields: pd.DataFrame, include_dataset_id=True) -> pd.DataFrame:
    optimized = fields.copy()
    drop_columns = ["fetched_at", "region", "delay", "universe"]
    if not include_dataset_id:
        drop_columns.append("dataset_id")
        drop_columns.extend(["dataset.id", "dataset.name"])
    return optimized.drop(columns=drop_columns, errors="ignore")


def datasets_requiring_refresh(datasets: pd.DataFrame, manifest: dict, force=False) -> list[str]:
    if force:
        return datasets["id"].dropna().astype(str).tolist()

    manifest_datasets = manifest.get("datasets", {})
    refresh_ids = []
    for record in datasets.to_dict(orient="records"):
        dataset_id = str(record.get("id", ""))
        if not dataset_id:
            continue

        current_count = record.get("field_count")
        cached_count = manifest_datasets.get(dataset_id, {}).get("field_count")
        if dataset_id not in manifest_datasets or current_count != cached_count:
            refresh_ids.append(dataset_id)

    return refresh_ids


def enrich_datasets_with_field_counts(
    session,
    datasets: pd.DataFrame,
    instrument_type="EQUITY",
    region="USA",
    universe="TOP3000",
    delay=1,
) -> pd.DataFrame:
    enriched = normalize_records(datasets)
    if enriched.empty or "id" not in enriched.columns:
        return enriched
    enriched = enrich_datasets_for_classification(enriched)

    counts = []
    for dataset_id in enriched["id"].dropna().astype(str):
        field_count = get_datafield_count(
            session,
            instrument_type=instrument_type,
            region=region,
            delay=delay,
            universe=universe,
            dataset_id=dataset_id,
        )
        counts.append({"id": dataset_id, "field_count": field_count})

    counts_df = pd.DataFrame(counts)
    return enriched.drop(columns=["field_count"], errors="ignore").merge(counts_df, on="id", how="left")


def write_excel(df: pd.DataFrame, path: Path, sheet_name="data") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with pd.ExcelWriter(path) as writer:
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    except ImportError as exc:
        raise RuntimeError(
            "Excel export requires openpyxl or XlsxWriter. "
            "Install one of them, for example: py -3 -m pip install openpyxl"
        ) from exc


def write_dataset_excel(fields: pd.DataFrame, dataset_row: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields_for_excel = optimize_datafields_for_excel(fields, include_dataset_id=False)
    try:
        with pd.ExcelWriter(path) as writer:
            fields_for_excel.to_excel(writer, sheet_name="datafields", index=False)
            fields.to_excel(writer, sheet_name="datafields_full", index=False)
            dataset_row.to_excel(writer, sheet_name="dataset_info", index=False)
            datafield_usage_guide().to_excel(writer, sheet_name="usage_guide", index=False)
            operator_parameter_guide().to_excel(writer, sheet_name="operator_params", index=False)
    except ImportError as exc:
        raise RuntimeError(
            "Excel export requires openpyxl or XlsxWriter. "
            "Install one of them, for example: py -3 -m pip install openpyxl"
        ) from exc


def workbook_has_required_sheets(path: Path) -> bool:
    try:
        sheets = set(pd.ExcelFile(path).sheet_names)
    except Exception:
        return False
    return {"datafields", "datafields_full", "dataset_info", "usage_guide", "operator_params"}.issubset(sheets)


def upgrade_cached_workbooks(paths: CatalogPaths, datasets: pd.DataFrame, region: str, universe: str, delay: int) -> int:
    if not paths.by_dataset_dir.exists():
        return 0

    upgraded = 0
    dataset_by_id = {
        str(record.get("id")): pd.DataFrame([record])
        for record in datasets.to_dict(orient="records")
        if record.get("id") is not None
    }
    for path in paths.by_dataset_dir.glob("*.xlsx"):
        if workbook_has_required_sheets(path):
            continue
        dataset_id = path.stem
        try:
            fields = pd.read_excel(path, sheet_name="datafields")
        except Exception:
            continue
        fields["dataset_id"] = dataset_id
        fields["region"] = region
        fields["universe"] = universe
        fields["delay"] = delay
        dataset_row = dataset_by_id.get(dataset_id, pd.DataFrame([{"id": dataset_id}]))
        if "dataset.id" not in fields.columns:
            fields["dataset.id"] = dataset_id
        if "dataset.name" not in fields.columns and "name" in dataset_row.columns:
            fields["dataset.name"] = dataset_row.iloc[0].get("name")
        fields = enrich_datafields_for_usage(fields)
        if "fetched_at" in fields.columns:
            fields = fields.drop(columns=["fetched_at"])
        fields.insert(0, "fetched_at", utc_now_iso())
        write_dataset_excel(fields, dataset_row, path)
        upgraded += 1
    return upgraded


def sync_manifest_from_cache(paths: CatalogPaths, manifest: dict) -> dict:
    manifest.setdefault("datasets", {})
    if not paths.by_dataset_dir.exists():
        return manifest

    for path in paths.by_dataset_dir.glob("*.xlsx"):
        if not workbook_has_required_sheets(path):
            continue
        try:
            fields = pd.read_excel(path, sheet_name="datafields")
        except Exception:
            continue
        manifest["datasets"][path.stem] = {
            "field_count": int(len(fields)),
            "last_refresh_at": manifest.get("datasets", {}).get(path.stem, {}).get("last_refresh_at") or utc_now_iso(),
        }
    return manifest


def write_scope_excel(paths: CatalogPaths, manifest: dict) -> None:
    scope = pd.DataFrame(
        [
            {"key": "instrument_type", "value": manifest.get("instrument_type")},
            {"key": "region", "value": manifest.get("region")},
            {"key": "universe", "value": manifest.get("universe")},
            {"key": "delay", "value": manifest.get("delay")},
            {"key": "dataset_count", "value": manifest.get("dataset_count", 0)},
            {"key": "cached_dataset_count", "value": manifest.get("cached_dataset_count", 0)},
            {"key": "datafield_count", "value": manifest.get("datafield_count", 0)},
            {"key": "last_refresh_at", "value": manifest.get("last_refresh_at")},
        ]
    )
    write_excel(scope, paths.scope_excel, "scope")
    write_excel(operator_parameter_guide(), paths.operator_guide_excel, "operator_params")


def combine_cached_datafields(by_dataset_dir: Path, sheet_name="datafields") -> pd.DataFrame:
    frames = []
    for path in sorted(by_dataset_dir.glob("*.xlsx")):
        try:
            fields = pd.read_excel(path, sheet_name=sheet_name)
        except ValueError:
            fields = pd.read_excel(path, sheet_name="datafields")
        dataset_id = path.stem
        if "dataset_id" not in fields.columns:
            fields.insert(0, "dataset_id", dataset_id)
        frames.append(fields)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def refresh_catalog(
    session,
    output_root=DEFAULT_CATALOG_ROOT,
    instrument_type="EQUITY",
    region="USA",
    universe="TOP3000",
    delay=1,
    force=False,
    dataset_ids: Iterable[str] | None = None,
) -> dict:
    paths = build_catalog_paths(output_root, instrument_type, region, universe, delay)
    paths.by_dataset_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(paths.manifest_json)
    all_datasets = normalize_records(
        get_datasets(
            session,
            instrument_type=instrument_type,
            region=region,
            delay=delay,
            universe=universe,
        )
    )

    selected_ids = None if dataset_ids is None else {str(item) for item in dataset_ids}
    datasets = all_datasets.copy()
    if selected_ids is not None:
        datasets = datasets[datasets["id"].astype(str).isin(selected_ids)].copy()

    datasets = enrich_datasets_with_field_counts(
        session,
        datasets,
        instrument_type=instrument_type,
        region=region,
        universe=universe,
        delay=delay,
    )
    all_datasets = enrich_datasets_for_classification(all_datasets)
    all_datasets = all_datasets.drop(columns=["field_count"], errors="ignore")
    upgraded_count = upgrade_cached_workbooks(paths, all_datasets, region, universe, delay)
    if upgraded_count:
        manifest["last_schema_upgrade_at"] = utc_now_iso()
    manifest = sync_manifest_from_cache(paths, manifest)
    manifest_counts = pd.DataFrame(
        [
            {"id": dataset_id, "cached_field_count": record.get("field_count")}
            for dataset_id, record in manifest.get("datasets", {}).items()
        ]
    )
    if not manifest_counts.empty:
        all_datasets = all_datasets.merge(manifest_counts, on="id", how="left")
    all_datasets = all_datasets.merge(
        datasets[["id", "field_count"]],
        on="id",
        how="left",
    )
    if "cached_field_count" in all_datasets.columns:
        all_datasets["field_count"] = all_datasets["field_count"].fillna(all_datasets["cached_field_count"])
        all_datasets = all_datasets.drop(columns=["cached_field_count"])

    refresh_ids = datasets_requiring_refresh(datasets, manifest, force=force)
    if selected_ids is not None:
        refresh_ids = [dataset_id for dataset_id in refresh_ids if dataset_id in selected_ids]

    fetched_at = utc_now_iso()
    for dataset_id in refresh_ids:
        fields = get_datafields(
            session,
            instrument_type=instrument_type,
            region=region,
            delay=delay,
            universe=universe,
            dataset_id=dataset_id,
        )
        fields = normalize_datafields(fields, dataset_id=dataset_id)
        fields = enrich_datafields_for_usage(fields)
        fields.insert(0, "fetched_at", fetched_at)
        dataset_row = datasets[datasets["id"].astype(str).eq(dataset_id)].copy()
        write_dataset_excel(fields, dataset_row, paths.by_dataset_dir / f"{safe_filename(dataset_id)}.xlsx")

        field_count = len(fields)
        datasets.loc[datasets["id"].astype(str).eq(dataset_id), "field_count"] = field_count
        manifest.setdefault("datasets", {})[dataset_id] = {
            "field_count": int(field_count),
            "last_refresh_at": fetched_at,
        }
        save_manifest(paths.manifest_json, manifest)

    write_excel(all_datasets, paths.datasets_excel, "datasets")
    all_fields = combine_cached_datafields(paths.by_dataset_dir)
    all_fields_full = combine_cached_datafields(paths.by_dataset_dir, sheet_name="datafields_full")
    if not all_fields.empty:
        write_excel(optimize_datafields_for_excel(all_fields), paths.all_fields_excel, "datafields")
    if not all_fields_full.empty:
        write_excel(all_fields_full, paths.all_fields_full_excel, "datafields_full")

    manifest["last_refresh_at"] = fetched_at
    manifest["instrument_type"] = instrument_type
    manifest["region"] = region
    manifest["universe"] = universe
    manifest["delay"] = delay
    manifest["dataset_count"] = int(len(all_datasets))
    manifest["cached_dataset_count"] = int(len(list(paths.by_dataset_dir.glob("*.xlsx"))))
    manifest["datafield_count"] = int(len(all_fields_full) if not all_fields_full.empty else len(all_fields))
    save_manifest(paths.manifest_json, manifest)
    write_scope_excel(paths, manifest)
    write_catalog_readme(paths, manifest)

    return {
        "paths": paths,
        "datasets": datasets,
        "all_datasets": all_datasets,
        "refreshed_dataset_ids": refresh_ids,
        "datafield_count": len(all_fields_full) if not all_fields_full.empty else len(all_fields),
    }


def write_catalog_readme(paths: CatalogPaths, manifest: dict) -> None:
    lines = [
        "# WorldQuant Brain Data Catalog",
        "",
        "This folder is generated by `consultant/catalog_cache.py`.",
        "",
        "## Files",
        "",
        "- `datasets.xlsx`: dataset list for this instrument/region/universe/delay.",
        "- `scope.xlsx`: common scope metadata, so region/universe/delay are not repeated on every field row.",
        "- `all_datafields.xlsx`: merged data fields from cached datasets, optimized for search.",
        "- `all_datafields_full.xlsx`: merged full field metadata, preserving raw API columns plus local usage annotations.",
        "- `by_dataset/*.xlsx`: one Excel workbook per dataset id, with `datafields`, `datafields_full`, `dataset_info`, `usage_guide`, and `operator_params` sheets.",
        "- `catalog_manifest.json`: refresh metadata used for incremental updates.",
        "",
        "## Scope",
        "",
        f"- instrument_type: `{manifest.get('instrument_type')}`",
        f"- region: `{manifest.get('region')}`",
        f"- universe: `{manifest.get('universe')}`",
        f"- delay: `{manifest.get('delay')}`",
        f"- datasets: `{manifest.get('dataset_count', 0)}`",
        f"- cached datasets: `{manifest.get('cached_dataset_count', 0)}`",
        f"- datafields: `{manifest.get('datafield_count', 0)}`",
        f"- last_refresh_at: `{manifest.get('last_refresh_at')}`",
        "",
        "## Incremental Logic",
        "",
        "The manifest records each dataset id and its cached field count. A normal refresh only fetches datasets that are new or whose cached count differs. Use `force=True` to rebuild every selected dataset.",
        "",
        "When `dataset_ids` is provided, `datasets.xlsx` still stores the full dataset index for the scope, while field downloads are limited to the selected ids.",
    ]
    paths.readme.write_text("\n".join(lines) + "\n", encoding="utf-8")


def is_complete_scope(paths: CatalogPaths) -> bool:
    manifest = load_manifest(paths.manifest_json)
    dataset_count = manifest.get("dataset_count")
    cached_dataset_count = manifest.get("cached_dataset_count")
    return bool(dataset_count and cached_dataset_count and dataset_count == cached_dataset_count)


def copy_scope_cache(source: CatalogPaths, target: CatalogPaths, target_region: str, target_universe: str) -> None:
    target.root.mkdir(parents=True, exist_ok=True)
    for source_path in source.root.iterdir():
        target_path = target.root / source_path.name
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            for child in source_path.iterdir():
                child_target = target_path / child.name
                if child.is_file() and not child_target.exists():
                    shutil.copy2(child, child_target)
        elif not target_path.exists():
            shutil.copy2(source_path, target_path)

    for excel_path in list(target.by_dataset_dir.glob("*.xlsx")) + [
        target.all_fields_full_excel,
        target.all_fields_excel,
        target.datasets_excel,
    ]:
        if excel_path.exists():
            rewrite_scope_columns(excel_path, target_region, target_universe, int(target.root.name.split("_")[-1]))

    manifest = load_manifest(target.manifest_json)
    manifest["region"] = target_region
    manifest["universe"] = target_universe
    manifest["last_reused_from"] = str(source.root)
    manifest["last_reused_at"] = utc_now_iso()
    save_manifest(target.manifest_json, manifest)
    write_scope_excel(target, manifest)
    write_catalog_readme(target, manifest)


def rewrite_scope_columns(excel_path: Path, region: str, universe: str, delay: int) -> None:
    try:
        sheets = pd.read_excel(excel_path, sheet_name=None)
    except Exception:
        return

    changed = False
    for sheet_name, sheet_df in sheets.items():
        if "region" in sheet_df.columns:
            sheet_df["region"] = region
            changed = True
        if "universe" in sheet_df.columns:
            sheet_df["universe"] = universe
            changed = True
        if "delay" in sheet_df.columns:
            sheet_df["delay"] = delay
            changed = True

    if not changed:
        return

    with pd.ExcelWriter(excel_path) as writer:
        for sheet_name, sheet_df in sheets.items():
            sheet_df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

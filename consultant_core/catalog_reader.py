from __future__ import annotations

from pathlib import Path
from typing import cast

import pandas as pd


class CatalogReader:
    """Read local WorldQuant Brain catalog cache files."""

    def __init__(self, root="data_catalog"):
        self.root = Path(root)

    def scope_path(self, region, universe, delay=1, instrument_type="EQUITY") -> Path:
        return self.root / instrument_type / region / universe / f"delay_{delay}"

    def dataset_path(self, dataset_id, region, universe, delay=1, instrument_type="EQUITY") -> Path:
        return self.scope_path(region, universe, delay, instrument_type) / "by_dataset" / f"{dataset_id}.xlsx"

    def read_excel(self, path: Path, sheet_name=0) -> pd.DataFrame:
        if not path.exists():
            raise FileNotFoundError(f"Catalog file not found: {path}")
        return pd.read_excel(path, sheet_name=sheet_name)

    def scope(self, region, universe, delay=1, instrument_type="EQUITY") -> pd.DataFrame:
        return self.read_excel(self.scope_path(region, universe, delay, instrument_type) / "scope.xlsx")

    def datasets(self, region, universe, delay=1, instrument_type="EQUITY") -> pd.DataFrame:
        return self.read_excel(self.scope_path(region, universe, delay, instrument_type) / "datasets.xlsx")

    def fields(self, region, universe, delay=1, instrument_type="EQUITY", full=False) -> pd.DataFrame:
        filename = "all_datafields_full.xlsx" if full else "all_datafields.xlsx"
        return self.read_excel(self.scope_path(region, universe, delay, instrument_type) / filename)

    def dataset_fields(self, dataset_id, region, universe, delay=1, instrument_type="EQUITY", full=False) -> pd.DataFrame:
        sheet_name = cast(str, "datafields_full" if full else "datafields")
        return self.read_excel(self.dataset_path(dataset_id, region, universe, delay, instrument_type), sheet_name=sheet_name)

    def dataset_info(self, dataset_id, region, universe, delay=1, instrument_type="EQUITY") -> pd.DataFrame:
        return self.read_excel(
            self.dataset_path(dataset_id, region, universe, delay, instrument_type),
            sheet_name=cast(str, "dataset_info"),
        )

    def usage_guide(self, dataset_id, region, universe, delay=1, instrument_type="EQUITY") -> pd.DataFrame:
        return self.read_excel(
            self.dataset_path(dataset_id, region, universe, delay, instrument_type),
            sheet_name=cast(str, "usage_guide"),
        )

    def dataset_operator_params(self, dataset_id, region, universe, delay=1, instrument_type="EQUITY") -> pd.DataFrame:
        return self.read_excel(
            self.dataset_path(dataset_id, region, universe, delay, instrument_type),
            sheet_name=cast(str, "operator_params"),
        )

    def operator_params(self, region, universe, delay=1, instrument_type="EQUITY") -> pd.DataFrame:
        return self.read_excel(self.scope_path(region, universe, delay, instrument_type) / "operator_parameter_guide.xlsx")

    def available_scopes(self, instrument_type="EQUITY") -> pd.DataFrame:
        path = self.root / instrument_type / "day1_scope_index.xlsx"
        if path.exists():
            return pd.read_excel(path)

        rows = []
        base = self.root / instrument_type
        if not base.exists():
            return pd.DataFrame(columns=["region", "universe", "delay"])
        for delay_dir in base.glob("*/*/delay_*"):
            rows.append(
                {
                    "region": delay_dir.parent.parent.name,
                    "universe": delay_dir.parent.name,
                    "delay": int(delay_dir.name.split("_")[-1]),
                    "path": str(delay_dir),
                }
            )
        return pd.DataFrame(rows)


def read_catalog(root="data_catalog") -> CatalogReader:
    return CatalogReader(root)

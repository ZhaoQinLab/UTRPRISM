#!/usr/bin/env python3
"""Report the accepted fixed-sequence context-switch analyses."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from common import write_result


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "reproduction_tables"


def row_to_dict(row: pd.Series) -> dict:
    return {
        key: (value.item() if hasattr(value, "item") else value)
        for key, value in row.to_dict().items()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    grid = pd.read_csv(DATA / "context_switch_threshold_grid.csv")
    top_quartile = grid[grid.threshold_percentile.eq(75)].copy()
    top_quartile = top_quartile[
        top_quartile.distance_group.isin(
            ["Low pairwise coverage distance", "High pairwise coverage distance"]
        )
    ]
    pair = pd.read_csv(DATA / "pair_disjoint_context_switch_summary.csv")
    confirmation = pair[pair.threshold_label.eq("fixed_0.0922")].copy()
    confirmation = confirmation[
        confirmation.coverage_distance_stratum.isin(
            ["Low coverage distance", "High coverage distance"]
        )
    ]
    result = {
        "development_top_abs_rs_quartile": [row_to_dict(row) for _, row in top_quartile.iterrows()],
        "pair_disjoint_fixed_threshold": [row_to_dict(row) for _, row in confirmation.iterrows()],
    }
    write_result(result, args.output)


if __name__ == "__main__":
    main()

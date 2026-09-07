#!/usr/bin/env python3
"""Recompute headline human miRNA-perturbation RPF metrics."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from common import experiment_balanced_spearman, write_result


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "reproduction_tables"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    frame = pd.read_csv(DATA / "human_perturbation_rpf_records.csv")
    estimate = experiment_balanced_spearman(
        frame, "experiment", "matched_mock_rs", "RPF_repression"
    )
    top = frame[frame.score_percentile > 0.80]
    bottom = frame[frame.score_percentile <= 0.40]
    result = {
        "n": int(len(frame)),
        "n_experiments": int(frame.experiment.nunique()),
        "experiment_balanced_spearman": estimate,
        "top_20_percent": {
            "n": int(len(top)),
            "mean_rpf_repression": float(top.RPF_repression.mean()),
        },
        "bottom_40_percent": {
            "n": int(len(bottom)),
            "mean_rpf_repression": float(bottom.RPF_repression.mean()),
        },
        "top_minus_bottom_mean_rpf_repression": float(
            top.RPF_repression.mean() - bottom.RPF_repression.mean()
        ),
    }
    write_result(result, args.output)


if __name__ == "__main__":
    main()

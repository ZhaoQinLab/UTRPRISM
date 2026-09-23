#!/usr/bin/env python3
"""Recompute frozen-model concordance in the independent GSE228542 cohorts."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from common import finite_spearman, write_result


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "reproduction_tables"


def summarize(cohort: str) -> dict:
    frame = pd.read_csv(DATA / f"independent_{cohort.lower()}_associations.csv.gz")
    stable = frame[frame.Selection_Frequency >= 0.76]
    return {
        "n_all": int(len(frame)),
        "spearman_all": finite_spearman(frame.Repression_Strength, frame.model),
        "n_sf_ge_0_76": int(len(stable)),
        "spearman_sf_ge_0_76": finite_spearman(stable.Repression_Strength, stable.model),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    write_result({"Sepsis": summarize("Sepsis"), "Healthy": summarize("Healthy")}, args.output)


if __name__ == "__main__":
    main()

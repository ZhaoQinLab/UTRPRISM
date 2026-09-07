#!/usr/bin/env python3
"""Plot reconstructed RS across UTRPRISM deciles for externally unscored candidates."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import CORAL, TEAL, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/external_database_unscored_calibration.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/unscored_candidate_calibration.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)

    set_style()
    fig, axis = plt.subplots(figsize=(3.5, 3.0))
    for cohort, color in [("sepsis", CORAL), ("healthy", TEAL)]:
        data = frame[frame.cohort.eq(cohort)].sort_values("decile")
        lower = data.median_reconstructed_rs - data.q1_reconstructed_rs
        upper = data.q3_reconstructed_rs - data.median_reconstructed_rs
        axis.errorbar(data.decile, data.median_reconstructed_rs, yerr=[lower, upper], marker="o", markersize=4, color=color, linewidth=1.3, capsize=2, label=cohort.capitalize())
    axis.set(xlabel="UTRPRISM score decile", ylabel="median reconstructed RS", xticks=range(1, 11))
    axis.legend(frameon=False)
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

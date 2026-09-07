#!/usr/bin/env python3
"""Plot ranking lift among candidates unscored by external databases."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _style import CORAL, GREY, TEAL, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/external_database_unscored_ranking_lift_summary.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/unscored_ranking_lift.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    x = np.arange(len(frame))
    width = 0.34

    set_style()
    fig, axis = plt.subplots(figsize=(3.4, 2.8))
    axis.bar(x - width / 2, 100 * frame.top_10_percent_rs_captured, width, color=[CORAL, TEAL], label="UTRPRISM top 10%")
    axis.bar(x + width / 2, 100 * frame.ideal_top_10_percent_rs_captured, width, color=GREY, alpha=0.65, label="ideal top 10%")
    axis.set(xticks=x, xticklabels=frame.cohort.str.capitalize(), ylabel="total reconstructed RS captured (%)")
    axis.legend(frameon=False)
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

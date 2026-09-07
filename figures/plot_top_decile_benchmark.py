#!/usr/bin/env python3
"""Plot development top-decile AUROC for the common held-out subset."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import GREY, NAVY, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/development_top_decile_auc.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/top_decile_benchmark.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    frame = frame[(frame.dataset == "held-out") & (frame.subset == "all-method common")].copy()
    frame = frame.sort_values("auroc")
    y = range(len(frame))
    errors = [frame.auroc - frame.ci_lo, frame.ci_hi - frame.auroc]

    set_style()
    fig, axis = plt.subplots(figsize=(3.4, 2.8))
    axis.errorbar(frame.auroc, y, xerr=errors, fmt="none", ecolor="#8A949D", elinewidth=1.3, capsize=3)
    axis.scatter(frame.auroc, y, s=44, color=[NAVY if method == "UTRPRISM" else GREY for method in frame.method], zorder=3)
    axis.axvline(0.5, color="#B9C1C8", linewidth=1, linestyle="--")
    axis.set(yticks=list(y), yticklabels=frame.method, xlabel="top-decile AUROC", xlim=(0.35, 0.9))
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

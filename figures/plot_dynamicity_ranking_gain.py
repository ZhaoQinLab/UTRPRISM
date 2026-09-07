#!/usr/bin/env python3
"""Plot coverage-dependent ranking gain across 3′UTR dynamicity strata."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _style import CORAL, GREY, TEAL, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/gene_ranking_performance.csv.gz"
ORDER = ["Static", "Moderate", "High variable"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/dynamicity_ranking_gain.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    frame = frame[(frame.n_validation_associations >= 4) & frame.primary_profile.astype(bool)]
    groups = [frame.loc[frame.dynamicity_stratum.eq(label), "delta_cindex_coverage"].dropna().to_numpy() for label in ORDER]

    set_style()
    fig, axis = plt.subplots(figsize=(3.6, 3.0))
    colors = [GREY, TEAL, CORAL]
    parts = axis.violinplot(groups, positions=np.arange(3), widths=0.72, showextrema=False)
    for body, color in zip(parts["bodies"], colors):
        body.set_facecolor(color)
        body.set_edgecolor("none")
        body.set_alpha(0.48)
    means = [values.mean() for values in groups]
    axis.scatter(np.arange(3), means, color=colors, edgecolor="#1E2933", linewidth=0.5, s=36, zorder=3)
    axis.axhline(0, color="#B9C1C8", linewidth=1, linestyle="--")
    axis.set(xticks=np.arange(3), xticklabels=ORDER, ylabel="coverage gain in C-index", ylim=(-0.55, 0.55))
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Plot human RPF repression for low- and high-ranked candidates."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import CORAL, GREY, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/human_perturbation_rpf_records.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/human_rpf_rank_groups.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    bottom = frame.loc[frame.score_percentile <= 0.40, "RPF_repression"].dropna()
    top = frame.loc[frame.score_percentile >= 0.80, "RPF_repression"].dropna()

    set_style()
    fig, axis = plt.subplots(figsize=(3.0, 3.0))
    plot = axis.boxplot([bottom, top], tick_labels=["Bottom 40%", "Top 20%"], widths=0.55, patch_artist=True, showfliers=False)
    for box, color in zip(plot["boxes"], [GREY, CORAL]):
        box.set(facecolor=color, alpha=0.78, edgecolor=color)
    for median in plot["medians"]:
        median.set(color="white", linewidth=1.5)
    axis.scatter([1, 2], [bottom.mean(), top.mean()], marker="D", s=26, color="#1E2933", zorder=3, label="mean")
    axis.axhline(0, color="#B9C1C8", linewidth=1, linestyle="--")
    axis.set_ylabel("RPF repression (log₂ units)")
    axis.legend(frameon=False, loc="upper left")
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Plot mouse RPF repression in the bottom and top UTRPRISM quintiles."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import CORAL, GREY, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/mouse_selected_analysis_records.tsv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/mouse_rpf_repression.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data, sep="\t").dropna(subset=["UTRPRISM", "tg_repression"])
    frame = frame.sort_values("UTRPRISM")
    group_size = int(len(frame) * 0.20)
    bottom = frame.head(group_size).tg_repression
    top = frame.tail(group_size).tg_repression
    effect = float(top.median() - bottom.median())

    set_style()
    fig, axis = plt.subplots(figsize=(3.0, 3.0))
    plot = axis.boxplot([bottom, top], tick_labels=["Bottom quintile", "Top quintile"], widths=0.55, patch_artist=True, showfliers=False)
    for box, color in zip(plot["boxes"], [GREY, CORAL]):
        box.set(facecolor=color, alpha=0.78, edgecolor=color)
    for median in plot["medians"]:
        median.set(color="white", linewidth=1.5)
    axis.axhline(0, color="#B9C1C8", linewidth=1, linestyle="--")
    axis.text(0.97, 0.96, f"median difference = {effect:+.3f}", transform=axis.transAxes, ha="right", va="top")
    axis.set_ylabel("RPF repression")
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

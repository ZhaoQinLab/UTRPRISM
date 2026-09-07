#!/usr/bin/env python3
"""Plot Ago-CLIP support in the bottom and top UTRPRISM quintiles."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import GREY, TEAL, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/mouse_ago_clip_candidates.tsv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/mouse_ago_clip.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data, sep="\t").dropna(subset=["utrprism", "clip_support"])
    frame = frame.sort_values("utrprism")
    group_size = len(frame) // 5
    values = [
        100 * frame.head(group_size).clip_support.mean(),
        100 * frame.tail(group_size).clip_support.mean(),
    ]

    set_style()
    fig, axis = plt.subplots(figsize=(3.0, 3.0))
    bars = axis.bar([0, 1], values, color=[GREY, TEAL], width=0.58)
    for bar, value in zip(bars, values):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 1.0, f"{value:.1f}%", ha="center", va="bottom")
    axis.set(xticks=[0, 1], xticklabels=["Bottom quintile", "Top quintile"], ylabel="Ago-CLIP-supported fraction (%)", ylim=(0, max(values) * 1.28))
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

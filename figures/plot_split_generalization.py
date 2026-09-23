#!/usr/bin/env python3
"""Plot development performance across held-out split designs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import NAVY, TEAL, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/split_robustness_summary.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/split_generalization.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    labels = frame["split"].str.replace(r" \(.*", "", regex=True)
    y = range(len(frame))

    set_style()
    fig, axis = plt.subplots(figsize=(4.0, 2.9))
    axis.hlines(y, 0, frame.global_spearman, color=TEAL, linewidth=2)
    axis.scatter(frame.global_spearman, y, s=45, color=NAVY, zorder=3)
    for yi, value in zip(y, frame.global_spearman):
        axis.text(value + 0.012, yi, f"{value:.3f}", va="center")
    axis.set(yticks=list(y), yticklabels=labels, xlabel="global Spearman R", xlim=(0, 0.6))
    axis.invert_yaxis()
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

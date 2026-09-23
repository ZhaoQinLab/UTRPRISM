#!/usr/bin/env python3
"""Reproduce the fixed-sequence context-switch threshold trajectory."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/context_switch_threshold_grid.csv"
COLORS = {
    "Low pairwise coverage distance": "#8A949D",
    "High pairwise coverage distance": "#D76C55",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/context_switch_ordering.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    frame = frame[frame.distance_group.isin(COLORS)]

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
            "font.size": 9,
            "pdf.fonttype": 42,
        }
    )
    fig, axis = plt.subplots(figsize=(3.5, 3.0))
    for label, color in COLORS.items():
        data = frame[frame.distance_group.eq(label)].sort_values("threshold_percentile")
        axis.plot(
            data.threshold_percentile,
            data.accuracy,
            marker="o",
            markersize=3.5,
            linewidth=1.5,
            color=color,
            label=label,
        )
    axis.axhline(0.5, color="#B9C1C8", linewidth=1, linestyle="--")
    axis.set_xlabel("minimum |ΔRS| percentile")
    axis.set_ylabel("gene-balanced ordering accuracy")
    axis.set_ylim(0.35, 0.82)
    axis.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, bbox_inches="tight")
    fig.savefig(args.output.with_suffix(".png"), dpi=300, bbox_inches="tight")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reproduce the continuous human RPF response plot."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "data/reproduction_tables/human_perturbation_rpf_records.csv"
COLORS = {"U2OS_miR1": "#315B8A", "U2OS_miR155": "#D76C55", "HEK293T_miR1": "#4FA6A0"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/human_rpf_response.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
            "font.size": 9,
            "pdf.fonttype": 42,
        }
    )
    fig, axis = plt.subplots(figsize=(3.3, 3.0))
    for experiment, data in frame.groupby("experiment", sort=False):
        axis.scatter(
            data.score_percentile,
            data.RPF_repression,
            s=24,
            alpha=0.8,
            edgecolor="white",
            linewidth=0.4,
            color=COLORS.get(experiment, "#8A949D"),
            label=experiment.replace("_", " "),
        )
    design = pd.get_dummies(frame.experiment, drop_first=True, dtype=float)
    matrix = np.column_stack([np.ones(len(frame)), frame.score_percentile, design.to_numpy()])
    coefficients = np.linalg.lstsq(matrix, frame.RPF_repression.to_numpy(), rcond=None)[0]
    x = np.linspace(0, 1, 100)
    mean_offset = float(coefficients[0] + (design.mean().to_numpy() @ coefficients[2:]))
    axis.plot(x, mean_offset + coefficients[1] * x, color="#1E2933", linewidth=1.5)
    axis.set_xlabel("within-experiment UTRPRISM percentile")
    axis.set_ylabel("RPF repression (log₂ units)")
    axis.legend(frameon=False, fontsize=7.5)
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, bbox_inches="tight")
    fig.savefig(args.output.with_suffix(".png"), dpi=300, bbox_inches="tight")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

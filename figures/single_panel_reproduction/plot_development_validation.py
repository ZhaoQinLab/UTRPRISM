#!/usr/bin/env python3
"""Reproduce the development-validation predicted-RS association plot."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "data/reproduction_tables/development_validation_predictions.csv.gz"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/development_validation.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    rho = float(spearmanr(frame.Repression_Strength, frame.pred).statistic)

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
            "font.size": 9,
            "pdf.fonttype": 42,
        }
    )
    fig, axis = plt.subplots(figsize=(3.25, 3.0))
    density = axis.hexbin(
        frame.pred,
        frame.Repression_Strength,
        gridsize=48,
        mincnt=1,
        cmap="Blues",
        linewidths=0,
    )
    axis.set_xlabel("predicted RS")
    axis.set_ylabel("regression-derived RS")
    axis.text(
        0.04,
        0.96,
        f"Spearman R = {rho:.3f}\nn = {len(frame):,}",
        transform=axis.transAxes,
        va="top",
    )
    colorbar = fig.colorbar(density, ax=axis, pad=0.02)
    colorbar.set_label("associations per hexbin")
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, bbox_inches="tight")
    fig.savefig(args.output.with_suffix(".png"), dpi=300, bbox_inches="tight")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

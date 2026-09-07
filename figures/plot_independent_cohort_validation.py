#!/usr/bin/env python3
"""Plot predicted versus reconstructed RS for one independent cohort."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import spearmanr

from _style import save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort", choices=["sepsis", "healthy"], required=True)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data_path = args.data or ROOT / f"data/reproduction_tables/independent_{args.cohort}_associations.csv.gz"
    output = args.output or ROOT / f"outputs/independent_{args.cohort}_validation.pdf"
    frame = pd.read_csv(data_path)
    rho = float(spearmanr(frame.model, frame.Repression_Strength).statistic)

    set_style()
    fig, axis = plt.subplots(figsize=(3.25, 3.0))
    density = axis.hexbin(frame.model, frame.Repression_Strength, gridsize=45, mincnt=1, cmap="Blues", linewidths=0)
    axis.set(xlabel="predicted RS", ylabel="independently reconstructed RS")
    axis.text(0.04, 0.96, f"Spearman R = {rho:.3f}\nn = {len(frame):,}", transform=axis.transAxes, va="top")
    colorbar = fig.colorbar(density, ax=axis, pad=0.02)
    colorbar.set_label("associations per hexbin")
    fig.tight_layout()
    save_figure(fig, output)


if __name__ == "__main__":
    main()

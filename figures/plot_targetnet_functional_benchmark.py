#!/usr/bin/env python3
"""Plot the pair-overlap-filtered human functional benchmark."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import GREY, NAVY, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/human_perturbation_targetnet_metrics.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/targetnet_functional_benchmark.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    y = range(len(frame))
    values = frame.experiment_balanced_spearman
    errors = [values - frame.gene_cluster_bootstrap_ci95_low, frame.gene_cluster_bootstrap_ci95_high - values]

    set_style()
    fig, axis = plt.subplots(figsize=(3.6, 2.5))
    axis.errorbar(values, y, xerr=errors, fmt="none", ecolor="#8A949D", elinewidth=1.4, capsize=3)
    axis.scatter(values, y, s=48, color=[NAVY, GREY], zorder=3)
    axis.axvline(0, color="#B9C1C8", linewidth=1, linestyle="--")
    axis.set(yticks=list(y), yticklabels=frame.method, xlabel="experiment-balanced Spearman R", xlim=(-0.6, 0.8))
    axis.invert_yaxis()
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

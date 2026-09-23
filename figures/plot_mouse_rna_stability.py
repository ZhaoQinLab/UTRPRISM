#!/usr/bin/env python3
"""Plot mouse RNA-stability classification curves for released model scores."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import auc, roc_curve

from _style import GREY, NAVY, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/mouse_rna_stability_locus_scores.tsv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/mouse_rna_stability.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data, sep="\t")
    outcome = frame.published_stabilized_target.astype(int)

    set_style()
    fig, axis = plt.subplots(figsize=(3.1, 3.0))
    for column, label, color in [
        ("utrprism_percentile", "UTRPRISM", NAVY),
        ("sequence_only_percentile", "sequence-only", GREY),
    ]:
        fpr, tpr, _ = roc_curve(outcome, frame[column])
        axis.plot(fpr, tpr, color=color, linewidth=1.7, label=f"{label} ({auc(fpr, tpr):.3f})")
    axis.plot([0, 1], [0, 1], color="#B9C1C8", linewidth=1, linestyle="--")
    axis.set(xlabel="false-positive rate", ylabel="true-positive rate", xlim=(0, 1), ylim=(0, 1))
    axis.legend(frameon=False, title="AUROC")
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

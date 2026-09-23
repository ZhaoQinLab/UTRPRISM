#!/usr/bin/env python3
"""Plot the effect of input-modality ablations on validation performance."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _style import NAVY, TEAL, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/modality_ablation_summary.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/modality_ablation.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    x = np.arange(len(frame))

    set_style()
    fig, axis = plt.subplots(figsize=(4.0, 3.0))
    axis.plot(x, frame.global_spearman, marker="o", color=NAVY, linewidth=1.5, label="Spearman R")
    axis.plot(x, frame.hl_auc, marker="s", color=TEAL, linewidth=1.5, label="high/low AUROC")
    axis.set_xticks(x, frame["input"], rotation=20, ha="right")
    axis.set(ylabel="performance", ylim=(0, 0.8))
    axis.legend(frameon=False)
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Plot the gene-level composite 3′UTR dynamicity distribution."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import CORAL, NAVY, TEAL, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/gene_utr_dynamicity.csv.gz"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/utr_dynamicity_distribution.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data)
    low = float(frame.stratum_cut_low.dropna().iloc[0])
    high = float(frame.stratum_cut_high.dropna().iloc[0])

    set_style()
    fig, axis = plt.subplots(figsize=(3.35, 2.8))
    axis.hist(frame.dynamicity_composite.dropna(), bins=42, color=NAVY, alpha=0.82, edgecolor="white", linewidth=0.25)
    axis.axvline(low, color=TEAL, linewidth=1.4, linestyle="--")
    axis.axvline(high, color=CORAL, linewidth=1.4, linestyle="--")
    axis.set(xlabel="composite 3′UTR dynamicity", ylabel="genes")
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

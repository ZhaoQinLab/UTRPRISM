#!/usr/bin/env python3
"""Plot the selection-frequency distribution used to define stable labels."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import CORAL, NAVY, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/label_selection_frequency.csv.gz"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/selection_frequency.pdf")
    args = parser.parse_args()
    values = pd.read_csv(args.data)["SF"].dropna()

    set_style()
    fig, axis = plt.subplots(figsize=(3.25, 2.8))
    axis.hist(values, bins=40, color=NAVY, alpha=0.82, edgecolor="white", linewidth=0.25)
    axis.axvline(0.76, color=CORAL, linewidth=1.5, linestyle="--", label="SF = 0.76")
    axis.set(xlabel="selection frequency (SF)", ylabel="associations")
    axis.legend(frameon=False)
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

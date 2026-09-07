#!/usr/bin/env python3
"""Plot the mean predicted-score change under local input perturbations."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import CORAL, NAVY, clean_axis, save_figure, set_style


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/reproduction_tables/input_perturbation_summary.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/input_perturbations.pdf")
    args = parser.parse_args()
    frame = pd.read_csv(args.data).sort_values("mean_drop")
    colors = [CORAL if value > 0 else NAVY for value in frame.mean_drop]

    set_style()
    fig, axis = plt.subplots(figsize=(4.0, 2.9))
    axis.barh(frame.perturbation, frame.mean_drop, color=colors, alpha=0.82)
    axis.axvline(0, color="#B9C1C8", linewidth=1)
    axis.set_xlabel("mean reduction in predicted RS")
    clean_axis(axis)
    fig.tight_layout()
    save_figure(fig, args.output)


if __name__ == "__main__":
    main()

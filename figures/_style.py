"""Shared visual settings for standalone UTRPRISM plots."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


NAVY = "#315B8A"
TEAL = "#4FA6A0"
CORAL = "#D76C55"
ORANGE = "#D98A45"
PURPLE = "#8A68AA"
GREY = "#8A949D"
LIGHT_GREY = "#D8DEE4"
DARK = "#1E2933"


def set_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "axes.titleweight": "bold",
            "axes.edgecolor": DARK,
            "axes.linewidth": 0.8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def clean_axis(axis) -> None:
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.tick_params(width=0.8, length=3)


def save_figure(fig, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight")
    preview = output.with_suffix(".png")
    fig.savefig(preview, dpi=300, bbox_inches="tight")
    print(f"Wrote {output}")
    print(f"Wrote {preview}")

#!/usr/bin/env python3
"""Recompute the three headline human-to-mouse transfer readouts."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu
from sklearn.metrics import roc_auc_score

from common import write_result


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "reproduction_tables"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    stability = pd.read_csv(DATA / "mouse_rna_stability_locus_scores.tsv", sep="\t")
    stability = stability.dropna(
        subset=["published_stabilized_target", "utrprism_percentile", "sequence_only_percentile"]
    )
    labels = stability.published_stabilized_target.astype(int)
    utrprism_auc = float(roc_auc_score(labels, stability.utrprism_percentile))
    sequence_auc = float(roc_auc_score(labels, stability.sequence_only_percentile))

    selected = pd.read_csv(DATA / "mouse_selected_analysis_records.tsv", sep="\t")
    rpf = selected[selected.dataset.eq("GSE83684")].dropna(
        subset=["UTRPRISM", "tg_repression"]
    ).sort_values("UTRPRISM")
    group_size = int(len(rpf) * 0.20)
    rpf_low = rpf.head(group_size).tg_repression
    rpf_high = rpf.tail(group_size).tg_repression

    clip = pd.read_csv(DATA / "mouse_ago_clip_candidates.tsv", sep="\t")
    clip = clip.dropna(subset=["utrprism", "clip_support"]).sort_values("utrprism")
    clip_group_size = len(clip) // 5
    clip_low = clip.head(clip_group_size).clip_support.astype(bool)
    clip_high = clip.tail(clip_group_size).clip_support.astype(bool)
    contingency = [
        [int(clip_high.sum()), int((~clip_high).sum())],
        [int(clip_low.sum()), int((~clip_low).sum())],
    ]
    odds_ratio, fisher_p = fisher_exact(contingency, alternative="greater")

    result = {
        "rna_stability": {
            "n": int(len(stability)),
            "positive_targets": int(labels.sum()),
            "utrprism_auroc": utrprism_auc,
            "sequence_only_auroc": sequence_auc,
            "delta_auroc": utrprism_auc - sequence_auc,
        },
        "rpf_repression": {
            "n": int(len(rpf)),
            "n_per_quintile": group_size,
            "top_median": float(rpf_high.median()),
            "bottom_median": float(rpf_low.median()),
            "top_minus_bottom_median": float(rpf_high.median() - rpf_low.median()),
            "mann_whitney_p_one_sided": float(
                mannwhitneyu(rpf_high, rpf_low, alternative="greater").pvalue
            ),
        },
        "ago_clip": {
            "n": int(len(clip)),
            "n_per_quintile": clip_group_size,
            "top_support_fraction": float(clip_high.mean()),
            "bottom_support_fraction": float(clip_low.mean()),
            "odds_ratio": float(odds_ratio),
            "fisher_p_one_sided": float(fisher_p),
        },
    }
    write_result(result, args.output)


if __name__ == "__main__":
    main()

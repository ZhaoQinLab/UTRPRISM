#!/usr/bin/env python3
"""Reproduce development-validation and strict-split summary metrics."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from common import finite_spearman, high_low_auc, write_result


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "reproduction_tables"


def summarize(path: Path) -> dict:
    frame = pd.read_csv(path)
    gene_auc = [
        high_low_auc(group, "Repression_Strength", "pred")
        for _, group in frame.groupby("Gene_ID", sort=False)
    ]
    gene_auc = [value for value in gene_auc if np.isfinite(value)]
    return {
        "n_associations": int(len(frame)),
        "n_genes": int(frame.Gene_ID.nunique()),
        "n_mirnas": int(frame.miRNA_ID.nunique()),
        "global_spearman": finite_spearman(frame.Repression_Strength, frame.pred),
        "mean_gene_high_low_auc": float(np.mean(gene_auc)) if gene_auc else None,
        "n_auc_evaluable_genes": len(gene_auc),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    files = {
        "production_development_validation": "development_validation_predictions.csv.gz",
        "separately_trained_association_random": "association_random_split_predictions.csv.gz",
        "pair_disjoint": "pair_disjoint_predictions.csv.gz",
        "gene_disjoint": "gene_disjoint_predictions.csv.gz",
    }
    write_result({name: summarize(DATA / path) for name, path in files.items()}, args.output)


if __name__ == "__main__":
    main()

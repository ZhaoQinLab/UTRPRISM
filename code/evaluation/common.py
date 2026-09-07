#!/usr/bin/env python3
"""Shared statistical helpers for released evaluation scripts."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr
from sklearn.metrics import roc_auc_score


def finite_spearman(first, second) -> float:
    first = np.asarray(first, dtype=float)
    second = np.asarray(second, dtype=float)
    keep = np.isfinite(first) & np.isfinite(second)
    if keep.sum() < 3:
        return float("nan")
    return float(spearmanr(first[keep], second[keep]).statistic)


def weighted_correlation(first, second, weights) -> float:
    first = np.asarray(first, dtype=float)
    second = np.asarray(second, dtype=float)
    weights = np.asarray(weights, dtype=float)
    keep = np.isfinite(first) & np.isfinite(second) & np.isfinite(weights)
    first, second, weights = first[keep], second[keep], weights[keep]
    weights = weights / weights.sum()
    first_mean = np.sum(weights * first)
    second_mean = np.sum(weights * second)
    numerator = np.sum(weights * (first - first_mean) * (second - second_mean))
    denominator = np.sqrt(
        np.sum(weights * (first - first_mean) ** 2)
        * np.sum(weights * (second - second_mean) ** 2)
    )
    return float(numerator / denominator)


def experiment_balanced_spearman(
    frame: pd.DataFrame, experiment: str, score: str, response: str
) -> float:
    data = frame.dropna(subset=[experiment, score, response]).copy()
    data["_score_rank"] = data.groupby(experiment)[score].rank(pct=True)
    data["_response_rank"] = data.groupby(experiment)[response].rank(pct=True)
    data["_weight"] = 1.0 / data.groupby(experiment)[score].transform("size")
    return weighted_correlation(data._score_rank, data._response_rank, data._weight)


def high_low_auc(group: pd.DataFrame, observed: str, predicted: str) -> float:
    if len(group) < 8:
        return float("nan")
    values = group[observed].to_numpy(float)
    p80, p40 = np.percentile(values, [80, 40])
    keep = (values >= p80) | (values <= p40)
    labels = (values[keep] >= p80).astype(int)
    if keep.sum() < 4 or labels.min() == labels.max():
        return float("nan")
    return float(roc_auc_score(labels, group[predicted].to_numpy(float)[keep]))


def write_result(result: dict, output: Path | None) -> None:
    rendered = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {output}")
    else:
        print(rendered, end="")

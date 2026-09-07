#!/usr/bin/env python3
"""Coverage loading, normalization, and tensor preparation."""

from __future__ import annotations

from pathlib import Path

import numpy as np


TARGET_COVERED_MEAN = 20.0


def load_coverage_csv(path: str | Path) -> np.ndarray:
    """Load a one-column coverage CSV, with or without a ``coverage`` header."""
    path = Path(path)
    first_line = path.read_text(encoding="utf-8").splitlines()[0].strip()
    skiprows = 1 if first_line.lower() == "coverage" else 0
    values = np.loadtxt(path, delimiter=",", dtype=np.float32, skiprows=skiprows)
    values = np.asarray(values, dtype=np.float32).reshape(-1)
    if values.size == 0:
        raise ValueError(f"Coverage file is empty: {path}")
    if not np.all(np.isfinite(values)):
        raise ValueError("Coverage contains non-finite values")
    if np.any(values < 0):
        raise ValueError("Coverage contains negative values")
    return values


def transform_raw_coverage(
    values: np.ndarray,
    covered_mean: float,
    target_mean: float = TARGET_COVERED_MEAN,
) -> np.ndarray:
    """Apply training-time covered-mean scaling and log2(x + 1)."""
    if covered_mean <= 0:
        raise ValueError("covered_mean must be positive")
    values = np.asarray(values, dtype=np.float32)
    if np.any(values < 0) or not np.all(np.isfinite(values)):
        raise ValueError("Raw coverage must be finite and non-negative")
    return np.log2(values * (target_mean / covered_mean) + 1.0).astype(np.float32)


def coverage_tensor(values: np.ndarray, length: int = 6000) -> np.ndarray:
    """Right-pad a model-ready coverage window to ``(length, 1)``."""
    values = np.asarray(values, dtype=np.float32).reshape(-1)
    if len(values) > length:
        raise ValueError(
            f"Coverage length {len(values)} exceeds tensor length {length}; "
            "window coverage explicitly before tensor construction"
        )
    tensor = np.zeros((length, 1), dtype=np.float32)
    tensor[: len(values), 0] = values
    return tensor


def select_window(values: np.ndarray, start: int, length: int = 6000) -> np.ndarray:
    values = np.asarray(values, dtype=np.float32).reshape(-1)
    if start < 0 or start >= max(1, len(values)):
        raise ValueError(f"Invalid window start {start} for coverage length {len(values)}")
    return values[start : start + length]

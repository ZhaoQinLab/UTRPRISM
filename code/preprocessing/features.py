#!/usr/bin/env python3
"""Build the three tensors consumed by the frozen production model."""

from __future__ import annotations

import numpy as np

from coverage import coverage_tensor
from sequence import one_hot


def build_model_inputs(
    utr_sequence: str,
    coverage: np.ndarray,
    mature_mirna: str,
    utr_length: int = 6000,
    mirna_length: int = 30,
) -> dict[str, np.ndarray]:
    if len(utr_sequence) != len(coverage):
        raise ValueError(
            "The selected 3′UTR sequence and coverage window must have identical lengths"
        )
    return {
        "utr_sequence": one_hot(utr_sequence, utr_length)[None, ...],
        "utr_coverage": coverage_tensor(coverage, utr_length)[None, ...],
        "mirna_sequence": one_hot(mature_mirna, mirna_length)[None, ...],
    }

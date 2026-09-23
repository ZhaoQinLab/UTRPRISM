#!/usr/bin/env python3
"""Sequence parsing, encoding, and candidate-centred windowing."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np


CHANNELS = {"A": 0, "C": 1, "G": 2, "T": 3, "U": 3}


def read_single_fasta(path: str | Path) -> tuple[str, str]:
    """Read exactly one FASTA record and return ``(identifier, sequence)``."""
    identifier: str | None = None
    chunks: list[str] = []
    with Path(path).open(encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                if identifier is not None:
                    raise ValueError(f"Expected one FASTA record in {path}")
                identifier = line[1:].split()[0]
            elif identifier is None:
                raise ValueError(f"Sequence found before FASTA header in {path}")
            else:
                chunks.append(line)
    if identifier is None or not chunks:
        raise ValueError(f"No FASTA record found in {path}")
    return identifier, "".join(chunks).upper().replace(" ", "")


def one_hot(sequence: str, length: int) -> np.ndarray:
    """Encode A/C/G/U(T) to four channels and right-pad with zeros."""
    if len(sequence) > length:
        raise ValueError(
            f"Sequence length {len(sequence)} exceeds tensor length {length}; "
            "window the sequence explicitly before encoding"
        )
    encoded = np.zeros((length, 4), dtype=np.float32)
    for index, base in enumerate(sequence.upper()):
        channel = CHANNELS.get(base)
        if channel is not None:
            encoded[index, channel] = 1.0
    return encoded


def candidate_window_bounds(
    utr_length: int,
    site_intervals: Iterable[tuple[int, int]],
    window_length: int = 6000,
) -> tuple[int, int]:
    """Return a window centred on the complete candidate-site span.

    Coordinates are zero-based, half-open offsets on the spliced,
    transcript-oriented 3′UTR.
    """
    intervals = list(site_intervals)
    if not intervals:
        raise ValueError("At least one candidate-site interval is required")
    if utr_length < 1:
        raise ValueError("UTR length must be positive")
    if any(start < 0 or end <= start or end > utr_length for start, end in intervals):
        raise ValueError("Candidate-site interval lies outside the 3′UTR")
    centre = (min(start for start, _ in intervals) + max(end for _, end in intervals)) // 2
    start = max(0, centre - window_length // 2)
    end = min(utr_length, start + window_length)
    start = max(0, end - window_length)
    return start, end


def select_window(sequence: str, start: int, length: int = 6000) -> str:
    if start < 0 or start >= max(1, len(sequence)):
        raise ValueError(f"Invalid window start {start} for sequence length {len(sequence)}")
    return sequence[start : start + length]

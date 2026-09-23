#!/usr/bin/env python3
"""Create model-ready, spliced 3′UTR coverage from a bigWig and BED6 file."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pyBigWig

from coverage import TARGET_COVERED_MEAN, transform_raw_coverage


def load_gene_exons(path: Path, gene: str) -> list[tuple[str, int, int, str]]:
    exons: list[tuple[str, int, int, str]] = []
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            if not raw.strip() or raw.startswith("#"):
                continue
            fields = raw.rstrip("\n").split("\t")
            if len(fields) < 6:
                raise ValueError("BED input must contain at least six columns")
            if fields[3] == gene:
                exons.append((fields[0], int(fields[1]), int(fields[2]), fields[5]))
    if not exons:
        raise ValueError(f"Gene {gene!r} was not found in {path}")
    strands = {row[3] for row in exons}
    if len(strands) != 1 or strands.pop() not in {"+", "-"}:
        raise ValueError("All gene exons must share one valid strand")
    return sorted(exons, key=lambda row: row[1])


def chromosome_alias(chromosome: str, available: dict[str, int]) -> str | None:
    for candidate in (chromosome, chromosome.removeprefix("chr"), f"chr{chromosome}"):
        if candidate in available:
            return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bigwig", type=Path, required=True)
    parser.add_argument("--bed", type=Path, required=True)
    parser.add_argument("--gene", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    exons = load_gene_exons(args.bed, args.gene)
    strand = exons[0][3]
    bigwig = pyBigWig.open(str(args.bigwig))
    if bigwig is None:
        raise ValueError(f"Could not open bigWig: {args.bigwig}")
    try:
        header = bigwig.header()
        covered = float(header.get("nBasesCovered", 0) or 0)
        covered_mean = float(header.get("sumData", 0)) / covered if covered else 0.0
        if covered_mean <= 0:
            raise ValueError("bigWig covered-base mean is zero or unavailable")
        chromosomes = bigwig.chroms()
        parts: list[np.ndarray] = []
        for chromosome, start, end, _ in exons:
            actual = chromosome_alias(chromosome, chromosomes)
            if actual is None:
                raise ValueError(f"Chromosome {chromosome!r} is absent from the bigWig")
            values = np.nan_to_num(bigwig.values(actual, start, end), nan=0.0)
            parts.append(np.asarray(values, dtype=np.float32))
    finally:
        bigwig.close()

    raw = (
        np.concatenate([part[::-1] for part in parts[::-1]])
        if strand == "-"
        else np.concatenate(parts)
    )
    transformed = transform_raw_coverage(raw, covered_mean, TARGET_COVERED_MEAN)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(args.output, transformed, delimiter=",", fmt="%.8g")
    print(
        f"Wrote {len(transformed)} transcript-oriented positions to {args.output}; "
        f"source covered-base mean={covered_mean:.6g}"
    )


if __name__ == "__main__":
    main()

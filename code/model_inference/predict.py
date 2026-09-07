#!/usr/bin/env python3
"""Run one candidate-context prediction with the frozen UTRPRISM model."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

import numpy as np

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
ROOT = CODE.parent
sys.path.insert(0, str(CODE / "preprocessing"))
sys.path.insert(0, str(HERE))

from coverage import load_coverage_csv, select_window as select_coverage_window
from coverage import transform_raw_coverage
from features import build_model_inputs
from model_loader import load_production_model
from sequence import read_single_fasta, select_window as select_sequence_window


DEFAULT_MODEL = ROOT / "model" / "epoch56_production_model" / "utrprism_epoch56.keras"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--utr-fasta", type=Path, required=True)
    parser.add_argument("--coverage-csv", type=Path, required=True)
    parser.add_argument("--mirna-fasta", type=Path, required=True)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--coverage-mode", choices=("model", "raw"), default="model")
    parser.add_argument("--covered-mean", type=float)
    parser.add_argument("--window-start", type=int)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    utr_id, utr = read_single_fasta(args.utr_fasta)
    mirna_id, mirna = read_single_fasta(args.mirna_fasta)
    coverage = load_coverage_csv(args.coverage_csv)
    if len(coverage) != len(utr):
        raise ValueError(
            f"Full input lengths differ: sequence={len(utr)}, coverage={len(coverage)}"
        )
    if args.coverage_mode == "raw":
        if args.covered_mean is None:
            raise ValueError("--covered-mean is required when --coverage-mode raw")
        coverage = transform_raw_coverage(coverage, args.covered_mean)
    elif args.covered_mean is not None:
        raise ValueError("--covered-mean is only valid with --coverage-mode raw")

    if len(utr) > 6000 and args.window_start is None:
        raise ValueError("Inputs longer than 6000 require an explicit --window-start")
    start = args.window_start or 0
    utr_window = select_sequence_window(utr, start, 6000)
    coverage_window = select_coverage_window(coverage, start, 6000)
    inputs = build_model_inputs(utr_window, coverage_window, mirna)

    model = load_production_model(args.model)
    prediction = float(model.predict(inputs, verbose=0).reshape(-1)[0])
    result = {
        "utr_id": utr_id,
        "mirna_id": mirna_id,
        "window_start": start,
        "window_end": start + len(utr_window),
        "coverage_mode": args.coverage_mode,
        "predicted_rs": prediction,
        "model": args.model.name,
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()

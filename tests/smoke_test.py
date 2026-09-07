#!/usr/bin/env python3
"""Load the frozen model and verify the IL6ST reference example."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    expected = json.loads((ROOT / "data/example_inputs/expected_prediction.json").read_text())
    with (ROOT / "data/reproduction_tables/web_gene_query_il6st.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["gene"] == expected["gene"] and row["miRNA"] == expected["mirna"]
        ]
    if len(rows) != 1:
        raise SystemExit("Smoke test failed: expected one matching released result row")
    released_prediction = float(rows[0]["predicted_rs"])
    if released_prediction != expected["predicted_rs"]:
        raise SystemExit("Smoke test failed: expected prediction differs from released result")
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "prediction.json"
        command = [
            sys.executable,
            str(ROOT / "code/model_inference/predict.py"),
            "--utr-fasta",
            str(ROOT / "data/example_inputs/candidate_centered_3utr.fasta"),
            "--coverage-csv",
            str(ROOT / "data/example_inputs/coverage.csv"),
            "--mirna-fasta",
            str(ROOT / "data/example_inputs/mature_mirna.fasta"),
            "--output",
            str(output),
        ]
        subprocess.run(command, check=True)
        observed = json.loads(output.read_text())
    if not observed["utr_id"].startswith(expected["gene"] + "|"):
        raise SystemExit("Smoke test failed: unexpected 3′UTR identifier")
    if observed["mirna_id"] != expected["mirna"]:
        raise SystemExit("Smoke test failed: unexpected mature-miRNA identifier")
    difference = abs(observed["predicted_rs"] - expected["predicted_rs"])
    if difference > expected["absolute_tolerance"]:
        raise SystemExit(
            f"Smoke test failed: observed={observed['predicted_rs']}, "
            f"expected={expected['predicted_rs']}, difference={difference}"
        )
    print(
        "SMOKE TEST: PASS\n"
        f"predicted_rs={observed['predicted_rs']:.10f}\n"
        f"absolute_difference={difference:.3g}"
    )


if __name__ == "__main__":
    main()

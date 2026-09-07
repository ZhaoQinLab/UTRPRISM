#!/usr/bin/env python3
"""Fail if a public release contains forbidden or suspicious material."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


BINARY_FORBIDDEN = {".bam", ".cram", ".bw", ".bigwig", ".docx", ".pdf", ".ai", ".pptx"}
NAME_FORBIDDEN = (".fastq", ".fastq.gz", ".fq", ".fq.gz", ".gtf", ".gtf.gz")
TEXT_PATTERNS = {
    "absolute home path": re.compile(r"/ho" + r"me/"),
    "private key": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "AWS key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "password assignment": re.compile(r"(?i)password\s*[:=]"),
    # Split the historical name so this audit source does not match its own rule.
    "legacy project name": re.compile(r"(?i)\bmi" + r"rprism\b"),
}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".tsv", ".csv", ".json", ".yaml", ".yml", ".cff"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.resolve()
    problems: list[str] = []
    models: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "outputs" in path.parts:
            continue
        relative = path.relative_to(root)
        lower_name = path.name.lower()
        if path.suffix.lower() in BINARY_FORBIDDEN or lower_name.endswith(NAME_FORBIDDEN):
            problems.append(f"forbidden file type: {relative}")
        if path.stat().st_size > 100 * 1024 * 1024:
            problems.append(f"file exceeds GitHub 100 MiB limit: {relative}")
        if path.suffix.lower() in {".keras", ".h5"}:
            models.append(relative)
        if path.suffix.lower() in TEXT_SUFFIXES and path.stat().st_size <= 10 * 1024 * 1024:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                problems.append(f"non-UTF-8 text candidate: {relative}")
                continue
            for label, pattern in TEXT_PATTERNS.items():
                if pattern.search(text):
                    problems.append(f"{label}: {relative}")
    expected_model = Path("model/epoch56_production_model/utrprism_epoch56.keras")
    if models != [expected_model]:
        problems.append(f"expected exactly one production model, observed: {models}")
    required = [
        Path("README.md"),
        Path("LICENSE"),
        Path("CITATION.cff"),
        Path("data/processed/state_resolved_repression_atlas.csv.gz"),
        Path("data/reproduction_tables/development_validation_predictions.csv.gz"),
        Path("environment/environment.yml"),
        Path("model/checksum.txt"),
    ]
    for relative in required:
        if not (root / relative).is_file():
            problems.append(f"missing required release file: {relative}")
    if problems:
        print("PUBLIC RELEASE AUDIT: FAIL")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)
    print("PUBLIC RELEASE AUDIT: PASS")
    print(f"Audited root: {root}")
    print(f"Production model: {expected_model}")
    print("No forbidden raw-data, manuscript, absolute-path, credential, or legacy-name match found.")


if __name__ == "__main__":
    main()

# UTRPRISM

UTRPRISM is a context-resolved framework for microRNA target prioritization by integrating expressed 3′UTR states with sequence information.

## Overview

Sequence defines candidate miRNA–target interactions, but regulatory opportunity also depends on the 3′UTR substrate expressed in a biological context. UTRPRISM expands the prioritization unit from a static gene–miRNA pair to a gene–miRNA interaction within a coverage-defined expressed 3′UTR state.

The frozen production model integrates three tensors:

1. a candidate-centred 3′UTR sequence (6000 × 4);
2. a position-matched expressed-coverage track (6000 × 1); and
3. a mature-miRNA sequence (30 × 4).

It returns a non-negative predicted repression score (predicted RS) for ranking sequence-defined candidates within a biological context. The score is a prioritization quantity, not a calibrated causal effect size.

## Repository organization

| Directory | Contents |
| --- | --- |
| `environment/` | Conda and pip environment specifications used for release testing |
| `model/` | Frozen epoch-56 production model and public configuration |
| `code/preprocessing/` | Sequence, coverage, windowing, and tensor-construction utilities |
| `code/model_inference/` | Model deserialization and command-line inference |
| `code/evaluation/` | Reproduction of development, independent-cohort, perturbation, and mouse-transfer metrics |
| `code/utilities/` | Public-release audit utilities |
| `data/processed/` | State-resolved repression atlas and public-dataset inventory |
| `data/reproduction_tables/` | Processed tables underlying reported quantitative analyses |
| `data/example_inputs/` | IL6ST reference-coverage inference example |
| `figures/` | Standalone scripts for visualizing released results |
| `docs/` | Reproducibility and source-data manifests |

## Installation

Create the tested Conda environment:

```bash
conda env create -f environment/environment.yml
conda activate utrprism
```

Alternatively, in a Python 3.12 environment:

```bash
python -m pip install -r environment/requirements.txt
```

## Model inference

The model expects a candidate-centred 6000-nt 3′UTR window and a position-matched coverage vector. Shorter sequences are right-padded with zeros. Longer inputs require an explicit `--window-start` so that sequence and coverage are cropped identically. Mature miRNA is encoded to 30 nt. Nucleotides use A/C/G/U(T) channels; ambiguous bases are encoded as zero.

The coverage tensor used during model development was scaled to a covered-base mean of 20 and transformed as `log2(normalized coverage + 1)`. Supply model-ready values with `--coverage-mode model`, or provide untransformed values together with the source track's covered-base mean using `--coverage-mode raw --covered-mean VALUE`.

Run the included IL6ST reference-coverage example:

```bash
python code/model_inference/predict.py \
  --utr-fasta data/example_inputs/candidate_centered_3utr.fasta \
  --coverage-csv data/example_inputs/coverage.csv \
  --mirna-fasta data/example_inputs/mature_mirna.fasta \
  --output outputs/example_prediction.json
```

The JSON output contains `predicted_rs` and the exact preprocessing choices. To verify the bundled release:

```bash
python tests/smoke_test.py
```

For a full spliced track from an assembly-matched bigWig and a BED6 file of transcript-oriented 3′UTR exons:

```bash
python code/preprocessing/coverage_from_bigwig.py \
  --bigwig sample.bw --bed utr_exons.bed --gene GENE \
  --output outputs/GENE.model_coverage.csv
```

Use bigWig and BED inputs from the same genome assembly.

## Data availability

Public source datasets are listed in [`data/processed/public_datasets.csv`](data/processed/public_datasets.csv). Processed association-level and candidate-level tables used by the released workflows are provided under `data/processed/` and `data/reproduction_tables/`.

## Citation

Please cite:

> Zhao Y, Zhang J, Qu S, Deng J, Zhang F, Zhou Y, Hu S, Gu B, Zhao Q. UTRPRISM enables context-resolved microRNA target prioritization across expressed 3′UTR states.

The manuscript citation can be updated with journal, year, volume, pages, and DOI after publication.

## License

Code and documentation are released under the [MIT License](LICENSE). Public source datasets and derived tables remain subject to the terms of their original repositories and publications.

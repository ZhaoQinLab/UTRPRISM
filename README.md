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
| `model/` | Frozen epoch-56 production model, public configuration, and checksums |
| `code/preprocessing/` | Sequence, coverage, windowing, and tensor-construction utilities |
| `code/model_inference/` | Model deserialization and command-line inference |
| `code/evaluation/` | Reproduction of development, independent-cohort, perturbation, and mouse-transfer metrics |
| `code/utilities/` | Hashing and public-release audit utilities |
| `data/processed/` | State-resolved repression atlas and public-dataset inventory |
| `data/reproduction_tables/` | Processed tables underlying reported quantitative analyses |
| `data/example_inputs/` | Synthetic, privacy-safe inference example |
| `figures/single_panel_reproduction/` | Standalone scientific plot scripts without manuscript layout code |
| `docs/` | Reproducibility and source-data manifests |

Raw sequencing files, clinical metadata, reference-genome bundles, manuscript files, publication-layout code, deployment configuration, and nonproduction checkpoints are intentionally excluded.

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

TensorFlow CPU inference is sufficient for the included example. GPU use is optional.

## Model inference

The model expects a candidate-centred 6000-nt 3′UTR window and a position-matched coverage vector. Shorter sequences are right-padded with zeros. Longer inputs require an explicit `--window-start` so that sequence and coverage are cropped identically. Mature miRNA is encoded to 30 nt. Nucleotides use A/C/G/U(T) channels; ambiguous bases are encoded as zero.

The coverage tensor used during model development was scaled to a covered-base mean of 20 and transformed as `log2(normalized coverage + 1)`. Supply model-ready values with `--coverage-mode model`, or provide untransformed values together with the source track's covered-base mean using `--coverage-mode raw --covered-mean VALUE`.

Run the included synthetic example:

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

Raw bigWig and reference files are not distributed here. Users are responsible for matching the bigWig and BED assembly.

## Reproduction

Recompute the principal released metrics:

```bash
python code/evaluation/evaluate_development.py
python code/evaluation/evaluate_context_switches.py
python code/evaluation/evaluate_independent_cohort.py
python code/evaluation/evaluate_human_perturbation.py
python code/evaluation/evaluate_mouse_transfer.py
```

Generate selected standalone quantitative plots:

```bash
python figures/single_panel_reproduction/plot_development_validation.py
python figures/single_panel_reproduction/plot_context_switch_ordering.py
python figures/single_panel_reproduction/plot_functional_response.py
```

These scripts generate scientific plot content only. Full-figure composition, panel lettering, and publication artwork are intentionally not part of this repository.

Expected headline values and the source table used by each command are recorded in [`docs/reproducibility_manifest.md`](docs/reproducibility_manifest.md). File-level provenance and checksums are in [`docs/source_data_manifest.tsv`](docs/source_data_manifest.tsv).

## Data availability

Public source datasets are listed in [`data/processed/public_datasets.csv`](data/processed/public_datasets.csv). Raw data are not redistributed. Processed association-level and candidate-level tables required for the released reproduction workflows are provided under `data/processed/` and `data/reproduction_tables/`.

No patient identifiers or private clinical metadata are included.

## Citation

Please cite:

> Zhao Y, Zhang J, Qu S, Deng J, Zhang F, Zhou Y, Hu S, Gu B, Zhao Q. UTRPRISM enables context-resolved microRNA target prioritization across expressed 3′UTR states.

The manuscript citation can be updated with journal, year, volume, pages, and DOI after publication. Machine-readable citation metadata are provided in [`CITATION.cff`](CITATION.cff).

## License

Code and documentation are released under the [MIT License](LICENSE). Public source datasets and derived tables remain subject to the terms of their original repositories and publications.

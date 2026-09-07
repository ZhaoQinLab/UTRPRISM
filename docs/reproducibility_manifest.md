# UTRPRISM v1.0.0 reproducibility manifest

## Frozen model

- Production checkpoint: epoch 56
- Architecture: v8g
- Selection-frequency operating point: SF ≥ 0.76
- Model parameters: 1,397,592
- Model file: `model/epoch56_production_model/utrprism_epoch56.keras`
- Expected SHA256: `a19f915e7cd4ac22c776940d8cf99d12251d7fb78d6c2d57a39f22f9d3b39f65`
- Model inputs: candidate-centred 3′UTR sequence (6000 × 4), matched coverage (6000 × 1), mature-miRNA sequence (30 × 4)
- Model output: non-negative predicted RS

## Expected reproduction checks

The commands below use the released processed tables; they do not download or redistribute raw sequencing data.

| Command | Principal expected result |
| --- | --- |
| `python code/evaluation/evaluate_development.py` | Production development-validation Spearman R ≈ 0.520 across 29,807 associations; separately trained split R values ≈ 0.516 (association-random), 0.516 (pair-disjoint), and 0.499 (gene-disjoint) |
| `python code/evaluation/evaluate_context_switches.py` | High pairwise-coverage-distance ordering accuracy 0.744 at the top |ΔRS| quartile; pair-disjoint fixed-threshold confirmation 0.593 |
| `python code/evaluation/evaluate_independent_cohort.py` | Sepsis R ≈ 0.398 across 15,655 associations and Healthy R ≈ 0.423 across 32,026 associations |
| `python code/evaluation/evaluate_human_perturbation.py` | Experiment-balanced RPF Spearman ≈ 0.371 across 77 observations; top-20% minus bottom-40% mean RPF repression ≈ +0.561 |
| `python code/evaluation/evaluate_mouse_transfer.py` | RNA-stability AUROC 0.781; RPF top-minus-bottom-quintile median difference ≈ +0.217; Ago-CLIP support 31.3% versus 18.1% with odds ratio ≈ 2.07 |

Bootstrap and permutation results are retained in their released summary tables. Re-running large resampling families can produce negligible Monte Carlo variation unless the fixed seeds and iteration counts in the original analysis are used.

## Coverage preprocessing contract

1. Use an assembly-matched coverage track.
2. Compute the source bigWig covered-base mean as `sumData / nBasesCovered`.
3. Scale raw coverage by `20 / covered-base mean`.
4. Apply `log2(x + 1)`.
5. Splice values across ordered 3′UTR exons in transcript orientation.
6. Use the candidate-site span to define a 6000-nt window; pad shorter windows with zeros.
7. Align the 3′UTR sequence and coverage positions exactly.

## Release boundaries

This release contains processed association-level/candidate-level results and scientific source code. It intentionally excludes raw FASTQ/BAM/bigWig data, patient-level clinical metadata, genome-reference packages, training tensors, alternate checkpoints, manuscript files, full-figure compositors, and deployment secrets.

The exact public-file hashes and their internal source provenance are recorded in `docs/source_data_manifest.tsv` and `model/checksum.txt`.

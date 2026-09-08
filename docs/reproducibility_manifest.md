# UTRPRISM v1.0.4 reproducibility manifest

## Frozen model

- Production checkpoint: epoch 56
- Architecture: v8g
- Selection-frequency operating point: SF ≥ 0.76
- Model parameters: 1,397,592
- Model file: `model/epoch56_production_model/utrprism_epoch56.keras`
- Model inputs: candidate-centred 3′UTR sequence (6000 × 4), matched coverage (6000 × 1), mature-miRNA sequence (30 × 4)
- Model output: non-negative predicted RS

## Expected reproduction checks

The commands below use the released processed tables.

| Command | Principal expected result |
| --- | --- |
| `python code/evaluation/evaluate_development.py` | Production development-validation Spearman R ≈ 0.520 across 29,807 associations; separately trained split R values ≈ 0.516 (association-random), 0.516 (pair-disjoint), and 0.499 (gene-disjoint) |
| `python code/evaluation/evaluate_context_switches.py` | High pairwise-coverage-distance ordering accuracy 0.744 at the top |ΔRS| quartile; pair-disjoint fixed-threshold confirmation 0.593 |
| `python code/evaluation/evaluate_independent_cohort.py` | Sepsis R ≈ 0.398 across 15,655 associations and Healthy R ≈ 0.423 across 32,026 associations |
| `python code/evaluation/evaluate_human_perturbation.py` | Experiment-balanced RPF Spearman ≈ 0.371 across 77 observations; top-20% minus bottom-40% mean RPF repression ≈ +0.561 |
| `python code/evaluation/evaluate_mouse_transfer.py` | RNA-stability AUROC 0.781; RPF top-minus-bottom-quintile median difference ≈ +0.217; Ago-CLIP support 31.3% versus 18.1% with odds ratio ≈ 2.07 |

Bootstrap and permutation results are retained in their released summary tables. Re-running large resampling families can produce negligible Monte Carlo variation unless the fixed seeds and iteration counts in the original analysis are used.

## Standalone visualizations

The `figures/` directory contains independent plotting scripts for the following released analyses:

| Analysis | Script | Released input table |
| --- | --- | --- |
| Selection-frequency distribution | `figures/plot_selection_frequency.py` | `label_selection_frequency.csv.gz` |
| Development validation | `figures/plot_development_validation.py` | `development_validation_predictions.csv.gz` |
| Split generalization | `figures/plot_split_generalization.py` | `split_robustness_summary.csv` |
| Input-modality ablation | `figures/plot_modality_ablation.py` | `modality_ablation_summary.csv` |
| Local input perturbations | `figures/plot_input_perturbations.py` | `input_perturbation_summary.csv` |
| Top-decile method benchmark | `figures/plot_top_decile_benchmark.py` | `development_top_decile_auc.csv` |
| 3′UTR dynamicity distribution | `figures/plot_dynamicity_distribution.py` | `gene_utr_dynamicity.csv.gz` |
| Ranking gain by dynamicity | `figures/plot_dynamicity_ranking_gain.py` | `gene_ranking_performance.csv.gz` |
| Fixed-sequence context switches | `figures/plot_context_switch_ordering.py` | `context_switch_threshold_grid.csv` |
| Independent-cohort validation | `figures/plot_independent_cohort_validation.py` | `independent_sepsis_associations.csv.gz` or `independent_healthy_associations.csv.gz` |
| Calibration among externally unscored candidates | `figures/plot_unscored_candidate_calibration.py` | `external_database_unscored_calibration.csv` |
| Ranking lift among externally unscored candidates | `figures/plot_unscored_ranking_lift.py` | `external_database_unscored_ranking_lift_summary.csv` |
| Continuous human RPF response | `figures/plot_functional_response.py` | `human_perturbation_rpf_records.csv` |
| Human RPF rank groups | `figures/plot_functional_rank_groups.py` | `human_perturbation_rpf_records.csv` |
| Pair-overlap-filtered functional benchmark | `figures/plot_targetnet_functional_benchmark.py` | `human_perturbation_targetnet_metrics.csv` |
| Mouse RNA stability | `figures/plot_mouse_rna_stability.py` | `mouse_rna_stability_locus_scores.tsv` |
| Mouse RPF repression | `figures/plot_mouse_rpf_repression.py` | `mouse_selected_analysis_records.tsv` |
| Mouse Ago-CLIP support | `figures/plot_mouse_ago_clip.py` | `mouse_ago_clip_candidates.tsv` |

Each plotting script writes one standalone result visualization. The independent-cohort script accepts `--cohort sepsis` or `--cohort healthy`.

## Coverage preprocessing contract

1. Use an assembly-matched coverage track.
2. Compute the source bigWig covered-base mean as `sumData / nBasesCovered`.
3. Scale raw coverage by `20 / covered-base mean`.
4. Apply `log2(x + 1)`.
5. Splice values across ordered 3′UTR exons in transcript orientation.
6. Use the candidate-site span to define a 6000-nt window; pad shorter windows with zeros.
7. Align the 3′UTR sequence and coverage positions exactly.

## Included inference example

The example under `data/example_inputs/` uses the human GRCh38 `IL6ST` spliced 3′UTR, mature `hsa-miR-449c-3p`, and the packaged pooled human reference coverage used for the Figure 6 gene-query workflow. Its expected predicted RS is linked to the corresponding row in `data/reproduction_tables/web_gene_query_il6st.csv`.

## Release boundaries

This release contains processed association-level and candidate-level results, scientific source code, and standalone plotting workflows. Source-table provenance is recorded in `docs/source_data_manifest.tsv`.

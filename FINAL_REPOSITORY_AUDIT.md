# Final public repository audit

Audit date: 2026-09-08 (Asia/Shanghai)

Repository: `https://github.com/ZhaoQinLab/UTRPRISM`

Release: `v1.0.1`

## Uploaded release contents

The release contains the following content classes:

- `README.md`, MIT `LICENSE`, and `CITATION.cff`;
- environment specifications tested with Python 3.12.12, TensorFlow 2.19.1, and Keras 3.12.0;
- one frozen epoch-56 production model (17,156,805 bytes);
- clean sequence, coverage, tensor-construction, model-loading, and inference code;
- evaluation code for development, context-switch, independent-cohort, human-perturbation, and mouse-transfer analyses;
- a processed state-resolved repression atlas containing 426,243 gene–miRNA–expressed-state associations;
- processed public-dataset metadata and panel-level reproduction tables for Figures 1–6 and selected Supplementary analyses;
- deterministic, synthetic example inputs and an expected inference result;
- 18 standalone plotting scripts for released quantitative results; and
- public source-data provenance, release notes, and audit utilities.

## Data Availability coverage

- [x] Processed data
- [x] Panel-level reproduction tables
- [x] Source code
- [x] Environment specifications
- [x] Figure-reproduction scripts
- [x] Frozen epoch-56 production model

## Verification results

- Public-release policy audit: PASS
- GitHub release immutability: ENABLED
- Python source compilation: PASS
- Public-file hash manifest verification: PASS
- Frozen-model deserialization and input/output signature check: PASS
- Deterministic synthetic inference smoke test: PASS (`predicted_rs = 0.10152196884155273`)
- Development evaluation: PASS (production validation Spearman R = 0.5204938984; n = 29,807)
- Fixed-sequence context-switch evaluation: PASS (high-distance top-quartile ordering accuracy = 0.7441860465)
- Independent-cohort evaluation: PASS (Sepsis R = 0.3983241153; Healthy R = 0.4230766993)
- Human-perturbation evaluation: PASS (experiment-balanced RPF Spearman = 0.3709271251; n = 77)
- Mouse-transfer evaluation: PASS (RNA-stability AUROC = 0.7812154696; RPF top-minus-bottom median = 0.2167916503; Ago-CLIP OR = 2.0678362573)
- Standalone plotting scripts: PASS
- Case-insensitive historical-name scan: PASS
- Absolute-home-path and credential-pattern scan: PASS
- Release-content and file-size scan: PASS
- Model-binary string scan for local paths, credentials, and historical project naming: PASS

## Release boundary and legal note

The repository uses the MIT License for code and documentation. Public-source datasets and derived tables remain subject to the terms of their originating repositories and publications.

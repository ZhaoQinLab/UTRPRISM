# Final public repository audit

Audit date: 2026-09-08 (Asia/Shanghai)

Repository: `https://github.com/ZhaoQinLab/UTRPRISM`

Release: `v1.0.0`

## Uploaded release contents

The exact path, byte size, and SHA256 of every release payload file other than the inventory itself are recorded in `docs/release_file_inventory.tsv`. The release contains the following bounded content classes:

- `README.md`, MIT `LICENSE`, and `CITATION.cff`;
- environment specifications tested with Python 3.12.12, TensorFlow 2.19.1, and Keras 3.12.0;
- one frozen epoch-56 production model (17,156,805 bytes; SHA256 `a19f915e7cd4ac22c776940d8cf99d12251d7fb78d6c2d57a39f22f9d3b39f65`);
- clean sequence, coverage, tensor-construction, model-loading, and inference code;
- evaluation code for development, context-switch, independent-cohort, human-perturbation, and mouse-transfer analyses;
- a processed state-resolved repression atlas containing 426,243 gene–miRNA–expressed-state associations;
- processed public-dataset metadata and panel-level reproduction tables for Figures 1–6 and selected Supplementary analyses;
- deterministic, synthetic example inputs and an expected inference result;
- three standalone scientific plotting scripts without panel letters or full-figure layout; and
- public source-data provenance, release notes, and audit utilities.

## Explicitly excluded

The release does not contain:

- FASTQ, BAM, bigWig, raw RNA-seq, raw miRNA-seq, or other raw biological data;
- patient identifiers, clinical metadata, phenotype tables, or raw genotype matrices;
- genome assemblies, annotations, alignment indices, or other large reference bundles;
- training tensors, caches, intermediate downloads, debug output, or nonproduction checkpoints;
- manuscript DOCX/PDF files, cover or response letters, graphical-abstract files, or submission QC screenshots;
- manuscript-generation, Word/PDF formatting, final-composite layout, Illustrator/SVG assembly, or panel-lettering code;
- web-server credentials, private deployment configuration, runtime uploads, logs, or personal notes.

## Data Availability coverage

- [x] Processed data
- [x] Panel-level reproduction tables
- [x] Source code
- [x] Environment specifications
- [x] Figure-reproduction scripts
- [x] Frozen epoch-56 production model

## Verification results

- Public-release policy audit: PASS
- GitHub release immutability: ENABLED before publication of `v1.0.0`
- Python source compilation: PASS
- Frozen-model SHA256 verification: PASS
- Frozen-model deserialization and input/output signature check: PASS
- Deterministic synthetic inference smoke test: PASS (`predicted_rs = 0.10152196884155273`)
- Development evaluation: PASS (production validation Spearman R = 0.5204938984; n = 29,807)
- Fixed-sequence context-switch evaluation: PASS (high-distance top-quartile ordering accuracy = 0.7441860465)
- Independent-cohort evaluation: PASS (Sepsis R = 0.3983241153; Healthy R = 0.4230766993)
- Human-perturbation evaluation: PASS (experiment-balanced RPF Spearman = 0.3709271251; n = 77)
- Mouse-transfer evaluation: PASS (RNA-stability AUROC = 0.7812154696; RPF top-minus-bottom median = 0.2167916503; Ago-CLIP OR = 2.0678362573)
- Selected standalone plotting scripts: PASS
- Case-insensitive historical-name scan: PASS
- Absolute-home-path and credential-pattern scan: PASS
- Forbidden-extension and file-size scan: PASS
- Model-binary string scan for local paths, credentials, and historical project naming: PASS

## Release boundary and legal note

The repository uses the MIT License for code and documentation. Public-source data and derived tables remain subject to the terms of their originating repositories and publications. The authors should confirm that MIT is consistent with institutional release policy; no third-party raw data or third-party source code is redistributed.

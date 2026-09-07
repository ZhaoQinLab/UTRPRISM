# IL6ST reference-coverage inference example

This example reproduces the `IL6ST`–`hsa-miR-449c-3p` candidate prediction used in the Figure 6 gene-query workflow.

- Species and assembly: human GRCh38 (`GCA_000001405.15`)
- 3′UTR input: spliced `IL6ST` 3′UTR, 5,987 nt
- Mature-miRNA input: `hsa-miR-449c-3p`
- Candidate site: zero-based half-open interval 3509–3530
- Coverage input: packaged pooled human reference (`tissue=all`)

The coverage vector is position-matched to the spliced 3′UTR and is already on the model input scale. The expected prediction is the value retained in `data/reproduction_tables/web_gene_query_il6st.csv`; small platform-dependent floating-point differences are accepted by the smoke test.

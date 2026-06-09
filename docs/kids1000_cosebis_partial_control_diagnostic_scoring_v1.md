# KiDS-1000 COSEBIs Partial-Control Diagnostic Scoring v1

This is the first caveated diagnostic score for the three-mask partial-control
route. It is not endpoint validation and not a population lensing claim.

The score uses:

- the retained 300-row KiDS COSEBIs `En` data vector for scoring only;
- the full 300 x 300 `COVMAT` covariance via Cholesky solve;
- the predeclared 300 x 6 partial-control design matrix;
- one nonnegative amplitude per predeclared branch.

The score does not use KiDS data-vector values for source selection, branch
selection, label selection, mask selection, or weight selection. It also uses no
posterior chains and no post-hoc residual labels.

Output artifacts:

```text
data/source_manifest/kids1000_cosebis_partial_control_diagnostic_scoring_v1.csv
data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_grid.csv
data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_summary.csv
```

The result is a diagnostic partial-control score only. `endpoint_scoring_allowed`
remains `false`.

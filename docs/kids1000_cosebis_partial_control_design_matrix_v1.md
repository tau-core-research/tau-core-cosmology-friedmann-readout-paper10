# KiDS-1000 COSEBIs Partial-Control Design Matrix v1

This artifact reduces the `900` source-only partial-control mapping values to
a `300`-row diagnostic branch matrix. It is a scoring-facing support artifact,
not a score.

Branches:

```text
baseline_zero
mask_sample_0
mask_sample_98
mask_sample_195
positive_mask_mean
sign_flip_positive_mean
```

The mask branches are copied from the three source-frozen mask products. The
positive-mask mean and its sign flip are deterministic controls. No KiDS
data-vector values, posterior chains, residuals, fit statistics, likelihood
values, AIC values, or post-hoc selections are used.

Output artifacts:

```text
data/source_manifest/kids1000_cosebis_partial_control_design_matrix_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_design_matrix_v1.csv
data/derived/kids1000_cosebis_partial_control_design_matrix_v1_summary.csv
```

Both `partial_control_scoring_allowed` and `endpoint_scoring_allowed` remain
`false`.

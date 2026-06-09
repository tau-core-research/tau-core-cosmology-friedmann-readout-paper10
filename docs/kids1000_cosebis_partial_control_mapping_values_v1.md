# KiDS-1000 COSEBIs Partial-Control Mapping Values v1

This artifact freezes a source-only diagnostic mapping-value rule for the
three-mask partial-control route. It is not an endpoint mapping vector, not a
COSEBIs theory vector, not a residual, not a likelihood, and not validation.

The frozen formula is:

```text
partial_mapping_value =
    source_mask_shell_value
    * normalized_pair_mean_z_weight
    * mode_decay_weight
```

where `normalized_pair_mean_z_weight` is computed from the source-frozen
KiDS `NZ_SOURCE` mean-redshift inventory and `mode_decay_weight = mode^{-1/2}`
is computed from the COSEBIs row structure. The rule uses no KiDS data-vector
values, posterior chains, residuals, fit statistics, or post-hoc selections.

Output artifacts:

```text
data/source_manifest/kids1000_cosebis_partial_control_mapping_values_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_values_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_values_v1_summary.csv
```

The resulting `900` rows support future partial-control diagnostics only.
Both `partial_control_scoring_allowed` and `endpoint_scoring_allowed` remain
`false`.

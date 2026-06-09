# KiDS-1000 COSEBIs E_web Null-Control Rule v1

This artifact resolves the `E_web` source-side gate only as a predeclared
null-web control. It does not provide a positive cosmic-web or environment
catalogue for the KiDS footprint.

The frozen control is:

```text
E_web(tile) = 1
```

for all 196 preferred route tiles and all 58,800 target-row by route-tile
domain rows.

This is intentionally uniform. It is therefore not a non-degenerate web signal,
not a web-anisotropy measurement, and not a validation result. Its role is to
open a path-only/projection-only control route when no source-frozen
environment catalogue is yet available.

The generated artifacts are:

```text
data/source_manifest/kids1000_cosebis_e_web_null_control_rule_policy_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_tile_rule_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_rule_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_rule_v1_summary.csv
scripts/build_kids1000_cosebis_e_web_null_control_rule_v1.py
scripts/validate_kids1000_cosebis_e_web_null_control_rule_v1.py
```

The rule forbids KiDS data-vector values, posterior chains, residuals,
fit-statistics, post-hoc sky/tile choices, post-hoc web labels, and post-hoc
path labels. Endpoint scoring remains disabled.

The next blocker after this control is the source-side normalization factor
`C_norm`. No mapping vector, theory vector, prediction, residual, or endpoint
score is computed here.

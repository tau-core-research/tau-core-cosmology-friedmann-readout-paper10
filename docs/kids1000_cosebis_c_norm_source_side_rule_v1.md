# KiDS-1000 COSEBIs C_norm Source-Side Rule v1

This gate defines the source-side normalization for the future KiDS-1000
COSEBIs path-aware weight. It is not a mapping vector, not a theory vector, and
not an endpoint score.

The rule is:

```text
C_norm = 1 / mean_domain(F_overlap * D_path * E_web)
```

where the mean is taken over the frozen 58,800-row target-row by route-tile
domain. In the current source ledger:

- `F_overlap` is the full-route pixel-fraction source factor;
- `D_path` is the caveated full-route mask-load proxy;
- `E_web` is the predeclared uniform null-web control, not a positive
  web/environment measurement.

The resulting source-side value is:

```text
C_norm = 2.110707798749
```

This normalizes the raw source factor product to unit mean over the frozen
domain. It uses no KiDS data-vector values, posterior chains, residuals,
fit-improvement flags, post-hoc tile/path/web labels, or post-hoc rule choice.

The output artifacts are:

```text
data/source_manifest/kids1000_cosebis_c_norm_source_side_rule_policy_v1.csv
data/derived/kids1000_cosebis_c_norm_source_side_domain_rule_v1.csv
data/derived/kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv
scripts/build_kids1000_cosebis_c_norm_source_side_rule_v1.py
scripts/validate_kids1000_cosebis_c_norm_source_side_rule_v1.py
```

Claim boundary: this gate makes the symbolic source-weight rule source-side
computable, but it does not build the COSEBIs mapping vector and does not
permit endpoint scoring.

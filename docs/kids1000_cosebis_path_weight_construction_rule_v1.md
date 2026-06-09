# KiDS-1000 COSEBIs Path-Weight Construction Rule v1

This gate declares, but does not yet compute, an admissible factorization for a
future source-frozen KiDS-1000 COSEBIs path-aware weight.

The declared symbolic form is:

```text
w_domain(row,tile)
  = N_pair(row)
    * T_tile(tile)
    * F_overlap(row,tile)
    * D_path(tile)
    * E_web(tile)
    * C_norm
```

where:

- `N_pair(row)` is a tomographic/redshift-kernel factor,
- `T_tile(tile)` is a route-tile availability/coordinate factor,
- `F_overlap(row,tile)` is a source-frozen full-route pixel-fraction overlap
  support factor,
- `D_path(tile)` is a caveated full-route mask-load proxy,
- `E_web(tile)` is currently a uniform null-web control, not a positive
  web/environment measurement,
- `C_norm` is the source-side unit-mean normalization of the frozen `F_overlap * D_path * E_web` product over the 58,800-row domain.

Current status:

- `N_pair` and `T_tile` have source-side support;
- `F_overlap` has non-degenerate source-side support from the full-route
  pixel-fraction rule over all 196 route masks;
- `D_path` has non-degenerate source-side support from the full-route mask-load
  proxy over all 196 route masks, but it is not a calibrated depth map;
- `E_web` is source-supported only as a uniform null-web control with no
  positive web claim;
- `C_norm = 2.110707798749` is source-side resolved, so the symbolic source-weight rule is computable as a source ledger;
- no mapping vector, theory-vector element, prediction, residual, likelihood
  value, or endpoint score is computed here.

Endpoint leakage remains forbidden: no KiDS data-vector values, posterior
chains, residuals, fit-improvement flags, or post-hoc path labels may be used to
select this rule or its future factor values.

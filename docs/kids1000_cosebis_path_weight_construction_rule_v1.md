# KiDS-1000 COSEBIs Path-Weight Construction Rule v1

This gate declares, but does not compute, an admissible factorization for a
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
- `F_overlap(row,tile)` is a footprint/row-to-tile overlap factor,
- `D_path(tile)` is a future depth/mask/path-load factor,
- `E_web(tile)` is a future web/environment factor,
- `C_norm` is a future normalization rule.

The current gate only records which factors have source-side support and which
factors remain missing or non-promotable. `F_overlap` now has a source-frozen
header-footprint rule candidate, but the degeneracy audit shows that this rule
is uniform across all 196 route tiles. It therefore remains blocking for
non-degenerate endpoint mapping until a pixel-mask or sub-tile overlap rule is
derived. This gate does not compute any numeric path weights, mapping vector,
theory-vector element, prediction, residual, likelihood value, or endpoint
score.

Endpoint leakage remains forbidden: no KiDS data-vector values, posterior
chains, residuals, fit-improvement flags, or post-hoc path labels may be used to
select this rule or its future factor values.

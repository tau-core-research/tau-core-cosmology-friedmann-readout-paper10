# KiDS-1000 COSEBIs F_overlap Pixel-Fraction Pilot v1

This is a source-only pilot, not an endpoint-scoring object.

The previous FITS-header footprint rule showed that all 196 KiDS mask products
share the same nominal WCS footprint area, so the header-only `F_overlap` proxy
is uniform and cannot support non-degenerate path mapping. This pilot checks
whether the mask pixel content itself carries non-uniform source support.

## Frozen rule

Input:

- `data/derived/kids1000_dr4_path_mask_subset_inventory_v1.csv`

Scope:

- the three committed source-mask products only,
- no endpoint data vector values,
- no posterior chains,
- no residuals,
- no post-hoc path labels,
- no path mapping.

Rule:

```text
F_overlap_pixel_fraction(tile)
  = nonzero_finite_pixel_fraction(tile)
    / max_subset(nonzero_finite_pixel_fraction)
```

This uses upstream source-mask inventory values that were already parsed from
the committed FITS masks. It does not promote the three-mask subset to a
full-route overlap rule.

## Result

The pilot is non-degenerate on the committed subset. Therefore the header
uniformity is a measurement-resolution limitation of the header-footprint proxy,
not proof that the mask source support is uniform.

## Claim boundary

This pilot motivates the next gate:

```text
promote_to_full_route_pixel_or_subtile_rule_with_streaming_cache_before_endpoint_scoring
```

It does not compute a KiDS path mapping, theory vector, prediction, residual,
fit statistic, or endpoint score.

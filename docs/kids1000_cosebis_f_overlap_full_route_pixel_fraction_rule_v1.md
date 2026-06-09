# KiDS-1000 COSEBIs F_overlap Full-Route Pixel-Fraction Rule v1

This artifact resolves the first `F_overlap` source-side blocker, but it is not
an endpoint score and not a KiDS theory-vector evaluation.

## Source-frozen rule

Input:

- `data/derived/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv`
- the 196 KiDS DR4.1 preferred-route mask products recorded there
- `data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1.csv`

Rule:

```text
F_overlap(tile)
  = nonzero_finite_pixel_fraction(tile)
    / max_full_route(nonzero_finite_pixel_fraction)
```

The rule reads source-mask pixels only. It does not read KiDS data-vector
values, posterior chains, residuals, fit statistics, post-hoc tile labels, or
post-hoc overlap choices.

The tile-level values are attached to the frozen `300 x 196 = 58,800`
target-row by route-tile domain as a source-only overlap component.

## Claim boundary

This is a non-degenerate full-route `F_overlap` source rule. It is sufficient to
move the first `F_overlap` route from "unresolved" to "source-supported" in the
readiness ledger.

It does not by itself compute:

- a full path-weight mapping,
- a theory vector,
- predictions,
- residuals,
- fit statistics,
- endpoint scores.

The next blockers are the remaining path-weight factors and non-degenerate
mapping construction.

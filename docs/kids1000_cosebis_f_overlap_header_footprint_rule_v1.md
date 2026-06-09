# KiDS-1000 COSEBIs F-overlap header-footprint rule v1

This artifact is the first source-frozen overlap rule built from the completed
196-mask route cache. It uses only FITS header/WCS metadata from the mask
products.

It is not a pixel-level mask-overlap rule, not a path mapping, not a theory
vector, and not endpoint scoring.

## Rule

For each route tile, the script reads:

- `NAXIS1`, `NAXIS2`
- `CRVAL1`, `CRVAL2`
- `CRPIX1`, `CRPIX2`
- the `CD` matrix
- `CTYPE1`, `CTYPE2`

It computes a header footprint area proxy:

```text
area_tile = |det(CD)| * NAXIS1 * NAXIS2
```

and normalizes it by the maximum route-tile area:

```text
F_overlap(tile) = area_tile / max_tile(area_tile)
```

The value is then attached deterministically to each row of the frozen
`300 x 196` COSEBIs target-row by route-tile domain.

## Claim boundary

The rule is source-native and leakage-safe: it uses no KiDS COSEBIs data-vector
values, posterior chains, residuals, fit statistics, or post-hoc tile
selection. It does not inspect the pixel-mask values, so it remains a caveated
header-footprint overlap rule. A later pixel-mask overlap derivation may
replace it if a source-frozen pixel semantics rule is accepted.

The immediate scoring implication is modest but concrete: the `F_overlap`
blocker now has a source-frozen first rule candidate. Mapping, theory-vector
construction, null controls, and endpoint scoring remain disabled.

# KiDS-1000 COSEBIs F-overlap header-footprint degeneracy audit v1

The first source-frozen header-footprint rule is intentionally audited before
any mapping or scoring promotion.

Result:

- all 196 route tiles have the same WCS header footprint area at the precision
  used by the rule;
- therefore `F_overlap(tile) = 1` for every tile;
- the rule is source-frozen and leakage-safe, but it is not a non-degenerate
  endpoint mapping support.

This is a negative/scoping result, not a failure of the acquisition route. It
shows that FITS-header area alone is too coarse: it resolves the source-cache
availability problem but does not provide the spatial variation needed for a
non-degenerate KiDS path mapping.

Next action: derive a pixel-mask or sub-tile overlap rule from source-native
mask information without reading endpoint residuals, posterior chains, or
fit-improvement flags.

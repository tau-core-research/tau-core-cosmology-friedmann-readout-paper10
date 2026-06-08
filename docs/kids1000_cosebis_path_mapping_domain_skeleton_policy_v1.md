# KiDS-1000 COSEBIs Path-Mapping Domain Skeleton Policy v1

This gate builds the full source-side domain skeleton for a future KiDS-1000
COSEBIs path-aware mapping.

The table is the Cartesian product of:

- 300 COSEBIs target rows, and
- 196 preferred KiDS DR4.1 9-band route tiles.

It therefore contains 58,800 rows. Each row records only the COSEBIs target-row
identity, source-bin redshift summaries, and filename-derived route-tile
coordinates. It does not compute tile weights, footprint overlap, depth/path
weights, web-environment labels, mapping-vector elements, theory-vector
elements, predictions, residuals, likelihood values, or endpoint scores.

This is a mapping-domain layout, not a mapping. The next scientific blocker is
still the source-frozen rule that turns tile/footprint/depth/web information
into admissible path weights without using endpoint behavior.

# KiDS-1000 COSEBIs F_overlap Resolution Decision v1

This gate records the current formal decision for the first KiDS COSEBIs
scoring blocker, `F_overlap`.

Current decision:

- no endpoint-grade `F_overlap` route is accepted;
- the official-footprint route remains unresolved because no source-frozen
  official geometry product is present;
- the full pixel-mask route is now source-cache complete in the committed
  local inventory snapshot: all 196 preferred-route masks are accounted for by
  193 ignored local-cache products plus the three committed subset masks;
- the full pixel-mask route still remains endpoint-disabled because no
  source-frozen overlap rule has been derived from those products;
- the batch-0 dry-run remains unresolved because no filled execution-review
  artifact and checksum manifest have been committed;
- the three predeclared masks are accepted only as a caveated partial path-mask
  control, not as a population endpoint overlap rule.

This artifact computes no overlap fraction, no path mapping, no theory vector,
no prediction, no residual, and no score. It exists to prevent accidental
promotion of source-cache evidence into endpoint validation.

The next `F_overlap` action is therefore no longer raw acquisition. It is to
derive a source-frozen full-mask overlap rule without reading endpoint data
values, residuals, posterior chains, or fit-improvement flags.

# KiDS-1000 COSEBIs F_overlap Resolution Decision v1

This gate records the current formal decision for the first KiDS COSEBIs
scoring blocker, `F_overlap`.

Current decision:

- no endpoint-grade `F_overlap` route is accepted;
- the official-footprint route remains unresolved because no source-frozen
  official geometry product is present;
- the full pixel-mask route remains unresolved because only 3 of 196 preferred
  route masks are source-frozen in the release package;
- the batch-0 dry-run remains unresolved because no filled execution-review
  artifact and checksum manifest have been committed;
- the three predeclared masks are accepted only as a caveated partial path-mask
  control, not as a population endpoint overlap rule.

This artifact computes no overlap fraction, no path mapping, no theory vector,
no prediction, no residual, and no score. It exists to prevent accidental
promotion of partial path-mask evidence into endpoint validation.

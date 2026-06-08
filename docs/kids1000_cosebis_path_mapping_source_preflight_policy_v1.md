# KiDS-1000 COSEBIs Path-Mapping Source Preflight Policy v1

This gate records the source-side availability state for a future KiDS-1000
COSEBIs web/path mapping.

It is deliberately not a mapping. It does not assign any mask pixel, tile,
redshift kernel, or environment observable to a COSEBIs row. It only states
which source-side ingredients are already frozen and which ingredients still
block a path-aware lensing endpoint.

The current preflight status is:

- COSEBIs target row structure is available: 300 rows from 15 tomographic pairs
  and 20 modes.
- The redshift-kernel inventory is available for the five KiDS source bins.
- The preferred KiDS DR4.1 9-band route tile inventory is available for 196
  filename-derived tile coordinates.
- A 300-row COSEBIs path-mapping design skeleton is available as a target
  layout.
- A 58,800-row target-row by route-tile domain skeleton is available as a
  mapping-domain layout.
- A symbolic path-weight construction rule is declared, but it is not yet
  computable.
- A tiny three-mask source observable shell exists, but it is partial and not a
  survey geometry mapping.
- A full source-frozen survey footprint/path/depth mapping is still missing.
- A source-frozen web/environment catalogue is still missing.
- Null-control families and seeds are declared, but controls are not executed.

This preflight forbids KiDS data-vector values, posterior chains, residuals, fit
statistics, or post-hoc sky/path labels. Endpoint scoring remains disabled.

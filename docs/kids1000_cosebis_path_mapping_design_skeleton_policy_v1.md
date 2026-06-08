# KiDS-1000 COSEBIs Path-Mapping Design Skeleton Policy v1

This gate builds a 300-row source-side design skeleton for a future KiDS-1000
COSEBIs path-aware mapping.

Each row corresponds to one COSEBIs target row: tomographic pair plus mode. The
row records source-side redshift-kernel summaries for the two tomographic bins
and the preferred DR4.1 route-tile span. It does not compute any tile weight,
path projection, theory-vector element, prediction, residual, likelihood, or
endpoint score.

The skeleton is a mapping target layout, not a mapping. The remaining blocker is
still a source-frozen rule that assigns survey footprint/path/depth and web
environment observables to these rows without using endpoint behavior.

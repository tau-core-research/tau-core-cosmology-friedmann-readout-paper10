# KiDS-1000 COSEBIs Partial-Control Mapping Shell v1

This artifact materializes the source-side shell for a future diagnostic
partial-control mapping based on the three source-frozen KiDS mask products.

It combines the 300-row COSEBIs template with the three caveated mask-control
rows, producing a `300 x 3 = 900` row support table. The table carries only
source-side mask-shell observables and row identities. It does not compute a
partial mapping value, mapping vector, theory vector, prediction, residual,
fit statistic, endpoint score, or validation result.

The shell is intentionally control-only. It cannot be interpreted as a KiDS
population endpoint overlap rule because the full 196-mask route or official
footprint geometry is still missing.

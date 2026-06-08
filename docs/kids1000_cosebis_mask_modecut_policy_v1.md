# KiDS-1000 COSEBIs Mask/Mode-Cut Policy v1

This freezes the first non-scoring data-vector mask and mode-cut policy for the
selected KiDS-1000 COSEBIs `En` data-vector table.

Frozen policy:

```text
mask policy:      retain all source rows
mode-cut policy:  retain COSEBIs modes 1..20
tomographic use:  retain all 15 upper-triangular bin pairs
retained rows:    300 / 300
```

This is intentionally conservative for leakage prevention: no tomographic pair,
mode, or row is removed based on model residuals, fit improvement, posterior
chains, or endpoint behavior. A future endpoint may predeclare a physically
motivated mode cut, but that would require a new frozen policy before scoring.

This policy does not define a theory prediction, covariance inverse, likelihood,
or Tau Core lensing amplitude.

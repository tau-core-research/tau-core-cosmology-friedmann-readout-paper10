# KiDS-1000 COSEBIs Tomographic Weight Policy v1

This freezes the first non-scoring tomographic-pair retention-weight policy for
the selected KiDS-1000 COSEBIs data vector.

Frozen policy:

```text
tomographic pairs: 15 retained pairs
rows per pair:     20 retained modes
retention weight:  1 for every pair
```

These are not likelihood weights and not fitted amplitudes. They are only
source-side retention weights that state that no tomographic pair is preferred
or downweighted using endpoint behavior, model residuals, posterior chains, or
fit improvement. The covariance matrix remains the only future source of
statistical coupling once a proper endpoint likelihood is predeclared.

This policy does not define a theory vector, covariance inverse, likelihood, or
Tau Core lensing amplitude.

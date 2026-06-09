# KiDS-1000 COSEBIs Partial-Control Scoring Protocol v1

This protocol freezes a future diagnostic scoring grammar for the caveated
three-mask `F_overlap` control route.

It is not an endpoint scoring protocol and not a validation result. It exists
only because the `F_overlap` resolution decision accepts the three source-frozen
mask products as a partial path-mask control while rejecting them as a
population endpoint overlap rule.

The future diagnostic shell is:

```text
diagnostic chi2 shell only; no population endpoint interpretation
```

A future run would still require a source-frozen partial mapping vector and
predeclared null controls before any diagnostic value could be emitted. The
present release computes no mapping vector, theory vector, residual, likelihood,
AIC value, control score, endpoint score, or validation result.

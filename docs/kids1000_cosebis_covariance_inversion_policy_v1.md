# KiDS-1000 COSEBIs Covariance Inversion Policy v1

This freezes the first non-scoring covariance-inversion policy for a future
KiDS-1000 COSEBIs lensing endpoint.

Frozen policy:

```text
covariance block:       full 300 x 300 COVMAT block
future solve method:    Cholesky solve
inverse materialization: forbidden
current inversion:      not executed
theory vector required: yes, frozen separately before scoring
```

The policy intentionally does not store an inverse covariance matrix. A future
endpoint must solve linear systems against the full covariance only after a
source-frozen theory vector, scoring protocol, and null controls are declared.

This is a numerical-readiness and leakage-prevention artifact, not a lensing
likelihood and not empirical validation.

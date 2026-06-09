# KiDS-1000 COSEBIs Endpoint Scoring Protocol v1

This protocol freezes the future endpoint scoring grammar for the KiDS-1000
COSEBIs lensing branch.

It does not execute scoring. It does not compute a theory vector, residual,
likelihood, AIC value, null-control score, or validation result.

The future scoring shell is:

```text
chi2 = (d - t)^T C^{-1} (d - t)
```

where:

- `d` is the retained 300-row COSEBIs `En` data vector;
- `C` is the full 300 x 300 covariance, solved by Cholesky without storing an
  inverse covariance;
- `t` is a future 300-row theory vector from source-frozen `W_web` and `W_path`
  mapping.

The future comparison must report:

- baseline-only branch;
- web/path candidate branch;
- wrong-channel controls;
- shuffled or rotated null controls;
- AIC delta;
- control rank.

The protocol can be interpreted only after the source-readiness ledger is green,
null controls are executed under frozen seeds, and no endpoint-leakage flag is
true. The current release fails that precondition: the first blocker remains
`F_overlap`.

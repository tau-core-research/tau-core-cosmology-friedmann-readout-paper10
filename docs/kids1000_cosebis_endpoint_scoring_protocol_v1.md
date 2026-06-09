# KiDS-1000 COSEBIs Endpoint Scoring Protocol v1

This protocol freezes the future endpoint scoring grammar for the KiDS-1000
COSEBIs lensing branch.

It does not execute scoring. The current release computes a source-frozen
unit-amplitude theory-vector shell and source-frozen null-control replay
digests. It does not compute a residual, likelihood, AIC value, null-control
score, endpoint score, or validation result.

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
true. The current release satisfies the source-readiness ledger through the
endpoint-family geometry audit: `F_overlap`, a caveated `D_path` mask-load
proxy, a uniform null-web `E_web` control, `C_norm`, a source-frozen mapping
basis, a source-frozen unit-amplitude theory-vector shell, source-frozen
null-control replay digests, and a non-degenerate endpoint-family geometry
audit are available. The first endpoint blocker is now `none`.

This document still does not execute scoring. The scoring protocol remains
frozen-not-run: no residual vector, likelihood, AIC value, null-control score,
endpoint score, or validation result is produced in this release.

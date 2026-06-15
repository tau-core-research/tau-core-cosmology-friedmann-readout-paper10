# Consolidated row-level penalized T_joint endpoint authorization package

This reviewer package collapses the previous row-level micro-gates into one
authorization artifact.  It is intended to reduce review overhead while keeping
the leakage boundary explicit.

It does **not** compute `T_joint_penalized`, does **not** run endpoint scoring,
and does **not** claim validation.  If completed and accepted by an external
reviewer, it may authorize exactly two downstream actions:

1. compute a record-only `T_joint_penalized = T_joint + lambda_row * P_row`
   ledger under the already frozen row-level formula;
2. run one guarded endpoint-scoring replay using that frozen statistic.

The package freezes:

- base `T_joint = 4.142466300799e+00`;
- `lambda_row = 1.0`;
- aligned control rows = 6;
- mean aligned control penalty = 0.109794891058.

Forbidden inputs remain endpoint residuals, endpoint scores, fit improvements,
posterior chains, and post-score control ranks.  No labels, kernels, source
proxies, amplitudes, or covariance policy may be changed after this package is
accepted.

The claim boundary is:

```text
consolidated_authorization_package_not_scoring_not_validation
```

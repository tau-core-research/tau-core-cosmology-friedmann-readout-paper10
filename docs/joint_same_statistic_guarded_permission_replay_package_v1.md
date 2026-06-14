# Joint same-statistic guarded permission replay package v1

**Doc class:** permission-only package preparation.
**Status:** ready, not executed.
**Claim boundary:** `joint_same_statistic_guarded_permission_replay_package_not_execution_not_scoring_not_validation`.

This artifact carries the completed same-statistic authorization into a
guarded package boundary.  It does not execute the joint statistic, does
not compute endpoint scores, and does not claim endpoint, cosmological,
or physical validation.

The package freezes the same-statistic requirement:

`T_joint = sum_i q_i z_i`

Any later candidate/control replay must use the same symbolic statistic,
same row scope, same `q_i` weights, same signs, same standardization rule,
and the same caveated block-diagonal covariance route.

The matched-control suite remains a frozen requirement, not an executable
scoring suite in this package.  A separate execution authorization is still
required before any replay script can run.

Carried caveats:
- no source-native cross-probe covariance product is available;
- the block-diagonal route is caveated;
- shared sky/mask, redshift-kernel, nuisance/calibration, and population
  covariance caveats remain active;
- direct scoring and validation claims remain forbidden.

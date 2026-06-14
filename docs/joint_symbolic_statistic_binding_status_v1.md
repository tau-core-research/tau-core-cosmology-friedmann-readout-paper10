# Joint symbolic statistic binding status v1

**Doc class:** post-replay binding-status ledger
**Status:** symbolic binding passed; numeric validation binding blocked
**Claim boundary:** `joint_symbolic_statistic_binding_status_not_scoring_not_validation`

This ledger separates two facts that were previously easy to conflate.
The symbolic same-statistic condition has passed: candidate and controls
are required to share `T_joint = sum_i q_i z_i`, the same row scope, and
the same covariance route.  However, this is not yet a numeric executable
validation statistic.

Summary:

- symbolic binding passed: `true`
- numeric executable binding passed: `false`
- cross-probe covariance closed: `false`
- criteria passed: `4/6`
- verdict: `SYMBOLIC_SAME_STATISTIC_BINDING_PASSED_NUMERIC_VALIDATION_BINDING_BLOCKED`

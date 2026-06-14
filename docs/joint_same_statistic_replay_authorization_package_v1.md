# Joint same-statistic replay authorization package v1

**Doc class:** external authorization handoff
**Status:** package authorization only; not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_same_statistic_replay_authorization_not_scoring_not_validation`

This package asks whether the next step may prepare a separate guarded
permission-only replay package using the symbolic joint statistic
`T_joint = sum_i q_i z_i`. It does not compute `T_joint` and does
not run controls.

The authorization boundary is strict: candidate and controls must share
the same symbolic statistic, row scope, q_i weights, signs,
standardization rule, and covariance route. The covariance route is the
caveated block-diagonal surrogate, not a source-native cross-probe
covariance product.

Upstream status:

- block-diagonal authorization decision: `AUTHORIZE_SEPARATE_GUARDED_JOINT_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION`
- statistic shell verdict: `JOINT_SINGLE_STATISTIC_PROTOCOL_SHELL_FROZEN_SYMBOLIC_NOT_EXECUTABLE`
- matched-control readiness verdict: `MATCHED_CONTROL_IMPLEMENTATION_READINESS_HAS_DESIGNS_BUT_PROTOCOL_BINDING_BLOCKED`
- covariance route verdict: `COVARIANCE_RESOLUTION_ROUTES_FROZEN_CROSS_PROBE_STILL_OPEN_NOT_SCORING`

# Joint row-level numeric penalty values v1

**Doc class:** numeric value package.
**Status:** separate penalty values only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.
**Claim boundary:** `joint_row_level_numeric_penalty_values_not_rescoring_not_validation`.

This package implements the reviewer-authorized numeric value step
for the symbolic row-level penalty shell. It computes channel-local
penalty values

`P_i(a) = omega_i mean_{r,f}(z_{i,a,r,f}^2)`

from the residual-blind normalized source-feature transform and the
frozen equal block weights. It does not choose a numeric `lambda_row`,
does not modify `T_joint`, and does not perform endpoint scoring.

## Scope

- feature rows read: `303986`
- channel penalty rows: `1042`
- candidate channel penalty rows: `3`
- control channel penalty rows: `1039`
- complete joint penalty rows: `1`
- candidate `P_row`: `0.0702783215662`

Controls are kept as channel-local penalty values because the current
source package does not define a residual-blind cross-channel control
alignment. Inventing that alignment here would create a new analysis
choice outside the authorization.

## Boundary

- `lambda_row_numeric_value_defined=false`
- `t_joint_rescoring_allowed=false`
- `endpoint_scoring_allowed=false`
- `endpoint_validation_claimed=false`

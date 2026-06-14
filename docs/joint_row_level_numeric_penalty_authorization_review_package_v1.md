# Joint row-level numeric penalty authorization review package v1

**Doc class:** external authorization handoff.
**Status:** not scoring; not endpoint validation; not cosmological validation.
**Claim boundary:** `joint_row_level_numeric_penalty_authorization_review_not_scoring_not_validation`.

This package asks whether the symbolic source-only row-level penalty
formula may be promoted into a later numeric penalty-value computation
package. It does not compute penalty values and does not modify
`T_joint`.

Upstream status:

- v4 protocol verdict: `SYMBOLIC_ROW_LEVEL_PENALTY_READY_NUMERIC_AUTHORIZATION_STILL_OPEN`
- symbolic formula verdict: `SYMBOLIC_ROW_LEVEL_PENALTY_FORMULA_FROZEN_NOT_COMPUTED_NOT_SCORING`
- formula family: `source_only_normalized_quadratic_feature_energy`
- channel formula: `P_i(a)=omega_i*mean_{r,f}(z_{i,a,r,f}^2)`
- joint formula: `P_row(a)=sum_i P_i(a)`

Allowed next action if accepted: build a separate package that computes
`P_i(a)` and `P_row(a)` from the frozen normalized source features for
candidates and matched controls under the same transform and block
weights.  `lambda_row` must remain unset or separately predeclared, and
`T_joint` rescoring remains forbidden unless a later authorization gate
explicitly permits it.

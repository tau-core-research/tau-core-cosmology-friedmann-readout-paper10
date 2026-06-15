# Joint row-level value-gate reviewer handoff v1

**Doc class:** reviewer handoff without repository access.
**Status:** two value-gate packages; not scoring; not validation.
**Claim boundary:** `joint_row_level_value_gate_handoff_not_scoring_not_validation`.

This handoff contains two independent review packages that follow the
completed open-blocker review. The reviewer does not need repository
access.

## Package 1: aligned-control value authorization

`joint_row_level_aligned_control_value_authorization_review_package_v1.zip`

Review question: may a later script compute aligned joint-control values
using only the already accepted deterministic min-count rule and the
already frozen channel-local penalty values?

Boundary: this package contains no aligned joint-control values and does
not authorize `lambda_row`, `T_joint` rescoring, endpoint scoring, or
validation.

## Package 2: numeric lambda candidate

`joint_row_level_numeric_lambda_review_package_v1.zip`

Review question: may `lambda_row = 1` be recorded as a dimensionless,
residual-blind unit-weight candidate for a later rescoring-authorization
package?

Boundary: this package does not apply `lambda_row`, does not rescore
`T_joint`, and does not authorize endpoint scoring or validation.

## Forbidden inputs for both packages

- endpoint residuals
- endpoint scores
- fit-improvement feedback
- posterior chains
- post-score control ranks

## Expected output

Return the completed response CSV or ZIP from each inner package. The
author-side import scripts must reject any response that authorizes
endpoint scoring or validation at this stage.

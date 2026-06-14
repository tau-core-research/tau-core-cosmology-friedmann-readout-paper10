# Joint row-level open blocker reviewer handoff v1

This handoff contains two independent, non-scoring reviewer packages.
The reviewer does not need repository access.

## What to review

1. `joint_row_level_cross_channel_control_alignment_review_package_v1.zip`
   - Review whether a residual-blind cross-channel control alignment is required.
   - Review whether the proposed deterministic min-count index alignment is acceptable as a design.
   - Do not authorize aligned control values, numeric `lambda_row`, or `T_joint` rescoring in this package.

2. `joint_row_level_lambda_policy_review_package_v1.zip`
   - Review whether any future `lambda_row` must be dimensionless.
   - Review whether any future numeric `lambda_row` must be residual-blind.
   - Do not authorize a numeric `lambda_row` or `T_joint` rescoring in this package.

## Required boundary

- No endpoint residuals.
- No endpoint scores.
- No fit-improvement feedback.
- No posterior chains.
- No post-score control ranks.
- No endpoint validation claim.

## Expected output

Return the completed response CSV or ZIP from each inner package.
The author-side import scripts will reject responses that authorize scoring, validation,
numeric `lambda_row`, or aligned control values at this stage.

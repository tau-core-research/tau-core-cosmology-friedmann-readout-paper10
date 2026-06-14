# Reviewer message: joint row-level open blockers v1

Dear Reviewer,

This package contains two independent non-scoring review tasks for the Paper10
joint row-level penalty route. You do not need repository access.

Please review the two ZIP files inside the handoff package:

1. `joint_row_level_cross_channel_control_alignment_review_package_v1.zip`
2. `joint_row_level_lambda_policy_review_package_v1.zip`

## Task 1: cross-channel control alignment

Please decide whether a residual-blind cross-channel control alignment is
required before any penalized joint score can be used, and whether the proposed
deterministic min-count index alignment is acceptable as a design to test next.

This task must not authorize:

- aligned joint control values,
- numeric `lambda_row`,
- `T_joint` rescoring,
- endpoint scoring,
- endpoint validation.

## Task 2: lambda policy

Please decide whether any future `lambda_row` must be dimensionless and whether
any future numeric value must be predeclared without endpoint feedback.

This task must not authorize:

- a numeric `lambda_row`,
- `T_joint` rescoring,
- endpoint scoring,
- endpoint validation.

## Forbidden inputs

Both reviews must remain source-side/protocol-side only. Please do not use:

- endpoint residuals,
- endpoint scores,
- fit-improvement feedback,
- posterior chains,
- post-score control ranks.

## Expected return

Please return the completed response CSV or completed response ZIP from each
inner package. The author-side import scripts will reject any response that
claims validation, authorizes scoring, authorizes numeric `lambda_row`, or
authorizes aligned control values at this stage.

Current handoff SHA-256:

```text
c7734f99b77ebe35fedb2752cc723390e07f2d0b0fafe152fe4d86fec16ebb5e
```


# Reviewer instructions: Joint guarded replay run-template authorization v1

You do not need repository access. Please review the attached zip:

`joint_guarded_replay_run_template_authorization_package_v1.zip`

Checksum:

```text
fb3e4f5554d8291fc4ad11addcefda237ba3c21c7edf1da3c3f2a7897834d38f  joint_guarded_replay_run_template_authorization_package_v1.zip
```

## What this package asks

This package asks only whether the frozen joint guarded replay run-template may be used as the basis for a later executable permission-only replay plan.

It does **not** authorize direct execution by itself. It does **not** authorize endpoint scoring. It does **not** claim endpoint validation or cosmological validation.

## File to fill

Inside the zip, fill:

`data/derived/joint_guarded_replay_run_template_authorization_response_template_v1.csv`

You may return either the completed CSV or a zip containing the completed CSV.

## Required safe fields

For every row, keep:

```text
forbidden_inputs_used=false
direct_execution_allowed=false
direct_execution_allowed_by_this_package=false
endpoint_scoring_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
separate_execution_step_required=true
```

## Accept responses

If accepted, use exactly:

```text
JGRT_Q1_TEMPLATE_SCOPE: authorize_template_for_separate_permission_only_replay
JGRT_Q2_IDENTICAL_STATISTIC: accept_identical_statistic_and_weights
JGRT_Q3_COVARIANCE_CAVEATS: accept_caveated_block_diagonal_conditions
JGRT_Q4_NO_VALIDATION_CLAIM: accept_permission_only_no_validation
```

Set `review_completed=true`, provide `reviewer_id_or_role`, and provide a short `reviewer_rationale` on every row.

## Reject option

Use `reject` on any row if the package appears to allow leakage, direct execution, endpoint scoring, endpoint validation, cosmological validation, or if the candidate/control statistic/covariance/caveat binding is not sufficiently frozen.

## Boundary to preserve

```text
joint_guarded_replay_run_template_authorization_not_execution_not_scoring_not_validation
```

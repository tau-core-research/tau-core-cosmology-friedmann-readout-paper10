# Joint Guarded Replay Execution Authorization Reviewer Instructions v1

This package asks only whether the already prepared joint guarded replay
runner may be executed once as a permission-only replay.

It does not authorize endpoint validation, cosmological validation, physical
validation, retuning, label changes, or any claim-strengthening.

## What to review

Use the package:

`data/derived/joint_guarded_replay_execution_authorization_package_v1.zip`

Inside it, review at least:

- `docs/joint_guarded_replay_execution_authorization_package_v1.md`
- `docs/joint_guarded_replay_execution_plan_v1.md`
- `docs/joint_guarded_replay_execution_blocker_status_v1.md`
- `scripts/run_joint_guarded_replay_permission_only_v1.py`
- `scripts/validate_joint_guarded_replay_permission_only_v1.py`
- `data/derived/joint_guarded_replay_execution_authorization_response_template_v1.csv`

## How to fill the response

Fill:

`data/derived/joint_guarded_replay_execution_authorization_response_template_v1.csv`

If you authorize the guarded permission-only execution, use these decisions:

- `JGRE_Q1_EXECUTION_SCOPE`: `authorize_permission_only_execution`
- `JGRE_Q2_RUNNER_GUARD`: `accept_runner_guard`
- `JGRE_Q3_CONTROL_AND_CAVEAT_BINDING`: `accept_same_controls_and_caveats`
- `JGRE_Q4_NO_VALIDATION`: `accept_permission_only_no_validation`

For every accepted row, keep:

- `forbidden_inputs_used=false`
- `permission_only_execution_allowed=true`
- `endpoint_validation_claimed=false`
- `cosmological_validation_claimed=false`
- `physical_validation_claimed=false`

If any row cannot be accepted, mark the reason in the reviewer notes and do
not authorize execution.

## Return

Return the completed CSV, or a ZIP containing the completed CSV.

The expected canonical import target is:

`data/derived/joint_guarded_replay_execution_authorization_response_v1.csv`

The expected accepted summary decision is:

`AUTHORIZE_JOINT_GUARDED_REPLAY_PERMISSION_ONLY_EXECUTION_NOT_VALIDATION`

## Claim boundary

The review is only an execution-permission gate for a guarded replay.  It is
not an endpoint validation gate and must not be cited as evidence that Tau Core
or any cosmological model has been validated.

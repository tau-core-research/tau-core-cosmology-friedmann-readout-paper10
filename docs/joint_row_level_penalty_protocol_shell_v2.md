# Joint row-level penalty protocol shell v2

**Doc class:** protocol shell.
**Status:** normalized symmetric transform ready; penalty not defined; not scoring; not validation.
**Claim boundary:** `joint_row_level_penalty_protocol_shell_v2_not_scoring_not_validation`.

This shell updates v1 after freezing the channel-local source-only
normalization rule and the candidate/control symmetric normalized
feature transform.

The shell does not define a penalty formula, does not compute a penalty,
does not authorize endpoint replay, and does not permit `T_joint`
rescoring. Before any score can change, the normalized transform must
be bound to a covariance or block-weight shell in a separate reviewed
gate.

Verdict: `NORMALIZED_SYMMETRIC_TRANSFORM_READY_COVARIANCE_BINDING_STILL_OPEN`.
Next action: `bind_transform_to_covariance_or_block_weight_shell_before_any_penalty_formula`.

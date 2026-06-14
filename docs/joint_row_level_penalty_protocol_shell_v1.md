# Joint row-level penalty protocol shell v1

**Doc class:** protocol shell.
**Status:** source-feature inputs complete; penalty not defined; not scoring; not validation.
**Claim boundary:** `joint_row_level_penalty_protocol_shell_not_scoring_not_validation`.

This shell is the first protocol layer after the common source-feature
export v5. It records that all active channels now expose residual-blind
source-feature inputs, including KiDS row-level null-control vectors.

The shell does not define a penalty formula, does not compute a penalty,
does not authorize endpoint replay, and does not permit `T_joint`
rescoring. Before any score can change, a channel-local normalization,
candidate/control symmetric transform, and covariance or block-weight
binding must be frozen in a separate reviewed gate.

Verdict: `SOURCE_FEATURE_INPUTS_COMPLETE_PENALTY_PROTOCOL_STILL_OPEN`.
Next action: `freeze_channel_local_normalization_and_control_symmetric_transform_before_any_scoring`.

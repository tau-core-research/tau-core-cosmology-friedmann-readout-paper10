# Joint candidate/control symmetric normalized feature transform v1

**Doc class:** source-only normalized feature transform.
**Status:** transform built; penalty not defined; not scoring; not validation.
**Claim boundary:** `joint_candidate_control_symmetric_normalized_feature_transform_not_scoring_not_validation`.

This artifact applies the frozen channel-local normalization rule to
candidate and matched-control source features using the same transform.
It includes the compressed KiDS row-level null-control vectors in the
same normalized feature basis as the KiDS candidate rows.

The transform uses no endpoint scores, residuals, fit statistics, or
posterior chains. It does not define or compute a penalty and does not
permit `T_joint` rescoring.

Rows: `303986`.
Verdict: `NORMALIZED_FEATURE_TRANSFORM_BUILT_NOT_SCORING`.
Next action: `bind_transform_to_covariance_or_block_weight_shell_before_any_penalty_formula`.

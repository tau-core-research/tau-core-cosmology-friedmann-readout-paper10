# Joint channel-local source normalization rule v1

**Doc class:** source-only normalization rule.
**Status:** normalization frozen; not applied to scoring; not validation.
**Claim boundary:** `joint_channel_local_source_normalization_rule_not_scoring_not_validation`.

This artifact freezes the first channel-local normalization rule for
future row-level penalty design. For each active channel, normalizable
source features are scaled by the maximum absolute residual-blind
source-feature value in that channel, with a unit fallback for an all-zero
channel. Metadata features such as artifact size are excluded.

The rule uses no endpoint scores, residuals, fit statistics, posterior
chains, or post-hoc endpoint ordering. It does not compute a penalty and
does not permit `T_joint` rescoring.

Verdict: `CHANNEL_LOCAL_SOURCE_NORMALIZATION_FROZEN_NOT_SCORING`.
Next action: `build_candidate_control_symmetric_normalized_feature_transform_without_endpoint_fields`.

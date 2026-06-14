# Joint numeric T_joint channel-distinguishability penalty requirements v1

**Doc class:** penalty requirements gate.
**Status:** requirements frozen; penalty not admissible yet; not scoring; not validation.
**Claim boundary:** `joint_numeric_t_joint_channel_distinguishability_penalty_requirements_not_scoring_not_validation`.

This gate prevents the thin shuffled-channel margin from being fixed
by an endpoint-driven penalty. It records that the observer-path and
DESI shape/time channels are source-distinct, but that source-route
distinctness alone is not enough to modify `T_joint`.

Before any channel-distinguishability penalty can be used, a residual-blind
source-native separation metric must be built, small-N imbalance must remain
caveated, and the same rule must apply symmetrically to candidate and controls.

Verdict: `PENALTY_NOT_ADMISSIBLE_YET_REQUIREMENTS_FROZEN`.
Next action: `build_residual_blind_source_native_overlap_metric_then_review_before_any_rescoring`.

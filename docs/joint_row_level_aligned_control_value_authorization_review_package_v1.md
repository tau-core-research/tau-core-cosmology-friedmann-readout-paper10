# Joint row-level aligned-control value authorization review package v1

**Doc class:** external authorization handoff.
**Status:** authorization to compute aligned control values only; no aligned values yet; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.
**Claim boundary:** `joint_row_level_aligned_control_value_authorization_not_values_not_scoring_not_validation`.

The previous cross-channel alignment design review has been completed.
It accepted the deterministic design but kept aligned values blocked.
This package is the next narrow gate: it asks whether a later script may
compute aligned joint-control values from source-frozen channel-local
penalty values using that deterministic rule.

It does not contain aligned joint-control values.
It does not choose a numeric `lambda_row`.
It does not rescore `T_joint`.
It does not authorize endpoint scoring or validation.

Frozen proposed rule:

`deterministic_min_count_index_alignment_after_sort_by_control_family_then_control_id`

Current diagnostic state:

- alignment design decision: `ACCEPT_CROSS_CHANNEL_CONTROL_ALIGNMENT_DESIGN_NOT_VALUES_NOT_RESCORING_NOT_VALIDATION`
- blocker verdict: `CROSS_CHANNEL_ALIGNMENT_DESIGN_ACCEPTED_VALUES_STILL_BLOCKED`
- active channels: `desi_shape_time_readout|kids_lensing_cosebis_low_mode|observer_path_basis_low_z`
- control rows available: `1039`
- candidate rows available: `3`
- min aligned control count if later authorized: `6`

A positive response may only authorize the later value-computation
artifact. A separate numeric-lambda gate and a separate rescoring gate
would still be required before any penalized `T_joint` result.

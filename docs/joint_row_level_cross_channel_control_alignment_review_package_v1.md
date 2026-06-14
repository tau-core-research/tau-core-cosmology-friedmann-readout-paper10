# Joint row-level cross-channel control alignment review package v1

**Doc class:** external design-review handoff.
**Status:** alignment design only; no aligned values; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.
**Claim boundary:** `joint_row_level_cross_channel_control_alignment_review_not_scoring_not_validation`.

The current numeric penalty values are channel-local for controls.
Before any penalized joint-control comparison, a residual-blind
cross-channel alignment rule must be accepted. This package proposes
only a deterministic design for review:

`sort controls by (control_family, control_id) within each channel,
then align the first min_count controls by index across channels.`

No aligned joint control values are computed here.

- active channels: `desi_shape_time_readout|kids_lensing_cosebis_low_mode|observer_path_basis_low_z`
- control counts: `desi_shape_time_readout:6;kids_lensing_cosebis_low_mode:1008;observer_path_basis_low_z:25`
- min aligned count if accepted: `6`

The severe count imbalance is explicit and remains a caveat. The
reviewer may reject this design or accept it only as a cautious
next-step alignment test.

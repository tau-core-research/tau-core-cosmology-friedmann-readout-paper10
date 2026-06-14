# Joint matched-control resolution plan v1

**Doc class:** post-replay control-suite blocker-resolution plan
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_matched_control_resolution_plan_not_scoring_not_validation`

This plan freezes how the third promotion blocker should be resolved.
It does not run the controls. It only binds every future control family
to the same joint statistic and same covariance route as the candidate.

Required control families:

1. `shuffled_channel_labels`
2. `wrong_channel_or_wrong_family_controls`
3. `sign_flip_controls`
4. `leave_one_probe_or_block_drop`
5. `null_readout_controls`
6. `scope_and_forbidden_input_controls`
7. `single_statistic_binding`
8. `covariance_binding`

Summary:

- active channel order: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- control families total: `8`
- planned not implemented: `6`
- blocked by upstream gate: `2`
- fastest covariance route: `caveated_block_diagonal_surrogate_plus_same_statistic_controls`
- verdict: `MATCHED_CONTROL_RESOLUTION_PLAN_FROZEN_IMPLEMENTATION_BLOCKED_NOT_SCORING`

Interpretation: the control-suite route is now fully specified as a
future implementation plan, but it remains blocked until the single joint
statistic and covariance binding are instantiated and reviewed.

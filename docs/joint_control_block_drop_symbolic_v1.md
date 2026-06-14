# Joint symbolic block-drop controls v1

**Doc class:** matched-control symbolic artifact
**Status:** complete symbolic enumeration; not scoring; not validation
**Claim boundary:** `joint_control_block_drop_symbolic_not_scoring_not_validation`

This artifact enumerates every nontrivial block-drop control for the
three active channels under the shared symbolic statistic
`T_joint = sum_i q_i z_i`. It includes leave-one, all-but-one, and
all-drop/null controls. It does not compute a numeric statistic.

Summary:

- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- controls enumerated: `7`
- leave-one controls: `3`
- all-but-one controls: `3`
- all-drop/null control included: `true`
- verdict: `BLOCK_DROP_CONTROLS_SYMBOLICALLY_COMPLETE_NOT_SCORING`

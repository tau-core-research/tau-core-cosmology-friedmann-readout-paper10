# Joint row-level penalty block-weight binding shell v1

**Doc class:** covariance/block-weight binding shell.
**Status:** binding frozen for future penalty design; penalty not defined; not scoring; not validation.
**Claim boundary:** `joint_row_level_penalty_block_weight_binding_shell_not_scoring_not_validation`.

This shell binds the candidate/control-symmetric normalized feature
transform to the existing caveated block-diagonal joint route.  It
does not introduce a row-level penalty formula and does not modify
`T_joint`.

The only frozen block-weight policy is an equal-channel preweight
shell, used solely as a future design constraint:

\[
  \omega_i = 1/3, \qquad i=1,\ldots,3.
\]

A later penalty formula must apply the same normalized transform,
the same channel weights, and the same covariance/caveat discipline
to candidates and matched controls.  Any numeric rescoring still
requires a separate authorization gate.

Current machine state:

- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- normalized feature rows: `303986`
- covariance binding route: `caveated_block_diagonal_independence`
- cross-probe covariance product available: `false`
- block-diagonal independence source-justified: `true`
- block-weight policy: `equal_channel_preweight_shell_only`
- penalty formula defined: `false`
- numeric `T_joint` rescoring allowed: `false`
- verdict: `BLOCK_WEIGHT_BINDING_SHELL_FROZEN_NOT_SCORING`

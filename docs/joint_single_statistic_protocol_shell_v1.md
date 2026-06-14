# Joint single-statistic protocol shell v1

**Doc class:** symbolic protocol shell
**Status:** not executable; not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_single_statistic_protocol_shell_not_scoring_not_validation`

This shell states the future joint statistic form that candidate and
matched controls must share. It does not compute the statistic.

Symbolic form:

```text
z_i = signed_standardized_channel_response(candidate_or_control_i)
T_joint = sum_i q_i z_i
```

The formula is only admissible for scoring after the covariance route,
row scope, channel standardization, and matched-control suite are frozen
for candidate and controls together.

Summary:

- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- symbolic joint statistic: `T_joint = sum_i q_i z_i`
- single joint statistic defined: `false`
- protocol executable: `false`
- cross-probe covariance defined: `false`
- matched controls ready for scoring: `false`
- verdict: `JOINT_SINGLE_STATISTIC_PROTOCOL_SHELL_FROZEN_SYMBOLIC_NOT_EXECUTABLE`

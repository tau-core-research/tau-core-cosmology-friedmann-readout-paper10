# Joint matched control-suite requirements gate v1

**Doc class:** matched-control requirements gate
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_matched_control_suite_requirements_gate_not_scoring_not_validation`

This gate freezes the control families required before any Paper10 joint
likelihood-surrogate scoring attempt. It does not run controls and does
not define the final joint statistic. The controls must later be evaluated
under exactly the same reviewed covariance/statistic as the candidate.

Required control families:

- shuffled channel labels
- wrong-channel / wrong-family controls
- deterministic sign flips
- leave-one-probe / block-drop controls
- null/readout controls
- scope and leakage controls
- shared-statistic binding
- covariance binding

Summary:

- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- specified control families: `8/8`
- implemented under joint statistic: `false`
- scoring allowed: `false`
- verdict: `JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_FROZEN_IMPLEMENTATION_BLOCKED`

Interpretation: the matched controls are now named and bound to a future
single-statistic/covariance discipline, but they remain implementation-blocked
until the covariance/independence gate and single-statistic gate are closed.

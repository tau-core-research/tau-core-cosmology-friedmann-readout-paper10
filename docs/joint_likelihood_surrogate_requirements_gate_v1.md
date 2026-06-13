# Joint likelihood-surrogate requirements gate v1

**Doc class:** requirements gate
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_likelihood_surrogate_requirements_gate_not_scoring_not_validation`

This gate records the next step opened by the completed Q_i source-side
review. The review accepts the active support factors only as caveated
source-side support; it does not authorize validation-facing promotion.
Therefore the next object must be a separately frozen joint likelihood
or likelihood-surrogate protocol with covariance-aware controls.

Summary:

- Q_i decision: `QI_REVIEW_ACCEPTED_OR_CAVEATED_SOURCE_SIDE_NOT_VALIDATION`
- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- requirements passed: `5/8`
- hard blockers open: `3`
- endpoint scoring allowed: `false`
- next required action: `define_covariance_aware_joint_likelihood_surrogate_and_controls_before_scoring`
- verdict: `JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_FROZEN_SCORING_BLOCKED`

Interpretation: the Paper10 joint-kernel route is now source-side
organized enough to specify the validation-facing protocol, but not to
run it. The remaining blockers are the covariance model, the single joint
statistic, and the matched control suite under that same statistic.

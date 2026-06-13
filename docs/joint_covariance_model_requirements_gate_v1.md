# Joint covariance-model requirements gate v1

**Doc class:** covariance requirements gate
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_covariance_model_requirements_gate_not_scoring_not_validation`

This gate narrows the first hard blocker from the joint likelihood-surrogate
requirements ledger: the covariance treatment for the three active positive-support
channels. It does not build a joint likelihood and does not permit scoring.

Summary:

- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- channel covariance blocks available: `3/3`
- cross-probe covariance defined: `false`
- block-diagonal surrogate allowed for future review: `true`
- block-diagonal surrogate allowed for scoring now: `false`
- hard blockers open: `3`
- verdict: `JOINT_COVARIANCE_MODEL_REQUIREMENTS_PARTIAL_BLOCKS_READY_CROSS_PROBE_BLOCKED`

Interpretation: KiDS has a source-native full covariance block. The observer/path
and DESI shape/readout blocks have narrow, caveated surrogate covariance support,
but remain hard blockers for validation-facing scoring. A future reviewed
block-diagonal likelihood surrogate may be prepared only if cross-probe independence
is frozen explicitly or a source-native cross-probe covariance is supplied.

# Joint guarded replay run-template authorization package v1

**Doc class:** external reviewer handoff package.
**Status:** prepared, not completed.
**Claim boundary:** `joint_guarded_replay_run_template_authorization_not_execution_not_scoring_not_validation`.

This package asks whether the frozen joint guarded replay run-template
may be used as the basis for a later executable permission-only replay.
It is not itself execution, endpoint scoring, endpoint validation, or
cosmological validation.

The reviewed template keeps candidate and controls under identical
block-diagonal statistic, block-weight, covariance/caveat, and
matched-control conditions.

Mandatory controls carried by the template:

- `shuffled_channel_labels`
- `wrong_channel_assignment`
- `sign_flip`
- `block_drop`
- `null_readout`
- `leakage_audit`
- `shared_statistic_control`
- `covariance_binding_control`

Mandatory caveats carried by the template:

- `no_source_native_cross_probe_covariance_product`
- `block_diagonal_independence_caveated`
- `shared_sky_overlap_caveat`
- `shared_mask_selection_caveat`
- `shared_redshift_kernel_caveat`
- `shared_cosmology_nuisance_caveat`
- `shared_calibration_population_caveat`

The reviewer should reject this package if any direct execution,
endpoint scoring, endpoint validation, or cosmological validation
claim is inferred from the template itself.

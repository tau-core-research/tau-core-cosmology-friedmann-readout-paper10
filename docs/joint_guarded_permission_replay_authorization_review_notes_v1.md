# Joint guarded permission replay authorization review notes v1

Decision:

```text
AUTHORIZE_GUARDED_PERMISSION_REPLAY_PACKAGE_PREPARATION_ONLY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION
```

The package supports preparing a later guarded permission-only joint replay package under the completed caveated block-diagonal authorization. This review does not authorize direct execution, endpoint scoring, endpoint validation, or cosmological validation.

Boundary retained:

```text
forbidden_inputs_used=false
endpoint_scoring_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
direct_execution_allowed=false
separate_run_template_required=true
```

Mandatory caveats retained:

```text
no_source_native_cross_probe_covariance_product_available
block_diagonal_independence_is_caveated
shared_sky_mask_overlap_caveat_active
redshift_kernel_overlap_caveat_active
shared_cosmology_nuisance_calibration_caveat_active
population_covariance_caveat_active
candidate_and_controls_same_statistic_required
candidate_and_controls_same_covariance_blocks_required
```

Interpretation: a guarded run-template package may be prepared next, but no executable replay script or endpoint score may be run until that separate run-template gate passes.

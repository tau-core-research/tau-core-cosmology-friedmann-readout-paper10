# Joint guarded replay execution plan v1

This artifact is an execution-plan gate, not an executable replay.
It creates no endpoint scores, no residuals, and no cosmological validation claim.

It freezes the future runner/validator names, future output artifact names,
active block order, identical statistic/weight/covariance/caveat discipline,
and mandatory controls for a later permission-only replay.

The future runner must not exist or run until a separate execution authorization
gate is built, reviewed, imported, and validated.

Required controls:

- `shuffled_channel_labels`
- `wrong_channel_assignment`
- `sign_flip`
- `block_drop`
- `null_readout`
- `leakage_audit`
- `shared_statistic_control`
- `covariance_binding_control`

Required caveats:

- `no_source_native_cross_probe_covariance_product`
- `block_diagonal_independence_caveated`
- `shared_sky_overlap_caveat`
- `shared_mask_selection_caveat`
- `shared_redshift_kernel_caveat`
- `shared_cosmology_nuisance_caveat`
- `shared_calibration_population_caveat`

Claim boundary: `joint_guarded_replay_execution_plan_not_run_not_scoring_not_validation`.

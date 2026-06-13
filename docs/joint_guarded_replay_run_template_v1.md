# Joint guarded replay run template v1

This artifact is a run-template gate, not an executable replay,
not endpoint scoring, and not cosmological validation.

The completed guarded-permission response authorizes only
preparation of this separate template.  It keeps direct execution
disabled until this template is independently authorized.

The template freezes the active block order, the shared
block-diagonal statistic, the same block-weight rule, and the
matched control suite.  Candidate and controls must be evaluated
under identical statistic, covariance, caveat, and block-weight
conditions in any later replay.

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

Claim boundary: `joint_guarded_replay_run_template_not_execution_not_scoring_not_validation`.

# Joint guarded replay run-template authorization review notes v1

Decision:

```text
AUTHORIZE_RUN_TEMPLATE_FOR_LATER_PERMISSION_ONLY_REPLAY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION
```

Scope reviewed:

- frozen joint guarded replay run-template only;
- active blocks: `kids_lensing_cosebis_low_mode`, `observer_path_basis_low_z`, `desi_shape_time_readout`;
- mandatory controls: shuffled channel labels, wrong channel assignment, sign flip, block drop, null readout, leakage audit, shared statistic control, covariance binding control;
- mandatory caveats: no source-native cross-probe covariance product, caveated block-diagonal independence, shared sky/mask/redshift-kernel/cosmology-nuisance/calibration-population caveats.

Boundary:

```text
forbidden_inputs_used=false
endpoint_scoring_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
direct_execution_allowed=false
separate_execution_step_required=true
```

Interpretation:

The run-template may be authorized as the basis for a later executable permission-only diagnostic replay, but this package itself is not execution, not endpoint scoring, not endpoint validation, and not cosmological validation. Candidate and controls must remain bound to the same frozen block-diagonal statistic, block weights, covariance/caveat conditions, and matched-control suite.

Completion-check: `pass`.

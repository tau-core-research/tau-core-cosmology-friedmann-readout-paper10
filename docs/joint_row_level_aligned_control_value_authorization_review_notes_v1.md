# Joint row-level aligned-control value authorization review notes v1

## Decision

`AUTHORIZE_ALIGNED_CONTROL_VALUE_COMPUTATION_ONLY_NOT_VALUES_NOT_LAMBDA_NOT_RESCORING_NOT_VALIDATION`

## Scope accepted

The package is downstream of the completed cross-channel alignment design review and may proceed to a later aligned-control value computation package using the frozen deterministic rule:

`deterministic_min_count_index_alignment_after_sort_by_control_family_then_control_id`

The authorization is limited to computing aligned joint-control values from source-frozen channel-local penalty values in a later package.

## Caveat retained

The min-count alignment caveat remains explicit:

- active channels: `desi_shape_time_readout|kids_lensing_cosebis_low_mode|observer_path_basis_low_z`
- control rows available: `1039`
- candidate rows available: `3`
- min aligned control count if later authorized: `6`

This is not an endpoint-validating statistic.

## Boundaries retained

- `forbidden_inputs_used=false`
- `aligned_joint_control_values_authorized=false` in this review response because no aligned values are present here
- `lambda_row_numeric_value_authorized=false`
- `t_joint_rescoring_authorized=false`
- `endpoint_scoring_allowed=false`
- `endpoint_validation_claimed=false`
- `cosmological_validation_claimed=false`
- `physical_validation_claimed=false`

## Interpretation

This review authorizes only a later aligned-control value computation artifact. It does not authorize `lambda_row`, does not rescore `T_joint`, does not perform endpoint scoring, and does not claim validation.

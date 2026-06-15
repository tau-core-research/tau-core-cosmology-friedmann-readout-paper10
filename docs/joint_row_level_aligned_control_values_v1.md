# Joint row-level aligned control values v1

**Doc class:** guarded numeric value artifact.
**Status:** aligned control values only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.
**Claim boundary:** `joint_row_level_aligned_control_values_not_rescoring_not_validation`.

This artifact is produced only after a completed reviewer response
authorizes a value-computation-only aligned-control step. It applies
the deterministic residual-blind min-count alignment rule to the
already frozen channel-local penalty values.

It does not choose `lambda_row`, does not rescore `T_joint`, and does
not perform endpoint scoring or validation.

- aligned rows: `6`
- active channels: `desi_shape_time_readout|kids_lensing_cosebis_low_mode|observer_path_basis_low_z`
- mean aligned control `P_row`: `0.109794891058`

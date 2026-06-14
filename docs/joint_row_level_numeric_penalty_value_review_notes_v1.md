# Joint row-level numeric penalty value review notes v1

Decision:

```text
ACCEPT_NUMERIC_PENALTY_VALUES_NOT_LAMBDA_NOT_T_JOINT_RESCORING_NOT_VALIDATION
```

Scope reviewed: numeric row-level penalty values only. The package does not authorize `lambda_row`, `T_joint` rescoring, endpoint scoring, endpoint validation, cosmological validation, or physical validation.

Checks performed on the package contents:

- package manifest byte/SHA-256 check: `pass` (12/12 artifacts)
- included validator `validate_joint_row_level_numeric_penalty_values_v1.py`: `pass`
- feature rows read: `303986`
- channel penalty rows: `1042`
- candidate channel penalty rows: `3`
- control channel penalty rows: `1039`
- complete joint penalty rows: `1`
- reported candidate `P_row`: `0.0702783215662`
- recomputed candidate `P_row` from candidate `P_i` rows: `0.0702783215662`

Boundary retained:

```text
forbidden_inputs_used=false
numeric_penalty_values_accepted=true
cross_channel_control_alignment_authorized=false
lambda_row_numeric_value_authorized=false
t_joint_rescoring_authorized=false
endpoint_scoring_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
physical_validation_claimed=false
```

Interpretation: the numeric penalty values are acceptable as a reviewed diagnostic value artifact. This is not a numeric `lambda_row`, not `T_joint` rescoring, not endpoint scoring, and not validation. Controls remain channel-local in this package.

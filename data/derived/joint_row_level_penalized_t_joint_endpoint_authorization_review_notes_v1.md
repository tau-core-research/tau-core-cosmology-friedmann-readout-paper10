# Joint row-level penalized T_joint endpoint authorization review notes v1

Decision:

```text
AUTHORIZE_PENALIZED_T_JOINT_LEDGER_AND_ONE_GUARDED_ENDPOINT_SCORING_REPLAY_NOT_VALIDATION
```

Scope accepted:

- compute one record-only `T_joint_penalized = T_joint + lambda_row * P_row` ledger;
- use `T_joint = 4.142466300799e+00`;
- use frozen `lambda_row = 1.0`;
- use aligned control rows = 6;
- use mean aligned control penalty = `0.109794891058`;
- run exactly one guarded endpoint-scoring replay only if executed later under the frozen package policy.

Boundaries retained:

```text
forbidden_inputs_used=false
endpoint_scoring_run_by_this_review=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
physical_validation_claimed=false
```

No validation is claimed. The authorization permits a downstream guarded endpoint-scoring/preflight evidence action only; it does not create a discovery claim, cosmological validation, or physical validation.

Frozen no-change policy retained:

```text
no_formula_changes
no_label_changes
no_source_proxy_changes
no_kernel_changes
no_amplitude_changes
no_covariance_policy_changes
no_post_score_retuning
```

# Low-z Pantheon+ W-time Uncertainty-Basis Replay Authorization Review Notes v1

## Decision

```text
GO_W_TIME_UNCERTAINTY_BASIS_REPLAY_PERMISSION_ONLY
```

## Scope

The authorization applies only to one separate permission-only replay using the frozen:

```text
W_time_uncertainty_basis_candidate
```

The authorized scope is:

```text
single_permission_only_low_z_W_time_uncertainty_basis_replay_not_validation
```

## Basis

The candidate summary reports:

```text
status=W_TIME_UNCERTAINTY_BASIS_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING
W_time_values_status=SOURCE_SIDE_BASIS_CANDIDATE_ONLY_NOT_ENDPOINT
basis_rows=424
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
```

The authorization decision uses only the frozen source-side candidate package and policy boundaries.

## Boundaries Preserved

```text
forbidden_inputs_used=false
endpoint_replay_allowed=true
endpoint_validation_claimed=false
physical_validation_claimed=false
claim_boundary=w_time_uncertainty_basis_replay_authorization_review_not_validation
```

This is not endpoint validation, not scoring, not population evidence, not a physical clock-drift measurement, and not a physical validation claim.

## Frozen Replay Conditions

The replay must preserve:

```text
424 frozen low-z Pantheon+ source rows
frozen CC redshift-bin policy
frozen Delta_clock_uncertainty_candidate
frozen source-normalized W_time_uncertainty_basis_candidate
no label changes
no bin changes
no normalization changes
no row-selection changes
```

The authorization decision does not use Pantheon distance residuals, endpoint scores, fit statistics, late-time fitted parameters, posterior chains, post-hoc H(z) smoothing, or post-hoc clock anomaly labels.

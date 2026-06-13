# V2 Observer-Basis Replay Authorization Review Notes v1

## Decision

```text
GO_OBSERVER_BASIS_REPLAY_PERMISSION_ONLY
```

## Scope

The authorization applies only to one separately declared 12-row replay for:

```text
W_path_x_sky_x_x_zcenter
```

The replay scope is:

```text
single_permission_only_12_row_W_path_x_sky_x_x_zcenter_replay_not_validation
```

## Basis

The prior observer-basis candidate review accepted the candidate only for preparation of a separate permission-only replay authorization package.

The observer-basis fast screen identifies `W_path_x_sky_x_x_zcenter` as the best candidate family on the frozen 12-row partial path scope and shows that it survived its local family controls in the preauthorization diagnostic setting.

## Boundaries Preserved

```text
forbidden_inputs_used=false
endpoint_replay_allowed=true
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
claim_boundary=v2_observer_basis_replay_authorization_not_validation
```

This is not endpoint validation, not population evidence, not a physical lensing-path-weight claim, not post-hoc residual tuning, and not an endpoint-score claim.

## Required Replay Controls

The permission-only replay must preserve the frozen source-side controls:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
```

No new source-family tuning, covariance reweighting, endpoint residual input, or threshold retuning is authorized by this review.

# V2 Sky-Z Replay Authorization Review Notes V1

## Decision

```text
GO_SKY_Z_REPLAY_PERMISSION_ONLY
```

## Scope

This authorizes only one future permission-only replay of the predeclared `W_path_x_sky_z` family on the frozen 12-row partial path scope.

## Boundary

```text
forbidden_inputs_used=false
endpoint_replay_allowed=true
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
authorization_scope=single_permission_only_12_row_W_path_x_sky_z_replay_not_validation
claim_boundary=v2_sky_z_replay_authorization_review_not_validation
```

## Review basis

- The supplied observer-dependence follow-up materials are source-side and not endpoint validation.
- The package manifest reports no endpoint residuals, endpoint scores, fit statistics, posterior chains, KiDS data vector values, or physical lensing-path weight claims.
- `W_path_x_sky_z` survives its frozen family controls in the source-side V2 path sky/environment screen with `controls_better_than_candidate_chi2=0`.
- The authorization does not expand the scope beyond `W_path_x_sky_z` and the 12-row partial path scope.

## Non-claims

This review does not claim endpoint validation, endpoint score improvement, population evidence, a physical lensing-path proof, a new gravitational law, post-hoc sky-direction tuning, or a full low-z path-channel result.

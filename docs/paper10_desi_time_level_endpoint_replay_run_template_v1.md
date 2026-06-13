# DESI Time-Level Endpoint Replay Run Template V1

**Doc class:** replay run template.

**Reader role:** Paper 10 endpoint runner/reviewer.

**Status:** prepared; authorization required; not replayed; not scoring; not validation.

**Canonical parent:** `paper10_desi_time_level_endpoint_authorization_review_v1.md`.

This template predeclares the grammar for a later DESI/CC five-row time-level
endpoint replay. It does not authorize or run the replay.

The replay script must not run unless a completed authorization response summary
exists with:

```text
decision=GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY
endpoint_replay_allowed=true
endpoint_validation_claimed=false
physical_validation_claimed=false
```

## Frozen Scope

Allowed rows:

```text
DESI radial indices 0;1;2;3;4
```

Excluded row:

```text
DESI radial index 5, z_eff=2.33
```

The excluded high-z Ly-alpha row remains holdout or future independent-clock
support. No CC extrapolation is allowed in this first replay scope.

## Candidate/Control Grammar

Active route family:

```text
DESI_CC_MATCHED_RADIAL_BAO_TIME_LEVEL
```

Frozen controls:

```text
rd_off_control
external_prior_width_stress
wrong_prior_control
BAO_pair_drop_control
CC_match_window_stress
level_slope_swap_control
redshift_order_shuffle_control
```

The corresponding deterministic seeds are frozen in
`paper10_desi_time_level_control_seed_manifest_v1.csv`.

## Forbidden Inputs

The template forbids endpoint scores before authorization, fit statistics before
authorization, post-hoc row/control/seed selection, post-hoc high-z policy
changes, CC extrapolation, post-hoc `H(z)` smoothing, Pantheon distance
residuals, late-time fit parameter selection, and physical validation claims.

## Claim Boundary

```text
paper10_desi_time_level_endpoint_replay_template_not_validation
```

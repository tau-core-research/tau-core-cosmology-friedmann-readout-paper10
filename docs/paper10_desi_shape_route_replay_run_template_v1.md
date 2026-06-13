# DESI Shape-Route Replay Run Template V1

**Doc class:** replay run template.

**Reader role:** Paper 10 endpoint runner/reviewer.

**Status:** prepared; authorization required; not replayed; not scoring; not validation.

**Canonical parent:** `paper10_desi_shape_route_replay_authorization_review_v1.md`.

This template predeclares the grammar for a later DESI shape-route replay. It
does not authorize or run the replay.

The replay script must not run unless a completed authorization response summary
exists with:

```text
decision=GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY
endpoint_replay_allowed=true
endpoint_validation_claimed=false
physical_validation_claimed=false
```

## Frozen Scope

Active route family:

```text
DESI_CC_MATCHED_RADIAL_BAO_TIME_SHAPE
```

Allowed radial rows:

```text
DESI radial indices 0;1;2;3;4
```

Excluded radial row:

```text
DESI radial index 5, z_eff=2.33
```

Allowed adjacent-shape rows:

```text
shape rows 0;1;2;3
```

Available curvature rows:

```text
curvature rows 0;1;2
```

## Candidate/Control Grammar

Primary candidate:

```text
CLOCK_SLOPE_SHAPE
```

Frozen control families:

```text
redshift_order_shuffle
leave_row_or_pair
cc_window_stress
wrong_time_basis
rd_prior_stress
```

The CC-window stress remains caveated source context with
`SOURCE_REOPEN_ONLY_NO_REPLAY`; the template only records that it is bound as a
control family.

## Forbidden Inputs

The template forbids endpoint scores before authorization, fit statistics before
authorization, post-hoc shape/row/control selection, post-hoc CC-window
selection, high-z policy changes, CC extrapolation, post-hoc `H(z)` smoothing,
post-hoc beta retuning, Pantheon distance residuals, late-time fit parameter
selection, and physical validation claims.

## Claim Boundary

```text
paper10_desi_shape_route_replay_template_not_validation
```

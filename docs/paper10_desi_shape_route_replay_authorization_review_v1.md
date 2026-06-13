# DESI Shape-Route Replay Authorization Review V1

**Doc class:** replay authorization handoff.

**Reader role:** external reviewer without repository access.

**Status:** blank authorization package; not completed; not replay; not
validation.

**Canonical parent:** `paper10_desi_shape_bound_control_vectors_v1.md`.

The DESI time/readout shape route has now reached the following source-side
state:

```text
shape_observable_candidate_available = true
shape_bound_control_count = 5
unbound_control_families = none
cc_window_stress_release_policy = SOURCE_REOPEN_ONLY_NO_REPLAY
endpoint_replay_allowed = false
endpoint_validation_claimed = false
physical_validation_claimed = false
```

This handoff asks whether one separate permission-only replay may be prepared
later for the frozen `CLOCK_SLOPE_SHAPE` route. It does not run the replay and
does not claim validation.

## Proposed Replay Scope

The proposed scope is limited to:

- the five DESI radial BAO rows matched within frozen cosmic-chronometer support;
- the frozen adjacent first-difference `CLOCK_SLOPE_SHAPE` observable;
- the frozen curvature shape only as secondary/wrong-time-basis context;
- the high-z `z=2.33` row retained as holdout, not replay input;
- the source-bound `K_null` control suite;
- CC-window stress retained only as caveated source context.

## Reviewer Questions

The reviewer is asked to check:

1. the scope is source-frozen and row5 remains excluded;
2. all `K_null` controls are bound to the shape route;
3. CC-window stress is caveated and does not release replay by itself;
4. no endpoint residuals, endpoint scores, fit statistics, posterior chains, or
   post-hoc shape/control choices are used in the authorization decision;
5. any positive decision grants only permission to run one replay later, not
   endpoint validation or physical validation.

## Claim Boundary

```text
paper10_desi_shape_route_replay_authorization_review_not_validation
```

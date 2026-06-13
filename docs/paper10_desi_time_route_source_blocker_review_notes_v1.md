# Paper10 DESI time-route source-blocker external review notes v1

Decision:

```text
PARTIAL_SOURCE_ACQUISITION_REOPEN_ROW4_KEEP_ROW5_BLOCKED_NO_REPLAY
```

## Row 4

Accepted as caveated source-side reopen only. The strict `|Delta z| <= 0.10` window remains the frozen default, but Moresco 2015 at `z=1.363`, `H=160+/-33.6 km/s/Mpc`, is independent of the Simon family and is a near-window miss for DESI row 4 at `z_eff=1.484` with `|Delta z|=0.121`. This is enough to reopen source acquisition under explicit caveats, not enough for endpoint replay or validation.

## Row 5

Kept blocked. The frozen cosmic-chronometer table reaches only `z=1.965`; DESI row 5 is at `z=2.33`, so the target is not bracketed without extrapolation. Ly-alpha BAO at `z=2.33` remains cross-probe/context control only, not independent clock support.

## Boundaries

```text
forbidden_inputs_used=false
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_validation_claimed=false
```

No endpoint residuals, endpoint scores, fit statistics, endpoint replay, endpoint validation, or physical validation were used or authorized.

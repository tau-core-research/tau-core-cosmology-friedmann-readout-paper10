# Paper10 DESI shape row2 left-endpoint window review notes v1

## Decision

`ALLOW_CAVEATED_LEFT_ENDPOINT_SOURCE_WINDOW_ROUTE_NO_REPLAY`

## Scope

This completed review is source-side only. It does not authorize endpoint replay, endpoint validation, physical validation, endpoint-pair replacement, or row2 promotion.

## Basis

The package freezes row2 left endpoint `z=0.934` with current endpoint family `Simon et al.`.

The strict endpoint-support window remains:

```text
|Delta z| <= 0.05
```

The relaxed context window is:

```text
|Delta z| <= 0.10
```

Frozen source-side near-misses:

```text
Stern et al. (2010), z=0.88, |Delta z|=0.054
Moresco et al. (2012), z=0.8754, |Delta z|=0.0586
```

Both are independent of the current Simon et al. endpoint family and fall within the relaxed context window, but both are outside the strict endpoint window.

## Completed answers

```text
Q1_STRICT_WINDOW_STATUS = ALLOW_CAVEATED_WINDOW_REVIEW_ROUTE
Q2_NEARMISS_ELIGIBILITY = ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE
Q3_RELEASE_POLICY = SOURCE_REOPEN_ONLY_NO_REPLAY
```

## Boundary

```text
forbidden_inputs_used=false
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_validation_claimed=false
claim_boundary=paper10_desi_shape_row2_left_endpoint_window_review_not_validation
```

## Interpretation

The two left-endpoint near-misses may be retained as caveated source-side context and can reopen the source-window acquisition route.

They do not satisfy strict endpoint-pair independence, do not replace the row2 endpoint pair, do not make row2 promotion-ready, and do not authorize replay.

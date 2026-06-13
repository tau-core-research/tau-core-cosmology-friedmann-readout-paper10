# Paper10 DESI shape row2 source-native shape-support review notes v1

## Decision

```text
ACCEPT_AS_CAVEAT_REDUCING_SOURCE_NATIVE_SHAPE_CONTEXT_NOT_REPLAY_NOT_VALIDATION
```

## Scope

This is a source-side review only. It does not authorize endpoint replay, endpoint validation, physical validation, endpoint scoring, route promotion, or endpoint-ready status.

## Reviewed object

- Row-2 interval: `z=0.934--1.321`
- Source-native DESI DR2 BAO rows: 4
- Quantities: `DM/rs` and `DH/rs` at both endpoints
- Shape vector:
  - `delta_log_DM_over_rs = 0.246281910984`
  - `delta_log_DH_over_rs = -0.218701863111`
  - `delta_log_anisotropy_DM_over_DH = 0.464983774095`
  - `slope_log_DM_over_rs = 0.636387366883`
  - `slope_log_DH_over_rs = -0.565121093311`

## Rationale

The package-internal manifest validates byte counts and SHA-256 hashes for all included files. The scout summary states that the row-2 DESI BAO covariance subblock is positive definite with minimum eigenvalue approximately `0.019944`. The source-native shape vector can therefore be retained as caveat-reducing row-2 source-side context.

## Boundaries preserved

```text
forbidden_inputs_used=false
uses_endpoint_scores=false
uses_endpoint_residuals=false
row2_endpoint_ready=false
row2_promotion_ready=false
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_validation_claimed=false
```

## Completion check

```text
pass
```

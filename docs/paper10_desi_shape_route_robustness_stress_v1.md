# DESI Shape-Route Robustness Stress V1

**Doc class:** permission-replay robustness ledger.

**Reader role:** Paper 10 endpoint runner/reviewer.

**Status:** built after authorized replay; not endpoint validation; not physical validation.

**Canonical parent:** `paper10_desi_shape_route_replay_run_template_v1.md`.

This ledger stress-tests the already authorized DESI shape-route replay without
fetching new data or changing the frozen source-side scope.

It asks whether the positive `CLOCK_SLOPE_SHAPE` replay signal is robust or
mostly carried by one shape row.

## Tests

- leave-one shape-row stress,
- leave-two shape-row stress,
- alternative RMS/rank checks over replay branches,
- signed-pattern consistency against full-length controls.

## Claim Boundary

The ledger is a robustness diagnostic for a permission-only replay. It is not an
endpoint validation claim and not a physical-validation claim.

```text
paper10_desi_shape_route_robustness_stress_not_validation
```

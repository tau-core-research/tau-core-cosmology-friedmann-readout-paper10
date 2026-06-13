# DESI Shape-Bound Control Vectors V1

**Doc class:** source-side shape-control binding ledger.

**Reader role:** Paper 10 DESI time-route auditor.

**Status:** controls bound to the frozen shape route; not replay; not
validation.

**Canonical parent:** `paper10_desi_ordering_control_suite_v1.md`.

This ledger binds the declared `K_null` controls to the frozen
`CLOCK_SLOPE_SHAPE` source route where this can be done without endpoint
scores or residuals.

## Bound Controls

```text
redshift_order_shuffle  bound as a shuffled first-difference source vector
leave_row_or_pair       bound as leave-shape-row source masks
wrong_time_basis        bound as curvature and rank-reverse shape vectors
rd_prior_stress         bound as analytic null: constant beta cancels
cc_window_stress        bound as caveated source-window stress
```

The CC-window stress is bound through the Row4 source-side review chain, but
only as caveated source context. It does not release replay.

## Current Result

```text
required_control_count = 5
shape_bound_control_count = 5
unbound_control_families = none
ordering_control_suite_ready_for_replay = false
```

This closes the previous unbound-control bookkeeping gap. The route remains
below replay status because the CC-window stress is caveated and a separate
replay authorization is still missing.

## Artifacts

```text
data/source_manifest/paper10_desi_shape_bound_control_vectors_policy_v1.csv
data/derived/paper10_desi_shape_bound_control_vectors_v1.csv
data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv
scripts/build_paper10_desi_shape_bound_control_vectors_v1.py
scripts/validate_paper10_desi_shape_bound_control_vectors_v1.py
docs/paper10_desi_cc_window_stress_binding_v1.md
data/source_manifest/paper10_desi_cc_window_stress_binding_policy_v1.csv
data/derived/paper10_desi_cc_window_stress_binding_v1.csv
data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv
scripts/build_paper10_desi_cc_window_stress_binding_v1.py
scripts/validate_paper10_desi_cc_window_stress_binding_v1.py
```

## Claim Boundary

```text
paper10_desi_shape_bound_control_vectors_not_validation
```

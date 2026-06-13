# DESI CC-Window Stress Binding V1

**Doc class:** source-side CC-window stress binding ledger.

**Reader role:** Paper 10 DESI time-route auditor.

**Status:** CC-window stress bound as caveated source control; not replay; not
validation.

**Canonical parent:** `paper10_desi_shape_bound_control_vectors_v1.md`.

This gate binds the remaining `cc_window_stress` control to the frozen
`CLOCK_SLOPE_SHAPE` route using the pre-existing Row4 source-side review chain.
It does not score the shape route and does not authorize replay.

## Bound Components

```text
strict_window_simon_bracket
non_simon_strict_window_search
caveated_near_window_context
```

The strict window has two Simon et al. 2005 bracket entries around
`z_eff=1.484`, but they do not satisfy independent reference-family
redundancy. The non-Simon strict-window search is negative. The Moresco 2015
near-window source is retained only as caveated source context.

## Current Result

```text
cc_window_stress_bound_to_shape_route = true
cc_window_stress_release_policy = SOURCE_REOPEN_ONLY_NO_REPLAY
row_can_enter_replay = false
shape_route_replay_ready_after_cc_window_stress = false
```

This closes the previous unbound-control bookkeeping gap, but it does not
release replay. It says the CC-window stress is now explicitly accounted for as
a caveated control.

## Artifacts

```text
data/source_manifest/paper10_desi_cc_window_stress_binding_policy_v1.csv
data/derived/paper10_desi_cc_window_stress_binding_v1.csv
data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv
scripts/build_paper10_desi_cc_window_stress_binding_v1.py
scripts/validate_paper10_desi_cc_window_stress_binding_v1.py
```

## Claim Boundary

```text
paper10_desi_cc_window_stress_binding_not_validation
```

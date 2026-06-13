# DESI Ordering Control Suite V1

**Doc class:** source-side null/control suite ledger.

**Reader role:** Paper 10 DESI time-route auditor.

**Status:** control requirements declared; not shape-bound; not replay; not
validation.

**Canonical parent:** `paper10_desi_time_readout_shape_projection_induction_v1.md`.

This ledger freezes the `K_null` controls that must be preserved before the
DESI time/readout shape route can be reconsidered for replay. It does not run a
new endpoint score.

## Why This Exists

The five-row constant-\(\beta_{r_d}\) diagnostic failed because the
redshift-order shuffle control beat the candidate. In Tau Core readout-basis
language, this is the current quotient-survival blocker:

```text
quotient_survival_gate_status = not_proven_ordering_null_unresolved
```

Therefore a future `K_time` shape route must preserve a `K_null` control suite.

## Frozen Control Families

```text
redshift_order_shuffle  available from the negative-control diagnostic
leave_row_or_pair       required before replay
cc_window_stress        required before replay
wrong_time_basis        required before replay
rd_prior_stress         required before replay
```

Current status:

```text
required_control_count = 5
available_control_count = 1
shape_bound_control_count = 0
ordering_control_suite_ready_for_replay = false
```

## Interpretation

The suite is a declaration of required null controls, not a pass. The next
technical task is to bind these controls to the frozen shape route without
using endpoint residuals or endpoint scores.

A first shape-bound control-vector ledger now performs that binding where it is
source-side safe. All five controls can now be bound without endpoint scoring:
redshift-order shuffle, leave-shape-row masks, wrong-time-basis vectors, the
analytic \(r_d\)-prior null for first differences, and CC-window stress as a
caveated source-window control. This closes the unbound-control bookkeeping gap,
but the suite still does not release replay.

## Artifacts

```text
data/source_manifest/paper10_desi_ordering_control_suite_policy_v1.csv
data/derived/paper10_desi_ordering_control_suite_v1.csv
data/derived/paper10_desi_ordering_control_suite_v1_summary.csv
scripts/build_paper10_desi_ordering_control_suite_v1.py
scripts/validate_paper10_desi_ordering_control_suite_v1.py
docs/paper10_desi_shape_bound_control_vectors_v1.md
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
paper10_desi_ordering_control_suite_not_validation
```

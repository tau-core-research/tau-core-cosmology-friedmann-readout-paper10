# DESI Time-Readout Shape Independent Review V1

**Doc class:** source-side independent review handoff.

**Reader role:** external reviewer without repository access.

**Status:** review package; not completed; not endpoint replay; not validation.

**Canonical parent:** `paper10_desi_time_readout_shape_observable_gate_v1.md`.

The DESI/chronometer constant-level replay was not control-resistant. A
source-side shape observable has therefore been frozen using adjacent
first-differences and uneven-grid curvature proxies of
\(-\log(D_H/r_d)-\log H_{\rm CC}\). This removes the constant
\(\beta_{r_d}\) nuisance and produces a candidate shape.

This review asks only whether that shape observable may be retained as a
caveated source-side diagnostic candidate. It does not authorize endpoint
replay.

The package also includes the companion Tau Core projection-induction ledger.
That ledger maps the clock-slope and curvature shapes to `K_time`, keeps radial
BAO level information as `K_closure` context, and keeps ordering controls as
`K_null`. It records the theory status as incomplete projection induction, not
as a validated time-projection channel.

The package further includes the first `K_null` ordering-control suite ledger.
It declares five required controls for any future shape replay:
`redshift_order_shuffle`, `leave_row_or_pair`, `cc_window_stress`,
`wrong_time_basis`, and `rd_prior_stress`. Only the redshift-order shuffle is
currently available from the negative-control diagnostic; none are yet bound to
the shape route.
The accompanying shape-bound control-vector ledger then binds four of these
five controls without endpoint scoring. A subsequent CC-window stress binding
ledger closes the fifth control as caveated source context. The control suite
is therefore shape-bound, but replay is still not authorized.

## Reviewer Scope

The reviewer should check:

1. the shape observable is derived only from frozen DESI/CC source-side ledgers
   and covariance;
2. the constant \(\beta_{r_d}\) nuisance is removed before the shape rows are
   recorded;
3. endpoint residuals, endpoint scores, late-time fits, posterior chains, and
   validation language are absent from the review decision;
4. the caveats remain explicit: high-\(z\) clock support is missing and
   multi-clock support is incomplete;
5. the Tau Core mapping is not overpromoted: the shape is a `K_time` candidate,
   while quotient survival, closure stability, and 4D readout survival remain
   below endpoint status;
6. the declared `K_null` control suite is retained as a blocker before replay.

## Current Source-Side State

```text
shape_observable_candidate_available = true
endpoint_ready_shape_observable = false
first_difference_rows = 4
second_difference_rows = 3
multi_clock_support_endpoint_ready = false
relaxed_multi_clock_failed_radial_indices = 4
high_z_row_can_enter_replay = false
tau_core_mapping_verdict = time_shape_maps_to_K_time_candidate_but_projection_induction_incomplete
ordering_control_suite_ready_for_replay = false
shape_bound_control_count = 5
unbound_control_families = none
cc_window_stress_release_policy = SOURCE_REOPEN_ONLY_NO_REPLAY
```

## Allowed Positive Outcome

A positive response may only say:

```text
retain_as_caveated_source_side_shape_candidate
```

It must not enable endpoint replay, endpoint validation, or physical validation.

## Claim Boundary

```text
paper10_desi_time_readout_shape_independent_review_not_validation
```

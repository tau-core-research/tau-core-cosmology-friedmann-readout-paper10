# DESI Time-Readout Shape Observable Gate V1

**Doc class:** source-side time/readout shape gate.

**Reader role:** Paper 10 time-level route auditor.

**Status:** shape candidates frozen; not endpoint replay; not validation.

**Canonical parent:** `paper10_desi_time_readout_expansion_manifest_v1.md`.

The first DESI/chronometer replay failed because a constant
\(\beta_{r_d}\)-level observable over five rows was not control-resistant. This
gate derives source-side shape candidates that remove the constant
\(\beta_{r_d}\) nuisance before any future replay is considered.

## Shape Construction

For each CC-matched DESI row, define the source-side level:

```text
beta_like_i = -log(D_H/r_d)_i - log H_CC,i
```

The constant \(r_d\)-nuisance level is removed by adjacent first differences:

```text
first_difference_i = (beta_like_{i+1} - beta_like_i) / (z_{i+1} - z_i)
```

The gate also freezes an uneven-grid curvature proxy:

```text
second_difference_curvature_shape
```

Both covariance estimates are propagated from the frozen BAO covariance and the
frozen CC diagonal uncertainties. No endpoint residuals, baseline scores,
late-time fitted parameters, or post-hoc row choices are used.

## Result

```text
input_cc_matched_rows = 5
high_z_row_included = false
constant_beta_nuisance_removed = true
first_difference_rows = 4
second_difference_rows = 3
first_difference_cov_rank = 4
second_difference_cov_rank = 3
first_difference_max_abs_snr_diag = 1.903233
second_difference_max_abs_snr_diag = 1.723197
shape_observable_candidate_available = true
endpoint_ready_shape_observable = false
```

## Interpretation

The source-side shape observable exists and removes the constant
\(\beta_{r_d}\) nuisance, but it remains underpowered: it still uses only the
five nearest-neighbor CC-matched DESI rows, and the high-z clock-support audit
keeps the `z=2.33` Ly-alpha row outside replay. Therefore this is a shape
candidate, not an endpoint-ready time/readout observable.

A companion Tau Core mapping ledger records the current theory status:

```text
CLOCK_SLOPE_SHAPE      -> K_time
CLOCK_CURVATURE_SHAPE  -> K_time
BAO_LEVEL_CONTEXT      -> K_closure
ORDERING_NULL_CONTROL  -> K_null
```

The projection-induction status is deliberately incomplete. The shape
observable has source-candidate activation, but quotient survival, closure
stability, and 4D readout survival remain below endpoint status.

## Artifacts

```text
data/source_manifest/paper10_desi_time_readout_shape_observable_gate_policy_v1.csv
data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv
data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv
scripts/build_paper10_desi_time_readout_shape_observable_gate_v1.py
scripts/validate_paper10_desi_time_readout_shape_observable_gate_v1.py
docs/paper10_desi_time_readout_shape_projection_induction_v1.md
data/source_manifest/paper10_desi_time_readout_shape_projection_induction_policy_v1.csv
data/derived/paper10_desi_time_readout_shape_projection_induction_v1.csv
data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv
scripts/build_paper10_desi_time_readout_shape_projection_induction_v1.py
scripts/validate_paper10_desi_time_readout_shape_projection_induction_v1.py
```

## Claim Boundary

```text
paper10_desi_time_readout_shape_observable_gate_not_validation
```

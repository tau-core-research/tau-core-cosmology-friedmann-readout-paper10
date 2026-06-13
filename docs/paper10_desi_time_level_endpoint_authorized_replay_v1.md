# DESI Time-Level Endpoint Authorized Replay V1

**Doc class:** permission-only endpoint replay result.

**Reader role:** Paper 10 endpoint auditor.

**Status:** authorized replay completed; not endpoint validation; not physical
validation.

**Canonical parent:** `paper10_desi_time_level_endpoint_replay_run_template_v1.md`.

This replay uses the completed authorization response:

```text
decision=GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY
```

and the frozen DESI/CC five-row scope:

```text
allowed radial rows: 0;1;2;3;4
excluded high-z row: 5
```

## Observable

For each authorized row, the source-side time-level observable is:

```text
y_BAO = -log(D_H / r_d) = log H_CC + beta_rd
```

The replay fits a constant nuisance `beta_rd` over the five rows. This nuisance
is not treated as a Tau Core signal.

## Result

```text
candidate_beta_rd = -7.58183919964
candidate_sigma_beta_rd = 0.0544821525192
candidate_chi2 = 5.52425578108
best_control_branch = redshift_order_shuffle_control
best_control_chi2 = 2.14549721198
family_survives_controls = false
verdict = desi_time_level_permission_replay_not_control_resistant_not_validation
```

The replay therefore does not support validation language. The five-row DESI/CC
time-level consistency check is runnable and source-frozen, but the current
candidate is not control-resistant on this scope.

## Claim Boundary

```text
paper10_desi_time_level_endpoint_authorized_replay_permission_only_not_validation
```

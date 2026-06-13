# DESI Time-Level Negative-Control Diagnostic V1

**Doc class:** endpoint diagnostic; negative-control explanation.

**Reader role:** Paper 10 endpoint auditor.

**Status:** diagnostic built; not endpoint validation; not physical validation.

**Canonical parent:** `paper10_desi_time_level_endpoint_authorized_replay_v1.md`.

This diagnostic explains why the permission-only DESI/chronometer time-level
replay is not control-resistant. It does not modify the candidate, add a new
kernel, retune an amplitude, or promote the DESI route to validation.

## Inputs

The diagnostic consumes only already frozen replay artifacts:

```text
data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_grid.csv
data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_summary.csv
data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv
data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv
```

The five authorized DESI/CC rows remain:

```text
0;1;2;3;4
```

The high-redshift row 5 remains excluded from this first replay.

## Diagnostic Result

The replay fits a constant nuisance level:

```text
beta_rd = -7.58183919964
candidate_chi2 = 5.52425578108
candidate_chi2_per_dof = 1.38106394527
```

The best frozen control is still:

```text
best_control_branch = redshift_order_shuffle_control
redshift_shuffle_chi2 = 2.14549721198
```

The largest diagonal candidate pull occurs at:

```text
radial_index = 3
z_eff = 1.321
candidate_diag_pull = -1.89077966
```

The resulting failure mode is:

```text
five_row_time_level_constant_beta_endpoint_is_ordering_fragile
```

## Interpretation

The candidate is not numerically catastrophic as a five-row consistency check,
but it is not distinctive. Several frozen controls, especially the deterministic
redshift-order shuffle, give a lower chi-square. Therefore the present DESI/CC
time-level route is best read as a useful negative-control diagnostic: a richer
independent clock support set or a more informative time/readout observable is
required before any endpoint claim can be considered.

## Artifacts

```text
data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_rows.csv
data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_branches.csv
data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_summary.csv
paper10_submission_source/figures/fig_desi_time_level_negative_control_diagnostic.pdf
scripts/build_paper10_desi_time_level_negative_control_diagnostic_v1.py
scripts/validate_paper10_desi_time_level_negative_control_diagnostic_v1.py
```

## Claim Boundary

```text
paper10_desi_time_level_negative_control_diagnostic_not_validation
```

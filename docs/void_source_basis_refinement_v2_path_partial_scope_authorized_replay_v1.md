# V2 Path Partial-Scope Authorized Replay v1

**Doc class:** permission-only diagnostic replay  
**Status:** authorized replay output; not validation; not physical lensing-path claim  
**Canonical parent:** `docs/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_v1.md`

This replay uses only the 12 predeclared partial `W_path` rows accepted by the
source-side review and permission-only replay authorization.

It does not enable the full low-z `W_path` channel.  The remaining 412 low-z
rows remain outside this replay scope.  The tile-proximity value remains a
source-side control proxy, not a calibrated physical lensing-path weight.

## Branches

```text
baseline_only
partial_W_path_candidate
path_off_control
wrong_sign_path_control
deterministic_shuffle_path_control
rank_reverse_path_control
```

All branches are evaluated on the same 12-row partial path-scope subset using
the low-z Pantheon covariance submatrix.

## Artifacts

```text
data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_run_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_grid.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_summary.csv
scripts/run_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1.py
```

## Current Result

The permission-only replay is executed on exactly 12 rows.  It produces a small
chi2 improvement relative to the baseline:

```text
delta_chi2_candidate_minus_baseline=-0.20237914656
```

However, the candidate worsens AIC relative to the baseline and ranks third
among the candidate/control set:

```text
candidate_rank_by_chi2_among_candidate_and_controls=3
controls_better_than_candidate_chi2=2
best_control_branch=rank_reverse_path_control
```

This is a weak caveated diagnostic replay. It does not support a positive
endpoint reading for the current partial `W_path` control.

## Claim Boundary

```text
v2_path_partial_scope_authorized_replay_permission_only_not_validation
```

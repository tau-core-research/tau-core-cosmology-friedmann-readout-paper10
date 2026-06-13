**Doc class:** permission-only replay result
**Reader role:** Paper10 observer/path projection audit
**Status:** authorized narrow replay; not endpoint validation
**Canonical parent:** README.md

# V2 Observer-Basis Authorized Replay

This replay is executed only after the completed external reviewer response
returned:

```text
GO_OBSERVER_BASIS_REPLAY_PERMISSION_ONLY
```

The replay uses the predeclared source-side family:

```text
W_path_x_sky_x_x_zcenter
```

on the frozen 12-row partial path scope. It compares the primary family against
the required controls:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
```

It is not population validation and not a physical path-weight derivation.

## Result

The authorized replay survives its frozen controls:

```text
delta_chi2_candidate_minus_baseline = -0.58072431813
delta_chi2_candidate_minus_best_control = -0.08783266799
candidate_rank_by_chi2_among_candidate_and_controls = 1
controls_better_than_candidate_chi2 = 0
family_survives_controls = true
verdict = observer_basis_permission_replay_family_control_survives_not_validation
```

This is the strongest current narrow observer/projection replay in the low-z
source-basis sequence. It remains a 12-object permission-only diagnostic replay,
not population validation.

## Claim Boundary

```text
v2_observer_basis_authorized_replay_permission_only_not_validation
```

**Doc class:** permission-only replay result
**Reader role:** Paper10 observer/path projection audit
**Status:** authorized narrow replay; not endpoint validation
**Canonical parent:** README.md

# V2 Observer-Orientation Kernel Authorized Replay

This replay is executed only after the completed external reviewer response
returned:

```text
GO_OBSERVER_ORIENTATION_V2_REPLAY_PERMISSION_ONLY
```

The replay uses the predeclared source-side kernel:

```text
K_v2 = W_path * (sky_z - mean_sky_z_scope)
```

on the frozen 12-row partial path scope. It compares the primary kernel against
the required controls:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
axis_x_reference
axis_y_reference
```

It is not population validation and not a physical path-weight derivation.

## Result

The authorized replay improves the baseline chi2 but does not survive the
predeclared controls:

```text
delta_chi2_candidate_minus_baseline = -0.47326976306
delta_chi2_candidate_minus_best_control = 0.01875086453
candidate_rank_by_chi2_among_candidate_and_controls = 2
controls_better_than_candidate_chi2 = 1
family_survives_controls = false
verdict = observer_orientation_v2_permission_replay_not_control_resistant_not_validation
```

Interpretation: the centered observer-orientation kernel is a useful diagnostic
negative. It retains baseline improvement on the frozen 12-row scope, but the
same source-side centering does not preserve the raw `W_path_x_sky_z`
family-control survival.

## Claim Boundary

```text
v2_observer_orientation_kernel_v2_authorized_replay_permission_only_not_validation
```

# Low-z Pantheon Void Replay v1

**Doc class:** permission-only replay result  
**Status:** run completed, not validation  

This replay was run only after the completed independent authorization review
accepted one predeclared low-z Pantheon void replay:

```text
low_z_void_replay_authorized_permission_only_not_validation
```

## Scope

The replay uses the frozen low-z Pantheon subset:

```text
n_rows = 424
z_min = 0.02303
z_max = 0.10794
```

Only the `W_VOID_MATURITY` channel is active. The following channels remain
disabled:

```text
W_WEB_ANISOTROPY
W_PATH_PROJECTION
W_TIME_READOUT
```

## Result

The void-only replay slightly improves the low-z distance chi-square relative
to the baseline:

```text
delta_chi2_void_minus_baseline = -0.37847238
```

However, after the predeclared AIC penalty the replay is worse:

```text
delta_aic_void_minus_baseline = +1.62152762
```

It also does not beat all controls:

```text
candidate_rank_by_chi2_among_void_and_controls = 2
controls_better_than_candidate_chi2 = 1
```

The shuffled low-z void control is marginally better in chi-square than the
candidate. This prevents any validation reading.

## Verdict

This result is a weak/mixed low-z replay outcome. It is useful because it checks
whether the low-z void source basis has an isolated distance-side signal on its
own supported scope. It does not provide source-complete validation of the void
channel and does not reopen the full-Pantheon void endpoint.

The preserved claim boundary is:

```text
low_z_void_replay_permission_only_not_validation
```

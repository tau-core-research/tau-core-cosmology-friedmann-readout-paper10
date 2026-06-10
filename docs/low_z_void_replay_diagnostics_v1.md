# Low-z Void Replay Diagnostics v1

**Doc class:** diagnostic, not validation  
**Parent result:** `LOW_Z_PANTHEON_VOID_REPLAY_RUN_V1`

The low-z replay gave a weak/mixed result: the void-only candidate slightly
improved low-z distance chi-square, but worsened AIC and did not beat all
controls. This diagnostic records why the result should not be promoted.

## Diagnostic result

```text
diagnosis = grid_edge_pressure_and_shuffled_control_beats_candidate
```

The key checks are:

```text
delta_chi2_void_minus_baseline = -0.37847238
delta_aic_void_minus_baseline = +1.62152762
shuffled_minus_candidate_chi2 = -0.418170454
candidate_omega_m_at_grid_edge = true
candidate_omega_void_at_grid_edge = true
```

The shuffled control being better means the present void source-basis pattern is
not control-unique on this low-z distance block. The grid-edge result means the
best candidate is also pushing against the frozen grid boundary. Together these
point to a weak or under-resolved source-basis proxy, not to a validated void
channel.

## Interpretation

This is not a reason to retune the amplitude or widen the grid post hoc. The
correct next step is source-side: refine or rebuild the void source basis before
any new void endpoint is considered.

The preserved claim boundary is:

```text
low_z_void_replay_diagnostic_not_validation
```

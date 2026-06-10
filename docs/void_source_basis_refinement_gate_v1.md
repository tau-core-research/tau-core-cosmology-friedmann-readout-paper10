# Void Source-Basis Refinement Gate v1

**Doc class:** source-side refinement gate  
**Status:** not scoring, not validation  

This gate follows the low-z void replay diagnostic. It freezes the reason why
the current `W_VOID_MATURITY` basis is not endpoint-ready and what must be
changed before any new void replay is proposed.

## Parent diagnostic

The parent diagnostic verdict is:

```text
grid_edge_pressure_and_shuffled_control_beats_candidate
```

The relevant symptoms are:

```text
delta_chi2_void_minus_baseline = -0.37847238
delta_aic_void_minus_baseline = +1.62152762
shuffled_minus_candidate_chi2 = -0.418170454
candidate_omega_m_at_grid_edge = true
candidate_omega_void_at_grid_edge = true
void_basis_pearson_r_with_zHD ~= 0.925
```

## Gate verdict

```text
current_W_void_not_endpoint_ready_redshift_degenerate_not_control_unique
```

The present void basis is too redshift-like and not control-unique on the
low-z Pantheon distance block. This does not validate or refute a Tau Core void
channel. It blocks further void endpoint attempts using this basis.

## Required source-side refinement

A future void basis must be built from residual-blind source data that can
separate void morphology/environment from redshift ordering:

- void depth;
- void radius;
- wall distance;
- host-to-void position;
- line-of-sight environment;
- sky direction;
- catalogue selection function.

It must pass source-side independence checks before scoring:

- low correlation with redshift;
- low correlation with source row index;
- resistance to deterministic shuffled controls;
- resistance to wrong-sign controls;
- resistance to threshold controls.

## Forbidden route

The following are explicitly forbidden:

- fitting the basis from distance residuals;
- changing the row mask after seeing score improvement;
- changing thresholds after seeing score improvement;
- tuning the amplitude or covariance to rescue the replay.

## Next allowed artifact

The next allowed artifact is only:

```text
void_source_basis_refinement_acquisition_manifest_v1
```

No endpoint scoring is opened by this gate.

## Claim boundary

```text
void_source_basis_refinement_gate_not_scoring_not_validation
```

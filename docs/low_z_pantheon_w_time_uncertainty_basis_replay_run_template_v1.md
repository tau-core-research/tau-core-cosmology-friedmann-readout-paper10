# Low-z Pantheon+ W-time uncertainty-basis replay run template v1

**Doc class:** replay run template
**Status:** prepared; authorization required; not scoring; not validation
**Canonical parent:** `docs/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_v1.md`

This template predeclares the candidate/control replay grammar for the frozen
`W_time_uncertainty_basis_candidate`.

It does not authorize replay.  The replay script must not run unless a
completed authorization response summary exists with:

```text
decision=GO_W_TIME_UNCERTAINTY_BASIS_REPLAY_PERMISSION_ONLY
endpoint_replay_allowed=true
endpoint_validation_claimed=false
physical_validation_claimed=false
```

## Candidate and controls

Candidate:

```text
W_time_uncertainty_basis
```

Controls:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
```

Disabled channels:

```text
W_VOID_SOURCE_BASIS_REFINEMENT
W_WEB_ANISOTROPY
W_PATH_PROJECTION
FULL_OBSERVER_PATH_KERNEL
PHYSICAL_CLOCK_DRIFT_CLAIM
```

The template forbids residual-driven activation, late-time fit parameter
selection, post-hoc `H(z)` smoothing, post-hoc clock anomaly labels,
post-hoc time-channel selection, post-hoc row selection, amplitude tuning,
covariance reweighting, endpoint score claims, and physical validation claims.

## Run

After an accepted authorization summary exists:

```bash
python scripts/run_low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1.py
python scripts/validate_low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1.py
```

Claim boundary:

```text
w_time_uncertainty_basis_replay_template_not_validation
```

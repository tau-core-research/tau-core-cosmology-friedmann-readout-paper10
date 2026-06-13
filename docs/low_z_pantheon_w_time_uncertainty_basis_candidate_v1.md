# Low-z Pantheon+ W-time uncertainty basis candidate v1

**Doc class:** source-side `W_time` basis-candidate freeze
**Reader role:** Paper 10 R6 time/readout activation boundary audit
**Status:** `W_time` basis candidate frozen; endpoint replay not authorized
**Canonical parent:** `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`

This artifact turns the residual-blind `Delta_clock_uncertainty_candidate` into
a source-normalized basis candidate:

```text
W_time_uncertainty_basis
  = (Delta_clock_uncertainty_candidate - source_mean) / source_std
```

The normalization is computed only from the source-side low-z candidate rows.
It does not use Pantheon+ distance residuals, endpoint scores, late-time fit
parameters, or post-hoc clock labels.

This is not an endpoint replay and not a validation result.  It only provides a
candidate time/readout basis that could later be submitted to a separate
authorization review.

Run:

```bash
python scripts/build_low_z_pantheon_w_time_uncertainty_basis_candidate_v1.py
python scripts/validate_low_z_pantheon_w_time_uncertainty_basis_candidate_v1.py
```

Outputs:

- `data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1.csv`
- `data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1_summary.csv`

Claim boundary:

```text
w_time_uncertainty_basis_candidate_source_side_not_scoring_not_validation
```

Interpretation:

This narrows the R6 activation blocker by freezing a reproducible source-side
`W_time` basis candidate.  It still does not authorize endpoint scoring.  The
next required step is a predeclared replay-authorization review or a broader
source-side control audit before this basis can enter scoring.

# Low-z Pantheon+ time/readout Delta-clock uncertainty candidate v1

**Doc class:** source-side `Delta_clock` candidate freeze
**Reader role:** Paper 10 R6 time/readout claim-boundary audit
**Status:** uncertainty-channel `Delta_clock` candidate frozen; no `W_time`
**Canonical parent:** `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`

This artifact freezes the most conservative current `Delta_clock` candidate:
an uncertainty-channel contrast computed only from the fetched/frozen
cosmic-chronometer `H(z)` table.

For each low-z Pantheon+ row, the already frozen redshift-bin policy assigns a
cosmic-chronometer support cell.  The candidate is then:

```text
Delta_clock_uncertainty_candidate
  = log((errHz/Hz)_assigned_CC_bin / median(errHz/Hz)_CC)
```

This is a dimensionless source-side contrast.  It is not a physical clock-drift
measurement and not a fitted late-time acceleration term.

It does not compute:

- `W_time`,
- a smoothed `H(z)` curve,
- a late-time fit parameter,
- a distance residual,
- an endpoint score.

Run:

```bash
python scripts/build_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.py
python scripts/validate_low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.py
```

Outputs:

- `data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.csv`
- `data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1_summary.csv`

Claim boundary:

```text
time_readout_delta_clock_uncertainty_candidate_source_side_not_scoring_not_validation
```

Interpretation:

This narrows the R6 blocker by providing a reproducible, residual-blind
`Delta_clock` candidate in the uncertainty/readout channel.  It still does not
activate a numeric `W_time` term.  A future activation rule would require a
separate, predeclared transformation from this candidate to a time/readout
kernel.

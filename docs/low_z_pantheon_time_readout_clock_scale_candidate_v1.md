# Low-z Pantheon+ time/readout clock-scale candidate v1

**Doc class:** source-side scale-candidate freeze
**Reader role:** Paper 10 R6 time/readout claim-boundary audit
**Status:** `Delta_clock_star` candidate frozen; no `Delta_clock`; no `W_time`
**Canonical parent:** `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`

This artifact freezes a conservative source-side candidate for the
time/readout consistency scale:

```text
Delta_clock_star_candidate = median(errHz / Hz)
```

computed only from the fetched/frozen cosmic-chronometer `H(z)` table.

It does not compute a time/readout residual.  In particular, it does not
compute:

- `Delta_clock`,
- `W_time`,
- a late-time fit parameter,
- a smoothed `H(z)` curve,
- a clock anomaly label.

Run:

```bash
python scripts/build_low_z_pantheon_time_readout_clock_scale_candidate_v1.py
python scripts/validate_low_z_pantheon_time_readout_clock_scale_candidate_v1.py
```

Outputs:

- `data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1.csv`
- `data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1_summary.csv`

Claim boundary:

```text
time_readout_clock_scale_candidate_source_side_not_scoring_not_validation
```

Interpretation:

This closes only one R6 sub-blocker: the source-side scale candidate.  R6 is
still not activation-ready because the actual `Delta_clock` observable and the
numeric `W_time` rule remain missing.

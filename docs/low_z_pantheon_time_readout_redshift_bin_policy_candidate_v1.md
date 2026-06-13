# Low-z Pantheon+ time/readout redshift-bin policy candidate v1

**Doc class:** source-side bin-policy freeze
**Reader role:** Paper 10 R6 time/readout claim-boundary audit
**Status:** redshift-bin policy candidate frozen; no `Delta_clock`; no `W_time`
**Canonical parent:** `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`

This artifact freezes a conservative source-side redshift support policy for a
future time/readout channel.  It uses only:

- the fetched/frozen cosmic-chronometer `H(z)` table, and
- the already frozen SDSS BAO/RSD redshift route markers.

The assigned bins are source-native CC support cells: each CC redshift node
defines a Voronoi-like redshift interval bounded by the midpoints to adjacent
CC nodes.  Low-z Pantheon+ rows are assigned to these source-support cells.
The SDSS BAO/RSD redshift nodes are recorded as route markers only.

It does not compute:

- `Delta_clock`,
- `W_time`,
- a smoothed `H(z)` curve,
- a late-time fit parameter,
- a clock anomaly label,
- any endpoint score.

Run:

```bash
python scripts/build_low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.py
python scripts/validate_low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.py
```

Outputs:

- `data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.csv`
- `data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1_summary.csv`

Claim boundary:

```text
time_readout_redshift_bin_policy_candidate_source_side_not_scoring_not_validation
```

Interpretation:

This closes only one R6 sub-blocker: the source-side redshift-bin support
policy.  R6 is still not activation-ready because the actual `Delta_clock`
observable and the numeric `W_time` rule remain missing.

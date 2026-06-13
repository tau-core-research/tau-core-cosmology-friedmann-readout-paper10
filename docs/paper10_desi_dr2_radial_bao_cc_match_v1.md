# DESI DR2 Radial BAO to Cosmic-Chronometer Match V1

**Doc class:** source-side support ledger.

**Reader role:** Paper 10 time-level route auditor.

**Status:** source-side support ledger only; not endpoint replay; not validation.

**Canonical parent:** `paper10_desi_dr2_radial_bao_time_interface_v1.md`.

This ledger matches the six source-frozen DESI DR2 radial BAO time-interface
rows to the nearest frozen cosmic-chronometer `H(z)` support point. It performs
no smoothing, no extrapolation, no fitting, and no endpoint scoring.

## Rule

```text
match_rule = nearest_CC_support_without_smoothing
edge_policy = mark_outside_CC_range_do_not_extrapolate
```

The current frozen cosmic-chronometer table covers:

```text
z = 0.07 ... 1.965
```

The DESI radial BAO interface covers:

```text
z = 0.51 ... 2.33
```

Therefore five DESI radial rows are matched within CC support, while the
`z=2.33` Ly-alpha row is blocked as outside CC coverage. This is not a failure;
it is a guard against silently extrapolating a clock/readout support table.

## Files

```text
data/source_manifest/paper10_desi_dr2_radial_bao_cc_match_policy_v1.csv
data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv
data/derived/paper10_desi_dr2_radial_bao_cc_match_v1_summary.csv
scripts/build_paper10_desi_dr2_radial_bao_cc_match_v1.py
scripts/validate_paper10_desi_dr2_radial_bao_cc_match_v1.py
```

## Current Verdict

```text
desi_bao_cc_support_partially_matched_high_z_row_blocked_no_replay
```

This closes the source-side CC-support ledger for the matched part of the DESI
radial BAO interface, but it does not authorize replay. A future endpoint still
needs a control seed manifest and an explicit policy for the high-redshift DESI
row: either exclude it predeclared from a CC-matched replay or acquire
independent high-redshift clock/readout support.

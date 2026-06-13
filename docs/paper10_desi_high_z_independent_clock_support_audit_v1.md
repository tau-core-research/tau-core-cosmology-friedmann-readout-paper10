# DESI High-z Independent Clock-Support Audit V1

**Doc class:** source-side high-z clock/readout support audit.

**Reader role:** Paper 10 time-level route auditor.

**Status:** source-side audit built; high-z row remains holdout; not endpoint
replay; not validation.

**Canonical parent:** `paper10_desi_time_readout_expansion_manifest_v1.md`.

This audit checks the first primary source gate after the DESI/chronometer
five-row negative-control result: whether the excluded DESI radial BAO row at
`z=2.33` has independent clock/readout support sufficient to enter a future
time-level replay without extrapolation.

## Result

The frozen cosmic-chronometer table contains:

```text
cc_table_row_count = 32
cc_z_min = 0.07
cc_z_max = 1.965
```

The excluded DESI row is:

```text
target_radial_index = 5
target_z_eff = 2.33
```

The nearest frozen clock support is:

```text
nearest_frozen_clock_z = 1.965
delta_z_to_nearest_frozen_clock = 0.365
nearest_frozen_clock_reference = Moresco (2015)
```

Therefore:

```text
target_within_frozen_cc_support = false
target_bracketed_without_extrapolation = false
endpoint_ready_support_count = 0
high_z_row_can_enter_replay = false
```

## Verdict

```text
desi_high_z_clock_support_missing_row_remains_holdout_not_validation
```

## Interpretation

The high-redshift DESI Ly-alpha row remains a holdout. It cannot be promoted
into the DESI time-level replay using the current frozen clock table, because
doing so would require extrapolating beyond the frozen cosmic-chronometer
support. A future route would need either a source-frozen high-z clock
compilation near `z=2.33` or a separately derived cross-probe time/readout shape
observable.

## Artifacts

```text
data/source_manifest/paper10_desi_high_z_independent_clock_support_audit_policy_v1.csv
data/derived/paper10_desi_high_z_independent_clock_support_audit_v1.csv
data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv
scripts/build_paper10_desi_high_z_independent_clock_support_audit_v1.py
scripts/validate_paper10_desi_high_z_independent_clock_support_audit_v1.py
```

## Claim Boundary

```text
paper10_desi_high_z_independent_clock_support_audit_not_validation
```

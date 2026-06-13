# DESI Multi-Clock Support Per BAO Row Audit V1

**Doc class:** source-side clock-redundancy audit.

**Reader role:** Paper 10 DESI time/readout route auditor.

**Status:** multi-clock support incomplete; not endpoint replay; not validation.

**Canonical parent:** `paper10_desi_time_readout_expansion_manifest_v1.md`.

The first DESI/chronometer endpoint used one nearest cosmic-chronometer support
point per authorized DESI radial BAO row. After the constant-level replay failed
the ordering controls, the expansion manifest required independent clock
redundancy or explicit caveats before any future replay route.

## Rule

The audit uses only the frozen cosmic-chronometer table and the frozen DESI/CC
match ledger. It checks the five authorized radial rows:

```text
0, 1, 2, 3, 4
```

Two redshift windows are recorded:

```text
strict_delta_z_window = 0.05
relaxed_delta_z_window = 0.10
```

A row passes a window only if it has at least two clock entries and at least two
independent reference sources within that window. No endpoint residuals,
endpoint scores, late-time fit parameters, outlier rejection, CC smoothing, or
post-hoc clock choices are used.

## Result

```text
authorized_row_count = 5
strict_multi_clock_pass_count = 3
relaxed_multi_clock_pass_count = 4
relaxed_multi_clock_failed_radial_indices = 4
multi_clock_support_endpoint_ready = false
```

The strict window fails rows 2 and 4. The relaxed window rescues row 2, but row
4 still has only one independent reference source even though it has two clock
entries. Therefore the current DESI/CC time-readout route does not yet have
complete independent multi-clock support.

## Interpretation

This is a useful blocker, not a negative physics result. The shape observable is
now available source-side, but the clock redundancy behind it is still uneven.
The next allowed route is either an independent shape review that accepts the
caveated five-row support as a diagnostic-only object, or a new clock
compilation/source route that gives row 4 and the high-z holdout stronger
independent support.

## Artifacts

```text
data/source_manifest/paper10_desi_multi_clock_support_per_bao_row_audit_policy_v1.csv
data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1.csv
data/derived/paper10_desi_multi_clock_support_per_bao_row_audit_v1_summary.csv
scripts/build_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py
scripts/validate_paper10_desi_multi_clock_support_per_bao_row_audit_v1.py
```

## Claim Boundary

```text
paper10_desi_multi_clock_support_per_bao_row_audit_not_validation
```

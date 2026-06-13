# DESI DR2 High-z BAO Policy V1

**Doc class:** source-side scope policy.

**Reader role:** Paper 10 time-level route auditor.

**Status:** source-side policy only; not endpoint replay; not validation.

**Canonical parent:** `paper10_desi_dr2_radial_bao_cc_match_v1.md`.

The DESI DR2 radial BAO interface contains one high-redshift Ly-alpha row at
`z=2.33`. The frozen cosmic-chronometer support table ends at `z=1.965`, so this
row cannot be treated as CC-matched without extrapolation.

## Accepted Policy

```text
exclude_from_first_CC_matched_time_endpoint_no_extrapolation
```

The first CC-matched DESI time-level endpoint candidate may use only the five
DESI radial rows that lie inside the frozen CC support range. The `z=2.33` row
is retained as a high-z holdout/control or future route candidate, not silently
discarded.

## Forbidden

```text
CC_extrapolation
posthoc_include_after_score
posthoc_exclude_after_score
using_LyA_row_as_CC_matched_clock_support
endpoint_scores
Pantheon_distance_residuals
late_time_fit_parameters
```

## Current Verdict

```text
high_z_lya_row_predeclared_excluded_from_first_cc_matched_time_endpoint
```

This closes the high-z support policy blocker. It does not open endpoint replay;
the next required gate is a frozen time-level control seed manifest.

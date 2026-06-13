# Paper 10 time-level BAO support expansion manifest v1

**Doc class:** source-side acquisition/expansion manifest
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time-level external-r_d readiness gate

The current time-level route is blocked because the frozen SDSS radial BAO
route contains only two usable `D_H/r_d` rows and the two-point differential
signal has low significance.

This manifest freezes the allowed source-side expansion routes before any
additional radial BAO values are fetched or scored.  It does not import new
values and it does not authorize endpoint replay.

Current route:

```text
CURRENT_SDSS_DR16_MULTITRACER_RADIAL_BAO
```

Candidate expansion routes:

```text
CANDIDATE_DESI_PUBLIC_RADIAL_BAO
CANDIDATE_EBOSS_LYA_QSO_RADIAL_BAO
CANDIDATE_LOWZ_BAO_COMPILATION_CROSSCHECK
```

Required fields for any future imported radial BAO row:

```text
z_eff
radial_BAO_observable
uncertainty_or_covariance
tracer_sample
release_id or source identifier
source_url_or_doi
product_hash
```

Forbidden inputs:

```text
Pantheon_distance_residuals
endpoint_scores
late_time_fit_parameters
posthoc_BAO_source_selection
posthoc_redshift_bin_selection
posthoc_rd_tuning
```

The protocol target for a future endpoint is at least four independent radial
BAO support bins plus the declared controls from the time-level control-suite
protocol.  The threshold is a protocol guardrail, not a Tau Core prediction.
The present package still has only two radial bins and therefore remains
endpoint-blocked.

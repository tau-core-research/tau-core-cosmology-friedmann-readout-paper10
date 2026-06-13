# Paper 10 external r_d prior freeze protocol v1

**Doc class:** source-side nuisance-prior freeze protocol
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time-level r_d policy selection gate

This protocol defines how a future external \(r_d\) prior may be frozen for the
`time_level_route`.

It does not select a numerical \(r_d\) value. It defines the admissible source
fields and leakage guards for a later completed response.

Required fields:

```text
prior_source_id
rd_mpc
sigma_rd_mpc
assumption_family
source_reference
source_url_or_doi
extraction_note
hash_or_page_cache
```

Forbidden inputs:

```text
Pantheon_distance_residuals
fit_statistics
endpoint_scores
late_time_fit_parameters
posthoc_prior_selection
rd_fit_from_same_endpoint
```

The future completed response must be source-side only. Even a valid response
will not by itself authorize endpoint replay; it will only close the
source-freeze part of the `external_rd_prior` route.

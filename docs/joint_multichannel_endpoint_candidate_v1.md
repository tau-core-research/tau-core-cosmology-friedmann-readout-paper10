# Joint multichannel endpoint candidate v1

**Doc class:** predeclared joint-channel preflight
**Status:** candidate score only; not a joint endpoint; not cosmological validation

This ledger is the first executable joint-channel layer above the existing
artifact meta-score.  It reads the frozen channel manifest, applies only
predeclared metric transforms, and records whether the combined pattern
remains positive before a true joint likelihood is attempted.

Forbidden interpretation: this is not an empirical validation of Tau Core
cosmology and not a replacement for covariance-aware joint endpoint scoring.

Summary:

- channels scored: `7`
- normalized joint score: `0.200059110`
- verdict: `JOINT_ENDPOINT_CANDIDATE_INCONCLUSIVE_PREVALIDATION`

Next required gate:

```text
single_predeclared_joint_likelihood_with_covariance_shuffled_and_wrong_channel_controls
```

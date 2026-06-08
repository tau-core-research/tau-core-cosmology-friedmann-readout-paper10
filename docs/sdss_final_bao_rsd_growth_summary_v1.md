# SDSS Final BAO/RSD Growth Summary V1

This artifact freezes the first growth-side summary points for Paper 10:

```text
data/source_manifest/sdss_final_bao_rsd_growth_summary_v1.csv
```

The values come from the SDSS Final BAO and RSD Measurements Table. The table
provides source-side `f sigma8(z)` summary values for MGS, BOSS, and eBOSS
samples.

## Claim Boundary

This is a diagonal-summary pilot input, not a full official likelihood.

The full covariance among BAO/RSD compressed parameters is not yet frozen here.
Therefore this artifact can support a first growth-side pipeline test, but not
a final growth endpoint validation.

## Leakage Prevention

The frozen summary may not use:

- growth residuals,
- fit-improvement flags,
- post-hoc environment labels,
- post-hoc growth sample selection.

The `W_web` value attached to each redshift is computed from the already frozen
SDSS DR17 MCPM source-native web catalogue, not from the growth residuals.

# Growth Web Source-Native Design Matrix V1

This artifact attaches the frozen source-native SDSS DR17 MCPM web-density
basis to the SDSS final BAO/RSD `f sigma8(z)` summary points.

Outputs:

```text
data/derived/growth_web_source_native_design_matrix_v1.csv
data/derived/growth_web_source_native_design_matrix_v1_summary.csv
```

## Claim Boundary

This is not endpoint validation. It is a growth-side design matrix using
diagonal-only `f sigma8` summary errors.

The matrix contains no fitted model residuals, no endpoint likelihood, and no
fit-improvement-driven labels.

## Why This Matters

The previous source-native `W_void + W_web` pilot was Pantheon-only. That means
the web channel was tested in a distance observable, where Tau Core does not
expect it to be maximally diagnostic. This design matrix moves `W_web` toward
its natural first target: structure-growth measurements.

# Pantheon Void/Web Source-Native Design Matrix V1

This artifact replaces the previous redshift/scale-factor proxy bases with
source-native void and web catalogue summaries:

```text
data/derived/pantheon_void_web_source_native_design_matrix_v1.csv
data/derived/pantheon_void_web_source_native_design_matrix_v1_summary.csv
```

It is built by:

```bash
python scripts/build_pantheon_void_web_source_native_design_matrix_v1.py
python scripts/validate_pantheon_void_web_source_native_design_matrix_v1.py
```

## Source-Native Columns

The design matrix adds:

- `W_void_source_native_basis`
- `W_web_source_native_basis`
- `r_pantheon_lowz_mpc_over_h`

The void basis is derived from the VAST/SDSS DR7 Planck2018 maximal-void table
using cumulative normalized `Reff^3` load in predeclared comoving-distance
bins. Pantheon `zHD` is mapped to a low-redshift comoving-distance proxy only
for source-side coordinate matching.

The web basis is derived from the SDSS DR17 MCPM SlimeMold catalogue using
median `matterDens` in predeclared redshift bins, robust-normalized by
source-only 10th and 90th percentiles.

## Claim Boundary

This is not endpoint scoring. The matrix contains no model predictions, no
distance residuals, no likelihoods, and no fit statistics. It only proves that
the source-native products can be transformed into leakage-safe design columns.

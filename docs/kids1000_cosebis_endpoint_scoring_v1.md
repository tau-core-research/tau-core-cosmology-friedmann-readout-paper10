# KiDS-1000 COSEBIs Endpoint Scoring v1

This artifact is the first explicit endpoint scoring run for the KiDS-1000
COSEBIs branch after the readiness ledger reached 12 ready components and zero
blockers.

It uses the frozen scoring grammar:

```text
chi2 = (d - t)^T C^{-1} (d - t)
```

where `d` is the retained 300-row KiDS COSEBIs `En` vector, `C` is the full
300 x 300 covariance solved by Cholesky, and `t` is either the zero baseline,
the source-frozen web/path candidate vector, or a predeclared null-control
vector.

Current result:

- candidate delta chi-square versus zero baseline: `-183.6152665217`;
- candidate delta AIC versus zero baseline: `-181.6152665217`;
- candidate rank by chi-square among candidate plus 1008 null controls: `3/1009`;
- plus-one null tail fraction by chi-square: `0.002973240832507`;
- candidate rank by AIC: `3/1009`;
- plus-one null tail fraction by AIC: `0.002973240832507`.

Interpretation boundary:

The run is an endpoint score, not empirical validation. The KiDS data vector is
used only for scoring after all source-side choices, candidate vectors, null
controls, and readiness gates are frozen. It is not used for source selection,
label selection, channel activation, mode cuts, tomographic selection, sky
direction choice, web/path labels, or weight selection.

The result is positive but not absolute-winner positive: two predeclared null
controls score better than the candidate under the same amplitude and
covariance policy. Therefore the claim-safe reading is a low-tail endpoint
score requiring follow-up robustness, not a KiDS lensing validation claim.

Claim boundary:

```text
kids1000_cosebis_endpoint_scoring_run_v1_endpoint_score_not_validation
```

# Void/Web Combined Multiblock Authorized Endpoint v1

## Status

This is the single combined void/web endpoint run authorized by the completed
review response:

`GO_COMBINED_VOID_WEB_ENDPOINT_PERMISSION_ONLY`.

It is an endpoint replay under the frozen protocol, not a physical validation
claim.

## Claim Boundary

- `physical_validation_claimed=false`
- `claim_boundary=combined_void_web_endpoint_permission_only_not_validation`
- CMB information is used only as low-redshift safety support, not as a CMB
  likelihood.
- The disabled channels remain disabled: `W_PATH_PROJECTION`, `W_TIME_READOUT`.

## Result

The source-native combined void/web candidate gives a small chi-square
improvement over the baseline, but it does not survive the information-criterion
or shuffled-control checks.

From `data/derived/void_web_combined_multiblock_authorized_endpoint_v1_summary.csv`:

- `candidate_delta_chi2_vs_baseline = -0.32825117`
- `candidate_delta_aic_vs_baseline = 3.67174883`
- `candidate_delta_bic_vs_baseline = 14.13576949`
- `candidate_rank_by_chi2 = 2`
- `candidate_rank_by_aic = 5`
- `best_wrong_branch = deterministic_shuffled_void_web`
- `candidate_beats_best_wrong_by_chi2 = false`
- `candidate_beats_best_wrong_by_aic = false`

## Interpretation

This is a preserved negative/weak endpoint result. The combined candidate is
not empty: it moves chi-square in the right direction. However, the effect is
too small relative to the added degrees of freedom, and the deterministic
shuffled void/web control is marginally better in chi-square and AIC.

The result therefore does not validate the current void/web combined endpoint
family. The next claim-safe step is diagnostic, not promotion: determine whether
the weakness is caused by source-native channel under-specification, the current
shared-amplitude grammar, missing path/time channels, or an actually weak
void/web cosmology signal in this observable combination.

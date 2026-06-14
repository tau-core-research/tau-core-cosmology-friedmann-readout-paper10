# Joint covariance resolution plan v1

**Doc class:** post-replay covariance blocker-resolution plan
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_covariance_resolution_plan_not_scoring_not_validation`

This plan freezes the allowed routes for resolving the second promotion
blocker in the joint guarded replay. It does not run a joint score and
does not promote the block-diagonal surrogate to validation.

Allowed routes:

1. source-native or source-frozen cross-probe covariance product;
2. caveated block-diagonal surrogate with explicit shared-sky, redshift,
   nuisance, calibration, and population-covariance caveats;
3. same-statistic matched-control binding under the chosen covariance route.

Summary:

- active channel order: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- block covariance blocks available: `3/3`
- cross-probe covariance defined: `false`
- independence rationale route ready: `true`
- fastest route: `caveated_block_diagonal_surrogate_plus_same_statistic_controls`
- verdict: `COVARIANCE_RESOLUTION_ROUTES_FROZEN_CROSS_PROBE_STILL_OPEN_NOT_SCORING`

Interpretation: the fastest viable next route is a caveated block-diagonal
surrogate plus same-statistic matched controls, but this remains a
prevalidation surrogate until a stronger covariance product or validation
protocol is reviewed separately.

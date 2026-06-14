# Joint matched-control distribution readiness v1

**Doc class:** matched-control distribution readiness audit
**Status:** available but caveated; not scoring; not validation
**Claim boundary:** `joint_matched_control_distribution_readiness_not_scoring_not_validation`

The frozen signed `z_i` protocol requires matched-control distributions
to define each channel center and scale. This audit checks whether the
current repository artifacts expose those raw control distributions.

Current result:

- ready channels: `1`
- caveated-ready channels: `2`
- blocked channels: `0`
- verdict: `MATCHED_CONTROL_DISTRIBUTIONS_AVAILABLE_CAVEATED_NOT_ZI`

The KiDS and DESI channels remain caveated because their available
control distributions come from endpoint-score or small-N permission
contexts. They are available for a future authorized `z_i` distribution
build, but this artifact still does not compute centers, scales, `z_i`,
or `T_joint`.

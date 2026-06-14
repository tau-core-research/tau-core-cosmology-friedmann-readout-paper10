# Joint matched-control distribution readiness v1

**Doc class:** matched-control distribution readiness audit
**Status:** partial; not scoring; not validation
**Claim boundary:** `joint_matched_control_distribution_readiness_not_scoring_not_validation`

The frozen signed `z_i` protocol requires matched-control distributions
to define each channel center and scale. This audit checks whether the
current repository artifacts expose those raw control distributions.

Current result:

- ready channels: `1`
- caveated-ready channels: `1`
- blocked channels: `1`
- verdict: `MATCHED_CONTROL_DISTRIBUTIONS_PARTIAL_KIDS_BLOCKED`

The KiDS channel remains blocked because the current repository exposes
top-null and family-summary artifacts, not the full raw matched-control
distribution needed by the frozen median/MAD rule.

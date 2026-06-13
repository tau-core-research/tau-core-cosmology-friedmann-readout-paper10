# Paper10 DESI Post-review Time-route Priority v1

**Doc class:** source-side route-priority ledger
**Reader role:** Paper10 DESI time/readout route reviewer
**Status:** priority frozen; not replay; not validation
**Canonical parent:** `paper10_desi_time_readout_expansion_manifest_v1.md`

This ledger updates the DESI time-route priority after the completed source
blocker review, the Row5 source scout, and the Row5 holdout confirmation.

The original expansion manifest listed high-z clock support as the primary
source gate.  After review, Row5 is frozen as holdout.  Therefore the next
scientific work should not be another attempt to replay the high-z row.  The
primary next source-side gate becomes a richer time/readout shape observable.

## Current Priority

1. `TIME_READOUT_SHAPE_OBSERVABLE`
2. `ORDERING_CONTROL_SUITE`
3. `JOINT_COVARIANCE_AND_NUISANCE_POLICY`
4. `MULTI_CLOCK_SUPPORT_PER_BAO_ROW`
5. `HIGH_Z_INDEPENDENT_CLOCK_SUPPORT`

The high-z route remains important, but only as a future holdout-reopen route
if a new independent clock or source-native time/readout source appears.

Current verdict:

`post_review_priority_is_shape_derivation_not_row5_replay`

## Claim Boundary

- no endpoint replay,
- no endpoint validation,
- no physical validation,
- no post-hoc row selection,
- no post-hoc shape selection,
- no endpoint-score-driven route selection.

# Joint permission replay promotion-readiness gate v1

**Doc class:** post-replay readiness gate
**Status:** not endpoint scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_permission_replay_promotion_readiness_not_validation`

This gate records what the guarded permission-only joint replay permits
and what it still blocks. It is deliberately conservative: a positive
permission replay can motivate the next validation protocol, but it cannot
itself become validation.

Summary:

- active blocks: `3`
- clean control-resistant blocks: `2`
- caveated support blocks: `1`
- hard blockers open: `3`
- promotion ready: `false`
- verdict: `JOINT_PERMISSION_REPLAY_POSITIVE_BUT_PROMOTION_BLOCKED_NOT_VALIDATION`

Interpretation: the joint replay has a coherent multi-block signal, but
promotion is still blocked by at least one caveated support block, incomplete
cross-probe covariance, and the lack of a fully implemented same-statistic
matched-control suite.

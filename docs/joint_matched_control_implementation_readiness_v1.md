# Joint matched-control implementation readiness v1

**Doc class:** matched-control implementation readiness ledger
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_matched_control_implementation_readiness_not_scoring_not_validation`

This ledger separates two facts that should not be conflated:
six control families have source-side design scaffolds, but no
control family is executable for validation until the single joint
statistic and covariance route are frozen for candidate and controls
together.

Summary:

- control families total: `8`
- design-ready but protocol-blocked families: `6`
- upstream-blocked families: `2`
- single statistic defined: `false`
- cross-probe covariance defined: `false`
- fastest covariance route: `caveated_block_diagonal_surrogate_plus_same_statistic_controls`
- verdict: `MATCHED_CONTROL_IMPLEMENTATION_READINESS_HAS_DESIGNS_BUT_PROTOCOL_BINDING_BLOCKED`

Interpretation: the control route is becoming implementable, but this
artifact intentionally does not run controls and does not authorize
endpoint scoring.

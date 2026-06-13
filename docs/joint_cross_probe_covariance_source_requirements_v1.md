# Joint cross-probe covariance source requirements v1

**Doc class:** source-side requirements gate
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_cross_probe_covariance_source_requirements_not_scoring_not_validation`

This gate freezes the source-side requirements needed before Paper10
can promote the best-justified joint kernel into a single covariance-aware
joint replay. It does not compute a likelihood, score, or validation result.

Two closure routes remain possible:

1. a source-native/source-frozen cross-probe covariance product;
2. a reviewer-accepted caveated block-diagonal independence rationale.

Current verdict:

`JOINT_CROSS_PROBE_CAVEATED_INDEPENDENCE_PRECONDITION_CLOSED_SCORING_AUTH_REQUIRED`

The covariance-product route remains unavailable. The reviewer has accepted a caveated block-diagonal independence precondition, but a separate scoring authorization package must still bind the statistic, covariance blocks, caveats, and matched controls before any replay.

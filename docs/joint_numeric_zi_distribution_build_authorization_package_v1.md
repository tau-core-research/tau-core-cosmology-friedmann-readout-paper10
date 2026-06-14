# Joint numeric z_i distribution build authorization package v1

**Doc class:** external authorization handoff.
**Status:** prepared, not completed.
**Claim boundary:** `joint_numeric_zi_distribution_build_authorization_not_scoring_not_validation`.

This package asks whether a numeric channel-level `z_i` distribution
build may be prepared from the frozen signed standardization protocol
and the currently exposed matched-control distributions.

It does not authorize `T_joint` computation, endpoint scoring,
cosmological validation, or physical validation.

If authorized, the output must keep KiDS endpoint-score-not-validation
and DESI small-N caveats attached.

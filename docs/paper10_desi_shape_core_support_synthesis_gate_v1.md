# Paper10 DESI shape-core support synthesis gate v1

**Doc class:** source-side synthesis gate
**Reader role:** reviewer / reproducibility auditor
**Status:** synthesis only; not replay authorization; not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This gate combines the already frozen DESI shape-route robustness
stress, row-sensitivity audit, core source-support scan, Row2
source-side reviews, and the isolated Row2 permission replay.
It does not run new endpoint scoring and does not authorize new replay.

Component status:

- `ROUTE_WIDE_REPLAY`: `positive_but_narrow_margin_and_row_sensitive_not_validation` -- candidate ranks first under the frozen shape score, but the margin is narrow
- `ROW_SENSITIVITY`: `row_sensitivity_explained_as_middle_shape_row_core_but_source_caveated_not_validation` -- middle shape rows 1 and 2 are the core-sensitive rows; row 1 is most required
- `CORE_SOURCE_SUPPORT_SCAN`: `p0_row2_has_existing_independent_in_interval_CC_support_not_endpoint_ready` -- frozen CC table supplies independent in-interval support for the row-2 core target
- `ROW1_CONFIRMATORY_SOURCE_ATTACHMENT`: `row1_confirmatory_source_review_accepted_not_endpoint_ready` -- external review accepts Borghi2022 and Stern2010 as Row1 confirmatory support
- `ROW2_CAVEAT_REDUCTION`: `ROW2_PERMISSION_ONLY_REPLAY_AUTHORIZED_NOT_VALIDATION` -- Moresco2012 and source-native DESI shape context reduce the row-2 caveat without promotion
- `ROW2_ONLY_PERMISSION_REPLAY`: `row2_permission_replay_candidate_not_control_resistant_not_validation` -- isolated Row2 replay is not control-resistant, so the route signal is not Row2-only

Synthesis:

- status: `DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_BUILT_SOURCE_STRENGTHENED_NOT_VALIDATION`
- core rows: `1;2`
- route interpretation: `multi_row_narrow_margin_source_sensitive_signal_not_row2_only`
- row 1 status: `most_required_confirmatory_independent_support_review_accepted_not_endpoint_ready`
- row 2 status: `caveat_reduced_but_permission_replay_not_control_resistant_not_promotion_ready`
- validation status: `not_endpoint_validation_not_physical_validation_not_falsification`
- recommended next action: `seek_route_level_source_synthesis_review_before_any_validation_claim`

Claim boundary:

```text
paper10_desi_shape_core_support_synthesis_gate_not_validation
```

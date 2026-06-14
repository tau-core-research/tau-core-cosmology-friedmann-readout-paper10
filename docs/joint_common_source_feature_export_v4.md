# Joint common source feature export v4

**Doc class:** residual-blind common source-feature export.
**Status:** KiDS candidate row features added; KiDS controls remain summary-only; still not scoring; not validation.
**Claim boundary:** `joint_common_source_feature_export_v4_not_scoring_not_validation`.

Version 4 keeps the v3 observer/DESI content and adds a KiDS COSEBIs
source-native feature export. The KiDS candidate side is represented by
the already source-frozen 300-row theory/mapping shell, while the
available KiDS null controls are represented only by residual-blind
vector-summary statistics.

This closes the pure missing-feature marker for KiDS, but it does not
close the penalty/scoring gate: row-level KiDS control vectors are still
not exported in a candidate/control-symmetric row basis. Therefore v4
is an audit-strengthening export, not an endpoint replay authorization.

Verdict: `COMMON_EXPORT_V4_KIDS_CANDIDATE_FEATURES_ADDED_CONTROLS_SUMMARY_ONLY_STILL_BLOCKS_PENALTY`.

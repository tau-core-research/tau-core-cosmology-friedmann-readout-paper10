# Joint common source feature export v2

**Doc class:** residual-blind common source-feature export.
**Status:** observer features added; still not scoring; not validation.
**Claim boundary:** `joint_common_source_feature_export_v2_not_scoring_not_validation`.

Version 2 promotes the already frozen R5 observer-path source vectors
into the common feature schema. These vectors are residual-blind and
candidate/control symmetric, but remain caveated because the R6 leakage
review is not complete.

DESI shape/time remains complete in the common schema. KiDS remains an
explicit missing-feature marker. Therefore the common export is stronger
than v1 but still does not authorize any penalty or `T_joint` rescoring.

Verdict: `COMMON_EXPORT_V2_OBSERVER_FEATURES_ADDED_KIDS_AND_R6_STILL_BLOCK`.

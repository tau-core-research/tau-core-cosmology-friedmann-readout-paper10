# Joint common source feature export v1

**Doc class:** residual-blind common source-feature export.
**Status:** common schema built; incomplete feature export; not scoring; not validation.
**Claim boundary:** `joint_common_source_feature_export_not_scoring_not_validation`.

This artifact exports source-side information under one common schema
for the active joint channels. It is candidate/control symmetric at
the schema level and uses only frozen source artifacts.

The DESI shape/time route exports a source-native shape vector for
candidate and controls. The observer-path route currently exports
only frozen source-scope membership and an explicit missing marker for
a row-level observer feature vector. KiDS has not yet been promoted
into this common feature layer.

Verdict: `COMMON_SCHEMA_BUILT_FEATURE_EXPORT_INCOMPLETE_NO_RESCORING`.

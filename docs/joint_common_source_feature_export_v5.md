# Joint common source feature export v5

**Doc class:** residual-blind common source-feature export.
**Status:** KiDS row-level null-control input artifact available; still not scoring; not validation.
**Claim boundary:** `joint_common_source_feature_export_v5_not_scoring_not_validation`.

Version 5 keeps the v4 observer/DESI/KiDS candidate export and adds
a compressed KiDS row-level null-control artifact reference. The
artifact expands 1008 predeclared controls into the same 300-row
COSEBIs basis used by the candidate source-frozen theory vector.

This closes the source-feature availability blocker for future
row-level penalty design, but it does not run or authorize that penalty.
Endpoint replay, validation, and `T_joint` rescoring remain forbidden.

Verdict: `COMMON_EXPORT_V5_SOURCE_FEATURE_INPUTS_COMPLETE_RESCORING_STILL_FORBIDDEN`.

# Joint numeric T_joint row-level penalty source availability v1

**Doc class:** source-side availability audit.
**Status:** no row-level penalty; not scoring; not validation.
**Claim boundary:** `joint_numeric_t_joint_row_level_penalty_source_availability_not_scoring_not_validation`.

This audit asks whether the observer-path and DESI shape/time routes
currently expose enough frozen, residual-blind source-side structure
to define a nontrivial row-level channel-distinguishability penalty.

Result: the observer-path route has a frozen source row scope and the
DESI route has a local shape vector, but the two routes do not expose
a common row-indexed feature space. Candidate/control-symmetric
per-row feature export is incomplete. A cross-channel row-level penalty
would therefore be artificial at this stage.

Verdict: `ROW_LEVEL_SOURCE_FEATURES_INCOMPLETE_NO_PENALTY`.

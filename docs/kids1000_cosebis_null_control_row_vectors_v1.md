# KiDS-1000 COSEBIs null-control row vectors v1

**Doc class:** source-frozen row-level control-vector expansion.
**Status:** not scoring; not endpoint validation.
**Claim boundary:** `kids1000_cosebis_null_control_row_vectors_not_scoring_not_validation`.

This artifact expands the already frozen KiDS null-control theory
replay into the same 300-row COSEBIs basis used by the candidate
source-frozen theory vector. It uses only the source-frozen theory
vector and the predeclared null-control seed inventory.

It does not use KiDS data-vector values, posterior chains, residuals,
fit statistics, post-hoc control selection, or endpoint scores.

The row-vector table is stored as a gzip-compressed CSV because the
uncompressed 302400-row table exceeds normal repository artifact
comfort limits. The build script deterministically regenerates it.

Rows: `302400`.
Verdict: `KIDS1000_COSEBIS_NULL_CONTROL_ROW_VECTORS_BUILT_NOT_SCORED`.

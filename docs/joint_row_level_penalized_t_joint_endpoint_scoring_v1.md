# Joint row-level penalized T_joint endpoint scoring v1

**Doc class:** guarded endpoint-scoring ledger.
**Status:** complete; not validation.
**Claim boundary:** `joint_row_level_penalized_t_joint_endpoint_scoring_not_validation`.

The replay uses the completed consolidated authorization response.
It scores only the six deterministically aligned row-level controls,
because those are the controls with frozen `P_row` values.

Candidate penalized statistic: `4.212744622365e+00`.
Controls beating/equal candidate: `0/6`.
Best aligned control: `matched_index_002` with penalized margin
`3.635632898848e+00`.

This is guarded endpoint scoring / preflight evidence only. It is
not endpoint validation, cosmological validation, or physical validation.

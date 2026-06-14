# Joint numeric T_joint control suite v1

**Doc class:** numeric same-statistic control-suite ledger
**Status:** prevalidation; not endpoint scoring; not validation
**Claim boundary:** `joint_numeric_t_joint_control_suite_prevalidation_not_endpoint_scoring`

Candidate `T_joint`: `4.142466300799e+00`.
Numeric controls: `26`.
Controls beating/equal candidate: `0`.
Control families: `block_drop:7;matched_control_index_aligned:6;null_readout:1;scope_and_forbidden_input_guard:1;shuffled_channel_labels:5;sign_flip:7`.
Verdict: `NUMERIC_T_JOINT_CONTROL_SUITE_BUILT_PREVALIDATION_NOT_ENDPOINT_SCORING`.

Every numeric control uses the same frozen formula
`T_joint = sum_i q_i z_i`, the same `q_i` weights, and the
same source-frozen channel standardization ledger. This artifact
does not authorize endpoint scoring or validation claims.

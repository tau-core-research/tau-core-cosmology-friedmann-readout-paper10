# Joint row-level penalty protocol shell v4

**Doc class:** protocol shell.
**Status:** symbolic row-level penalty ready; numeric computation authorization open; not scoring; not validation.
**Claim boundary:** `joint_row_level_penalty_protocol_shell_v4_not_scoring_not_validation`.

This shell supersedes v3 by closing the symbolic formula gate through
the non-scoring symbolic formula shell. It still does not compute
numeric penalty values, choose `lambda_row`, authorize endpoint
replay, or permit `T_joint` rescoring.

Frozen symbolic score shell:

`T_joint_penalized(a)=T_joint(a)+lambda_row*P_row(a)`

Open gate:

- numeric penalty computation and `lambda_row` authorization, in a
  separate review package.

Verdict: `SYMBOLIC_ROW_LEVEL_PENALTY_READY_NUMERIC_AUTHORIZATION_STILL_OPEN`.
Next action: `prepare_numeric_penalty_computation_authorization_review_package_before_any_values_or_rescoring`.

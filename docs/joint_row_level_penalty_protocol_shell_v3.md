# Joint row-level penalty protocol shell v3

**Doc class:** protocol shell.
**Status:** inputs and block-weight binding ready; symbolic penalty formula still open; not scoring; not validation.
**Claim boundary:** `joint_row_level_penalty_protocol_shell_v3_not_scoring_not_validation`.

This shell supersedes v2 by closing the covariance/block-weight
binding requirement through the non-scoring block-weight binding
shell.  It still does not define a penalty formula, compute a
penalty, authorize endpoint replay, or permit `T_joint` rescoring.

Closed gates:

- source-feature inputs;
- channel-local source-only normalization;
- candidate/control symmetric normalized transform;
- covariance/block-weight binding shell.

Open gate:

- symbolic row-level penalty formula, in a separate non-scoring
  review gate.

Verdict: `ROW_LEVEL_PENALTY_INPUTS_AND_BINDING_READY_SYMBOLIC_FORMULA_STILL_OPEN`.
Next action: `define_symbolic_row_level_penalty_formula_in_separate_non_scoring_gate`.

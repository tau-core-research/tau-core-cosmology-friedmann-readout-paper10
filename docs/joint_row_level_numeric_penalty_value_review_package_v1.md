# Joint row-level numeric penalty value review package v1

**Doc class:** external value-audit handoff.
**Status:** numeric penalty values only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.
**Claim boundary:** `joint_row_level_numeric_penalty_value_review_not_rescoring_not_validation`.

This package asks a reviewer to audit the already computed numeric
row-level penalty values. It does not ask for permission to use a
numeric `lambda_row`, modify `T_joint`, replay an endpoint, or make a
validation claim.

Current value summary:

- feature rows read: `303986`
- channel penalty rows: `1042`
- candidate channel penalty rows: `3`
- control channel penalty rows: `1039`
- complete joint penalty rows: `1`
- candidate `P_row`: `0.0702783215662`

Review focus:

1. Reproduce the values from the included scripts and artifacts.
2. Confirm that controls remain channel-local in this package.
3. Confirm that no endpoint residuals, endpoint scores, or fit
   statistics enter the value computation.
4. Confirm that all rescoring and validation flags remain false.

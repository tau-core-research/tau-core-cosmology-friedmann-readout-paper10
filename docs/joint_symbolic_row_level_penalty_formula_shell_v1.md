# Joint symbolic row-level penalty formula shell v1

**Doc class:** symbolic formula shell.
**Status:** formula defined symbolically; no numeric penalty; not scoring; not validation.
**Claim boundary:** `joint_symbolic_row_level_penalty_formula_shell_not_scoring_not_validation`.

This artifact freezes only the symbolic shape of a possible future
row-level source-feature penalty. It does not read endpoint residuals,
does not compute penalty values, does not choose a numeric
`lambda_row`, and does not modify `T_joint`.

For candidate or control alternative \(a\), channel \(i\), row
\(r\), and source feature \(f\), let \(z_{i,a,r,f}\) denote the
already frozen normalized source feature.  The frozen symbolic shell is:

\[
  P_i(a) = \omega_i\,\mathrm{mean}_{r,f}\, z_{i,a,r,f}^2,
\]

\[
  P_{\rm row}(a) = \sum_i P_i(a),
\]

with the already frozen equal-channel preweight shell \(\omega_i=1/3\)
for the three active channels.  A possible future score shell would be

\[
  T_{\rm joint}^{\rm penalized}(a)
  = T_{\rm joint}(a) + \lambda_{\rm row} P_{\rm row}(a),
\]

but \(\lambda_{\rm row}\) is symbolic only here. No numeric value is
chosen, fitted, inferred, or applied.

The formula is candidate/control symmetric: every candidate and every
matched control must use the same normalized transform, same block
weights, same covariance/caveat discipline, and same formula.

Verdict: `SYMBOLIC_ROW_LEVEL_PENALTY_FORMULA_FROZEN_NOT_COMPUTED_NOT_SCORING`.
Next action: `prepare_numeric_penalty_computation_authorization_review_package_before_any_values_or_rescoring`.

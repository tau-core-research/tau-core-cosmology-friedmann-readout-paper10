# Joint matched control-suite implementation scaffold v1

**Doc class:** implementation scaffold
**Status:** not run; not scoring; not endpoint validation
**Claim boundary:** `joint_matched_control_suite_implementation_scaffold_not_scoring_not_validation`

This scaffold turns the frozen matched-control requirements into a
future implementation checklist. It declares future builder names,
validators, output artifacts, required freeze inputs, and minimum
control-count rules. It does not create control vectors, residuals,
likelihoods, fit statistics, or endpoint scores.

The two binding rows remain hard-blocked:

- single-statistic binding: no final joint statistic is defined yet;
- covariance binding: no reviewed cross-probe covariance or reviewed
  block-diagonal independence response is available yet.

Summary:

- control families: `8`
- planned but not implemented: `6`
- blocked by upstream gate: `2`
- implementation ready: `false`
- endpoint scoring allowed: `false`
- verdict: `JOINT_MATCHED_CONTROL_SUITE_IMPLEMENTATION_SCAFFOLD_FROZEN_NOT_RUN`

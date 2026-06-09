# KiDS-1000 COSEBIs Operator Leakage Theorem Requirements v1

This gate converts the mask-mode leakage audit into a frozen requirement list
for a future survey-native operator theorem.

The current verdict is:

```text
requirements_frozen_for_operator_leakage_theorem_but_proof_remains_open
```

The gate uses no KiDS COSEBIs data-vector values, residuals, fit statistics,
posterior chains, or endpoint scores. It depends only on the already frozen
source-side operator, spectrum, null-safety, pure-mask, and mask-mode leakage
artifacts.

The result is intentionally not a proof. It records:

- the uniform tile-average limit, where centered pure-mask directions collapse
  to zero;
- the non-uniform leakage risk, where a future operator could couple mask-only
  amplitudes to the low-mode envelope;
- the requirement that an admissible operator must reject pure-mask directions
  in quotient space or route them to an explicit null-control family;
- the requirement that the mode spectrum and the null descent be generated or
  rejected by one source-native operator;
- the remaining open blockers: operator leakage theorem and gauge/quotient
  descent.

Claim boundary:

```text
kids1000_cosebis_operator_leakage_theorem_requirements_not_validation
```

# KiDS-1000 COSEBIs Mask-Mode Leakage Audit v1

This audit checks a narrow source-side leakage risk: whether the pure-mask
perturbation basis can be safely separated from the low-mode COSEBIs carrier
without a survey-native operator theorem.

The current verdict is:

```text
uniform_mask_collapse_is_null_but_nonuniform_operator_leakage_remains_open
```

The audit uses no KiDS COSEBIs data-vector values, residuals, fit statistics,
posterior chains, or endpoint scores. It combines:

- the centered, unit-RMS pure-mask basis from the pure-mask response gate;
- the four frozen mode-response spectrum families from the spectrum-attempt
  gate.

The result is intentionally mixed:

- under uniform tile averaging, the centered pure-mask basis collapses to zero;
- under a hypothetical non-uniform operator, a mask-only direction could still
  couple to a low-mode envelope.

Therefore the source-side leakage risk is now explicit, but the operator-level
leakage theorem remains open.

Claim boundary:

```text
kids1000_cosebis_mask_mode_leakage_audit_not_validation
```

# KiDS-1000 COSEBIs Pure-Mask Response Gate v1

This gate narrows the pure-mask branch of the operator null-safety blocker. It
uses only source-frozen full-route mask observables and does not read KiDS
COSEBIs data-vector values, residuals, posterior chains, or endpoint scores.

The current verdict is:

```text
pure_mask_basis_exists_but_quotient_triviality_and_mode_coupling_remain_blocked
```

The gate constructs a centered, unit-RMS, source-only pure-mask perturbation
basis from two full-route mask observables:

- `F_overlap`, the finite nonzero pixel fraction normalized by the maximum
  tile fraction;
- `D_path`, the finite nonzero mask-load mean normalized by the maximum tile
  mean.

The two centered directions are non-degenerate, and the basis is lifted to the
`58,800` row target-by-route-tile domain. This makes future pure-mask null
replay concrete.

The gate does not construct a mapping vector, does not construct a theory
vector, and does not score. Two blockers remain explicit:

- pure-mask perturbations have not been proven quotient-trivial under the
  survey-native operator;
- the mode-response coupling has not been shown to suppress mask-only leakage
  into the low-mode envelope.

Claim boundary:

```text
kids1000_cosebis_pure_mask_response_gate_not_validation
```

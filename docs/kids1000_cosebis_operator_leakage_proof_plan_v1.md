# KiDS-1000 COSEBIs Operator Leakage Proof Plan v1

Document class: proof-plan ledger.

Status: `OPERATOR_LEAKAGE_PROOF_PLAN_BUILT_NOT_PROOF`.

This ledger freezes the exit conditions for the next primary physical-promotion
gate, `B2_operator_leakage_theorem_open`. It computes no new score, uses no
KiDS endpoint data-vector values, and does not claim endpoint validation or
physical validation.

## What Is Already Available

- Uniform tile-average null anchor:
  `uniform_collapse_all_null=true`.
- Endpoint-feedback guard:
  no KiDS data-vector values, residuals, fit statistics, posterior chains, or
  endpoint scores enter this proof-plan ledger.

## What Remains Open

The leakage theorem itself is still open. Three proof steps remain:

1. Non-uniform leakage projection:
   prove or reject an operator projection that sends non-uniform mask-only
   directions to a null or controlled subspace.

2. Pure-mask quotient/control:
   prove that the pure-mask basis is quotient-trivial, or route it into a
   predeclared null-control family before any positive Tau response claim.

3. Single-operator coupling:
   derive or reject one source-native operator that generates both the mode
   response and the null descent. Separate spectrum and null artifacts are not
   enough for physical promotion.

## Exit Condition

`nonuniform_mask_response_cannot_masquerade_as_positive_low_mode_tau_path_signal`

In plain language: before the KiDS COSEBIs diagnostic signal can be promoted
physically, we must prove that mask/leakage structure cannot imitate the same
low-mode response that the candidate kernel currently captures.

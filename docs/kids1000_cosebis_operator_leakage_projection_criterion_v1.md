# KiDS-1000 COSEBIs Operator Leakage Projection Criterion v1

Document class: theorem-criterion ledger.

Status: `OPERATOR_LEAKAGE_PROJECTION_CRITERION_BUILT_NOT_PROVEN`.

This ledger freezes the sufficient projection criterion for the first open
operator-leakage proof step, `P2_nonuniform_leakage_projection`. It computes no
new score, uses no endpoint data-vector values, and does not claim endpoint or
physical validation.

## Sufficient Criterion

Let the source-side operator domain be decomposed as:

```text
V_source = V_phys_candidate + V_mask + V_control_or_null
```

A future operator `O` passes the non-uniform leakage projection criterion if it
satisfies either:

```text
Pi_phys O m = 0
```

for every mask-only direction `m in V_mask`, modulo quotient-null directions,
or:

```text
O(V_mask) subset V_control
```

where `V_control` is scored only as a predeclared null-control family.

The same operator must also generate the mode-response spectrum and satisfy the
null/control condition; separate spectrum and null artifacts are not enough.

## Current Status

- Criterion frozen: yes.
- Domain decomposition declared: no.
- Null projection condition proven: no.
- Control routing condition proven: no.
- Single-operator consistency proven: no.
- P2 closed: no.

## Verdict

`nonuniform_leakage_projection_criterion_frozen_but_not_proven`

In plain language: we have now stated exactly what would be enough to prevent
non-uniform mask leakage from masquerading as the low-mode Tau response, but we
have not yet proven that the KiDS operator satisfies it.

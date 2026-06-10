# KiDS-1000 COSEBIs Operator-Leakage Domain Decomposition v1

**Doc class:** theorem-support ledger  
**Reader role:** proof-gate reviewer  
**Status:** `OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_DECLARED_NOT_PROJECTION_PROOF`  
**Canonical parent:** `README.md`

This ledger closes only the bookkeeping part of the nonuniform leakage
criterion. It declares the source-domain components used by the future
operator-leakage theorem target:

```text
V_source = V_phys_candidate + V_mask + V_control_or_null.
```

It does not prove pairwise orthogonality, quotient triviality, control routing,
single-operator consistency, or physical promotion.

## Components

`V_phys_candidate` is the source-frozen low-mode candidate response shell built
from the mapping and theory-vector artifacts. It is not a validated physical
signal.

`V_mask` is the pure-mask/depth/path basis built from the mask response gate.
Its basis exists, but its quotient triviality and operator coupling remain open.

`V_control_or_null` is the predeclared null-control family. It is a possible
routing target for mask-only response, not a positive Tau signal.

## Claim Boundary

Allowed:

```text
domain_decomposition_declared = true
```

Forbidden:

```text
components_pairwise_orthogonality_proven = true
operator_projection_condition_proven = true
operator_leakage_theorem_proven = true
validation_ready = true
```

## Verdict

`domain_decomposition_declared_but_projection_and_leakage_theorem_remain_open`.

The next open proof obligations remain the null-projection/control-routing
condition and the single-operator consistency condition.

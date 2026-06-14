# KiDS/COSEBIs operator-leakage closure attempt v1

**Doc class:** proof-blocker narrowing artifact
**Status:** theorem not proven; no endpoint scoring; no validation claim
**Claim boundary:** `kids1000_cosebis_operator_leakage_closure_attempt_not_validation`

This note narrows the first KiDS/COSEBIs physical-promotion blocker:
`B2_operator_leakage_theorem_open`.  It does not close the blocker.
Its role is to state the exact source-side conditions under which
nonuniform mask leakage cannot be promoted into a quotient-visible
Tau path/readout signal.

Minimal target theorem:

```text
For every admissible mask-only direction m in the source mask domain,
either P_phys O_tau(m) = 0 in the quotient, or O_tau(m) is routed
to the frozen null-control family under the same statistic and
covariance discipline.  The same operator must reduce to the
uniform-tile pure-mask null limit and descend through gauge/quotient
representations.
```

Current status:

- uniform limit available: `true`
- domain decomposition declared: `true`
- null-control draws available: `1008`
- mask quotient triviality proven: `false`
- null projection condition proven: `false`
- control routing condition proven: `false`
- single-operator consistency proven: `false`
- gauge quotient descent proven: `false`
- verdict: `OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN`

Interpretation: the KiDS low-tail block remains useful as a caveated
diagnostic signal, but the operator-level theorem is still open.  The
next proof work must close mask quotient triviality or same-statistic
control routing, and then prove gauge/quotient descent for the same
source-native operator.

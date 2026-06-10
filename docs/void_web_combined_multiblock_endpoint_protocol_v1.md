# Void/Web Combined Multiblock Endpoint Protocol v1

**Doc class:** frozen scoring-protocol shell  
**Reader role:** Paper 10 reproducibility / future endpoint design  
**Status:** frozen, not run, not validation  
**Canonical parent:** README.md

This protocol is the next gate after the FLRW-audited void/web readiness
ledger. It does not compute scores. It freezes the grammar that a future
combined void/web endpoint must obey before any promotion from isolated pilots
to a joint endpoint test.

## Included Blocks

- Pantheon distance, using the retained full-covariance block.
- SDSS final growth summary, as a diagonal-summary block unless upgraded.
- SDSS DR16 multi-tracer BAO/RSD, using the official 6x6 covariance.
- CMB low-redshift safety support, as a constraint/check rather than a CMB
  likelihood.

The active channel families are `W_VOID_MATURITY` and `W_WEB_ANISOTROPY`.
`W_PATH_PROJECTION` and `W_TIME_READOUT` remain disabled for this protocol.

## Unified Criterion

The future score must be a shared multi-block comparison, not a per-block
rescue. The frozen shell is:

```text
AIC_total = chi2_distance + chi2_growth + chi2_multitracer + 2*k_shared
```

`k_shared` must count shared source-frozen void/web channel amplitudes and
declared baseline parameters. A BIC robustness line may be added only after an
effective sample-size convention is declared.

## Required Controls

The future endpoint must include baseline-only, source-native void/web,
void-only, web-only, wrong-sign, wrong-threshold, deterministic shuffled, and
block-drop controls. CMB-safety support must also be preserved.

## Claim Boundary

This is not scoring and not validation. It is a leakage-prevention and
endpoint-design artifact. The void/web branch remains unvalidated until a
future run implements this protocol and survives the declared controls.

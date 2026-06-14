# KiDS/COSEBIs response-unit normalization closure attempt v1

**Doc class:** proof-blocker narrowing artifact
**Status:** unit map not derived; no endpoint scoring; no validation claim
**Claim boundary:** `kids1000_cosebis_response_unit_normalization_closure_attempt_not_validation`

This note narrows the third KiDS/COSEBIs physical-promotion blocker:
`B4_response_unit_normalization_open`. It does not derive the missing
response-unit map.

Minimal target theorem:

```text
A source-side or theorem-side map U_tau must convert the dimensionless
source kernel A_src K_i into the retained COSEBIs response codomain,
without using endpoint residuals, fit statistics, posterior feedback,
or the covariance metric as a unit derivation. The same U_tau must
preserve the standard-lensing/no-Tau-source null limit and must attach
only to an operator class that has passed leakage and gauge/quotient
descent.
```

Current status:

- COSEBIs row domain available: `true`
- dimensionless kernel/source amplitude available: `true`
- covariance metric available: `true`
- covariance metric used as units derivation: `false`
- response-unit normalization derived: `false`
- physical operator units derived: `false`
- standard-lensing null compatibility proven: `false`
- leakage theorem proven: `false`
- gauge quotient descent proven: `false`
- verdict: `RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_UNITS_REMAIN_OPEN`

Interpretation: Paper 10 has a reproducible response domain and a
dimensionless source-side kernel, but not yet a physical COSEBIs
response-unit theorem. The KiDS block therefore remains caveated.

# KiDS-1000 COSEBIs Low-Mode Carrier Source Grounding v1

This ledger addresses the next question raised by the mode-localization and
mode-shape stress audits:

```text
Why is a low-mode COSEBIs carrier allowed as a source-frozen path/readout
protocol object?
```

The answer is only partial. The current carrier

```text
M_mode(n) = n^(-1/2) / mean_{n=1..20}(n^(-1/2))
```

is source independent, predeclared, unit-mean normalized, and not selected from
the KiDS data vector. It is consistent with a path/readout expectation that a
projection residual should be broad and coherent in the COSEBIs mode hierarchy
rather than concentrated only in high-frequency modes. It is also supported by
post-score diagnostics: the endpoint signal is low-mode localized, flat mode
weighting still improves, and high-mode weighting removes the signal.

However, those diagnostics do not derive the exponent. The exponent remains a
source-frozen protocol carrier, not a first-principles Tau Core lensing/path
kernel theorem.

Current verdict:

```text
partial_protocol_grounding_with_open_first_principles_derivation_blocker
```

Required future work:

- derive a covariant or survey-native path/readout mode kernel;
- test external covariance, scale cuts, and mocks;
- keep validation language disabled until those tests pass.

Claim boundary:

```text
kids1000_cosebis_low_mode_carrier_source_grounding_partial_not_validation
```

# KiDS-1000 COSEBIs Mode-Response Operator Spec v1

This artifact freezes the requirements for a future survey-native
mode-response operator. It does not derive the operator and it does not score
KiDS.

The purpose is to prevent post-hoc mode-shape promotion. Before the conditional
`n^-1/2` envelope can be treated as more than a protocol carrier, a
survey-native operator must map source-side path observables into the retained
COSEBIs row/mode domain.

Current verdict:

```text
operator_requirements_frozen_but_survey_native_mode_response_not_derived
```

The spec records eight requirements:

- source-side path-observable domain;
- retained 300-row COSEBIs codomain;
- linearity before endpoint amplitude;
- mode response derived from the source operator;
- pair/redshift/path separation;
- no data-vector or fit feedback;
- gauge/mask null safety;
- standard-lensing null limit.

Two blockers remain explicit: the mode-response spectrum is not yet derived
from source-side path fields, and operator-level gauge/null safety has not yet
been proven.

Claim boundary:

```text
kids1000_cosebis_mode_response_operator_spec_not_validation
```

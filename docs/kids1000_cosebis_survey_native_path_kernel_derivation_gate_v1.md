# KiDS-1000 COSEBIs Survey-Native Path-Kernel Derivation Gate v1

This gate audits how far the current KiDS COSEBIs route has moved from a
conditional low-mode envelope toward a survey-native path/readout kernel.

It is not a validation claim and it does not close the Tau Core lensing
derivation. Its purpose is to separate:

- available source-side route support;
- caveated path-observable support;
- missing mode-response and covariant/survey-native kernel derivation.

Current verdict:

```text
survey_native_path_route_available_but_mode_response_and_covariant_kernel_derivation_blocked
```

The first five route-support conditions pass or pass caveated: the source-frozen
mapping basis exists, a full-route mask-load path proxy is available but
caveated, the path-weight factorization is source-side computable, the
source-frozen theory-vector shell exists, and the deterministic mock-sanity
guardrail passes.

Three blockers remain open:

1. a survey-native operator from path observables to COSEBIs mode response;
2. a derivation of the log-band prior from that response spectrum;
3. a covariant or survey-native lensing/path limit with explicit gauge and unit
   descent.

Claim boundary:

```text
kids1000_cosebis_survey_native_path_kernel_derivation_gate_not_validation
```

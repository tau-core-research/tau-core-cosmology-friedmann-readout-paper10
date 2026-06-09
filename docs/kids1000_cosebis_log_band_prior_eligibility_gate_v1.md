# KiDS-1000 COSEBIs Log-Band Prior Eligibility Gate v1

This gate records when the conditional low-mode envelope derivation is allowed
to be used as a source-side protocol object.

The gate does not score KiDS data and does not claim validation. It separates
three things:

- source-side conditions already satisfied by the current COSEBIs route;
- the smooth/coherent path-readout assumption that remains unproven;
- the future covariant or survey-native path-kernel derivation blocker.

Current verdict:

```text
protocol_eligible_for_conditional_envelope_but_not_full_kernel_validated
```

Meaning:

The retained COSEBIs mode hierarchy is ordered and dimensionless, all modes
`1..20` are kept, the source-side path mapping shell exists, and the parent
derivation is compatible with a broad coherent path/readout residual rather
than a high-frequency-only source. Therefore the `n^-1/2` envelope is eligible
as a conditional protocol carrier.

But the physical smoothness prior is not yet source-proven, and the full
covariant/survey-native Tau Core lensing/path kernel remains open.

Claim boundary:

```text
kids1000_cosebis_log_band_prior_eligibility_gate_not_validation
```

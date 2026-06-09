# KiDS-1000 COSEBIs Physical Amplitude Requirements Gate v1

This gate separates the internal source-normalized amplitude map from a future
physical COSEBIs response amplitude.

The current verdict is:

```text
dimensionless_source_amplitude_available_but_physical_response_amplitude_remains_open
```

The previous source-side amplitude artifact froze only:

```text
A_src = 1
```

as a dimensionless unit-mean source normalization. This gate records that this
is not yet a physical COSEBIs response amplitude. A future physical amplitude
must still provide:

- the response-unit normalization mapping the dimensionless source kernel into
  the retained COSEBIs statistic;
- the standard-lensing/no-Tau-source null amplitude limit;
- a derivation that does not use endpoint residuals, fit statistics, posterior
  chains, random noise, or KiDS data-vector values.

The covariance metric remains useful for later scoring, but it is not an
amplitude derivation.

Claim boundary:

```text
kids1000_cosebis_physical_amplitude_requirements_gate_not_validation
```

# KiDS-1000 COSEBIs Response-Unit Normalization Requirements Gate v1

This gate freezes the requirements for turning the current dimensionless
source-side kernel into a physical COSEBIs response object.

The current verdict is:

```text
cosebis_response_unit_requirements_frozen_but_normalization_remains_open
```

The gate does not derive the response-unit normalization. It records that:

- the retained COSEBIs row domain is available;
- the source-side kernel and source amplitude remain dimensionless;
- the covariance metric is available for later scoring but is not a unit
  derivation;
- the actual response-unit map remains open;
- compatibility with the standard-lensing/no-Tau-source null limit remains
  open;
- no KiDS data-vector values, residuals, fit statistics, posterior chains,
  random noise, or endpoint scores are used.

Claim boundary:

```text
kids1000_cosebis_response_unit_normalization_requirements_gate_not_validation
```

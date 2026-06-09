# KiDS-1000 COSEBIs Physical Operator Units Gate v1

This gate records the unit and normalization requirements that remain after the
first source-side operator skeleton has been constructed.

The current verdict is:

```text
dimensionless_operator_kernel_identified_but_physical_units_and_amplitude_remain_open
```

The current skeleton is a dimensionless unit-amplitude kernel. It is useful for
operator audits, but it is not yet a physical COSEBIs prediction. A future
operator theorem must still derive:

- the physical response units and normalization;
- a source-side amplitude map without endpoint residual or fit feedback;
- the standard-lensing/no-Tau-source null normalization.

The gate uses no KiDS COSEBIs data-vector values, residuals, fit statistics,
posterior chains, random noise, or endpoint scores.

Claim boundary:

```text
kids1000_cosebis_physical_operator_units_gate_not_validation
```

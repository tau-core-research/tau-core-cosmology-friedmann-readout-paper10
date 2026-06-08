# Pantheon+ Design Matrix V1

This is a dry-run design-matrix layer for the frozen Pantheon+ scope.

It does not run a likelihood, fit a model, compute residuals, or compare
baselines.

## Inputs

Parent artifacts:

- `PANTHEON_DISTANCE_SCOPE_V1`
- `PANTHEON_SCORING_PROTOCOL_V1`

Allowed input columns:

```text
CID
source_row_index
zHD
zCMB
MU_SH0ES
MU_SH0ES_ERR_DIAG
```

## Derived Columns

The design matrix includes only source-derived or family-basis columns:

```text
a_scale = 1 / (1 + zHD)
log1p_z
baseline_intercept_column
W_tau_basis_a_over_1pa
W_tau_basis_a2_over_1pa2
```

The two `W_tau` basis columns are not fitted parameters. They are fixed basis
columns included to verify that the later scoring script can consume a declared
activation-family grammar without changing row masks.

## Forbidden Columns

The design matrix may not contain:

```text
model_mu
distance_residuals
delta_mu
chi2
likelihood
fit_improvement_flags
Tau_residual_parameters
```

## Current Status

```text
DESIGN_MATRIX_FROZEN_NOT_SCORED
```

The next step, if approved separately, is a pilot scoring script that consumes
this matrix and reports results as pilot evidence only.

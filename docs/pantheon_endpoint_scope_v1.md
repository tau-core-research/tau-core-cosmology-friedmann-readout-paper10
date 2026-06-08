# Pantheon+ Endpoint-Eligible Pilot Scope V1

This note freezes the first Pantheon+ distance-side pilot scope.

It does not score any cosmological model.

## Parent Frozen Products

- `PANTHEON_PLUS_SH0ES_DAT`
- `PANTHEON_PLUS_SH0ES_STAT_SYS_COV`

## Row Rule

The frozen residual-blind row rule is:

```text
include if IS_CALIBRATOR == 0 and zHD >= 0.023
exclude if IS_CALIBRATOR == 1 or zHD < 0.023
```

Rationale:

- Cepheid calibrator rows are not used in this distance-shape pilot scope.
- The redshift cut is source-side and predeclared.
- The rule does not inspect Lambda-CDM residuals, Tau residuals, fit
  improvements, or late-time activation parameters.

## Observable Columns

The frozen observable columns are:

```text
CID
zHD
zCMB
MU_SH0ES
MU_SH0ES_ERR_DIAG
```

The STAT+SYS covariance matrix is available and dimension-checked against the
source table, but no likelihood or endpoint statistic is run in this step.

## Forbidden Inputs

The following fields remain forbidden during scope construction:

```text
distance_residuals
fit_improvement_flags
Tau_residual_parameters
late_time_activation_fit
```

## Derived Artifacts

The scope builder writes:

```text
data/derived/pantheon_scope_v1_row_mask.csv
data/derived/pantheon_scope_v1_summary.csv
```

These artifacts are allowed because they are source-derived row masks and
hashes, not model scores.

## Current Status

```text
SCOPE_FROZEN_NOT_SCORED
```

Endpoint scoring remains disabled. The next gate is a separate scoring protocol
that must predeclare baseline cosmology, nuisance handling, and any Tau
activation family before reading model residuals.

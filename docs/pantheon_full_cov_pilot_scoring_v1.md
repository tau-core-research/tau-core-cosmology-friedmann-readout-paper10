# Pantheon+ Full-Covariance Pilot Scoring V1

This is the first full-covariance numerical pilot score for Paper 10.

It is not validation.

## Inputs

The run consumes only frozen artifacts:

- `PANTHEON_DISTANCE_SCOPE_V1`
- `PANTHEON_SCORING_PROTOCOL_V1`
- `PANTHEON_DESIGN_MATRIX_V1`
- retained Pantheon+ STAT+SYS covariance submatrix
- the same branch grid used by `PANTHEON_PILOT_SCORING_V1`

## Covariance Policy

The retained STAT+SYS covariance submatrix is positive definite on the frozen
1371-row Pantheon+ scope. The run therefore uses Cholesky solves with no
eigenvalue floor or diagonal approximation.

The diagonal-covariance pilot remains a lower-level numerical smoke test. This
full-covariance run is a stronger pilot, but still not a cosmological
validation.

## Branches

The run evaluates four branches:

- baseline-only flat-Lambda-CDM distance modulus,
- Tau late-activation shell,
- wrong-activation control,
- deterministic shuffled-activation control.

The absolute magnitude / Hubble offset is analytically marginalized for every
grid point. No SALT2 nuisance refit is performed. No row mask is changed.

## Claim Boundary

```text
FULL_COV_PILOT_SCORING_NOT_VALIDATION
```

The result is a full-covariance pilot test of the frozen scoring grammar. It is
not a claim that Tau Core explains dark energy, not a replacement for
Lambda-CDM, and not a covariance-complete multi-probe cosmological analysis.

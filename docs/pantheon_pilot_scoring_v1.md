# Pantheon+ Pilot Scoring V1

This is the first numerical pilot score for Paper 10.

It is not validation.

## Inputs

The run consumes only frozen artifacts:

- `PANTHEON_DISTANCE_SCOPE_V1`
- `PANTHEON_SCORING_PROTOCOL_V1`
- `PANTHEON_DESIGN_MATRIX_V1`
- diagonal of the retained Pantheon+ STAT+SYS covariance submatrix

## Branches

The run evaluates four branches:

- baseline-only flat-Lambda-CDM distance modulus,
- Tau late-activation shell,
- wrong-activation control,
- deterministic shuffled-activation control.

## Fit/Nuisance Policy

The absolute magnitude / Hubble offset is analytically marginalized for every
grid point. No SALT2 nuisance refit is performed. No row mask is changed.

The retained STAT+SYS covariance product remains frozen and shape-validated,
but this first pilot score uses only its retained diagonal as a numerical smoke
test. A fixed diagonal variance floor, `rtol = 1e-8` relative to the median
positive retained variance, is applied for stability. A covariance-complete
likelihood is a later gate and is not claimed here.

## Claim Boundary

```text
PILOT_SCORING_NOT_VALIDATION
```

The result is a numerical smoke test of the frozen scoring grammar. It is not a
claim that Tau Core explains dark energy, not a replacement for Lambda-CDM, and
not a covariance-complete cosmological analysis.

# Pantheon+ Scoring Protocol V1

This document freezes the first Pantheon+ scoring grammar for Paper 10.

It does not run scoring.

## Parent Scope

```text
PANTHEON_DISTANCE_SCOPE_V1
```

The parent scope has:

- 1701 total source rows,
- 1371 retained rows,
- the Pantheon+ STAT+SYS covariance available,
- calibrators excluded,
- and `zHD >= 0.023`.

## Baseline Family

The frozen baseline family is:

```text
flat_LCDM_distance_modulus
```

The future baseline scoring protocol may allow `Omega_m` as a fit parameter,
with the absolute magnitude / H0 offset marginalized analytically. No Tau
parameters are allowed in the baseline branch.

## Tau Activation Family

The frozen Tau shell family is:

```text
W_tau(a) = a^q / (a^q + a_tau^q)
```

This document freezes the family only. It does not fit `q`, `a_tau`, or
`Omega_tau`.

## Required Future Controls

Any later scoring run must include:

- baseline-only branch,
- Tau-shell branch,
- shuffled-activation control,
- wrong-activation control,
- and no post-hoc row-mask changes.

## Forbidden Inputs

The scoring protocol was frozen without using:

```text
distance_residuals
fit_improvement_flags
Tau_residual_parameters
late_time_activation_fit
posthoc_row_masks
```

## Current Status

```text
SCORING_PROTOCOL_FROZEN_NOT_RUN
```

This is the last pre-scoring gate. The next step, if approved separately, is to
write a scoring script that consumes this protocol and produces a clearly marked
pilot result.

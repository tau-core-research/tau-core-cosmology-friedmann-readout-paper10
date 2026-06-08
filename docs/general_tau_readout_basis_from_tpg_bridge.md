# General Tau Core Readout Basis Abstracted from the TPG Bridge

This note records why the first Pantheon+ pilot should not be overread.

The point is not that Paper 10 is based on the TPG bridge. The point is that
the galaxy-scale TPG bridge made explicit a more general Tau Core readout
principle that can also be used in cosmology.

## Current Pilot

The current Paper 10 numerical pilot uses one homogeneous late-time shell:

```text
W_tau(a)
```

This is a useful stress test of the scoring ladder, but it is not the full Tau
Core morphology/projection-readout structure.

Result:

```text
full-cov Delta chi2_tau-baseline = -0.192
full-cov Delta AIC_tau-baseline  = +5.808
```

Interpretation:

```text
scoring pipeline works;
single-shell evidence is weak;
not a Tau Core true negative.
```

## General Readout Principle

The TPG bridge is a worked example of the more general Tau Core pattern:

```text
Tau-side morphology/projection state
    -> four-dimensional readout residual
    -> observable closure test
```

At galaxy scale, the closure test is a rotation/readout residual.

At cosmological scale, the closure test becomes:

```text
Friedmann-readout residual
    -> distance + growth + lensing + CMB-safety audit
```

So the common object is not TPG itself. The common object is the Tau Core
readout principle:

```text
four-dimensional observables may be channel-dependent readouts
of a deeper Tau-side configuration.
```

## Missing Channel Families

A cosmological implementation of this general principle should not rely on one
smooth activation shell. It needs independently frozen channel families:

```text
W_void(a)
    void maturity / late-time distance activation

W_web(a,k,env)
    cosmic-web anisotropy for growth and lensing

W_path(z,n_hat)
    observer/path projection along the null-geodesic bundle

W_time(a)
    time/readout projection of observed a(t), H(t)
```

The path channel means the metric and matter environment affecting the null
geodesic bundle by which light reaches the observer. It is not a claim about
objects outside the relevant causal past.

The time/readout channel means that observed four-dimensional clock variables
may be readout variables rather than fundamental Tau-side time coordinates. It
is not a backward-causation term.

## Multi-Channel Residual Shell

A future source-frozen shell should have the schematic form:

```text
C_tau,cosmo
    = C_void[W_void]
    + C_web[W_web]
    + C_path[W_path]
    + C_time[W_time]
    + C_cross
```

`C_cross` must remain controlled and source-frozen. It cannot be introduced
post hoc to rescue an endpoint score.

## Audit Rule

Each channel must be selected from independent source-side observables before
the corresponding target residual is scored.

This is why the present full-covariance Pantheon+ result is a limitation of the
homogeneous shell, not a decisive test of the broader Tau Core readout
framework.

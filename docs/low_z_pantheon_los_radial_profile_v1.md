# Low-z Pantheon LOS Radial Profile v1

**Doc class:** source-side path/environment observable.
**Status:** not scoring; not endpoint replay; not validation.
**Canonical parent:** full observer/path kernel source requirements.

## Purpose

The previous line-of-sight environment artifact used one fixed redshift window
and one fixed angular cone.  That scalar proxy is too compressed for a future
full observer/path kernel.  This artifact builds a residual-blind radial shell
profile from the same SDSS DR17 MCPM slime-mold galaxy catalogue.

## Frozen shell rule

For each frozen low-z Pantheon row, the script uses a fixed angular radius of
2 degrees and the following predeclared redshift shells relative to the source:

```text
foreground_far:  -0.03 <= dz < -0.01
foreground_near: -0.01 <= dz < -0.003
near_source:     -0.003 <= dz <  0.003
background_near:  0.003 <= dz <  0.01
background_far:   0.01 <= dz <  0.03
```

For each shell it records count, mean density, and median density.  It also
records two source-side contrasts:

```text
foreground_minus_background_density
near_minus_far_density
```

## Current coverage

```text
low-z rows:                         424
rows with any shell support:        246
rows with complete 5-shell profile: 153
partial path-scope rows:             12
partial path-scope with any support: 10
partial path-scope complete profiles: 7
```

## Interpretation

This is progress toward the R2 source requirement, because the line-of-sight
environment is no longer represented only by a single count/mean-density scalar.
It is still not a full path integral.  The profile has incomplete coverage and
does not yet include metric/lensing weights, directional web tensor contraction,
or a physically derived null-geodesic bundle weight.

## Claim boundary

Allowed:

```text
source-side LOS radial profile exists as a partial observable.
```

Forbidden:

```text
endpoint replay authorization
validation
physical lensing-path weight claim
full observer/path kernel claim
```

# SDSS Multi-Tracer BAO/RSD Transform Rule v1

The transform maps the official SDSS multi-tracer Fourier-space compressed
measurement into a source-native design matrix. The observable order is kept as
published:

```text
D_M/r_d, D_H/r_d, f sigma_8
```

for each of the two effective redshifts. A source-native SDSS DR17 MCPM
`W_web` basis is attached by nearest redshift-bin lookup. The web channel is
allowed to act only on the growth entries in the pilot model; distance entries
are retained to test the shared BAO/RSD covariance and to prevent reading the
growth block in isolation.

Disabled channels:

```text
W_void, W_path, W_time
```

Claim boundary: this is a covariance-aware pilot transform, not a validated
multi-probe likelihood.

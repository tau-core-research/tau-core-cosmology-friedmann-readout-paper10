# SDSS Multi-Tracer BAO/RSD Full-Covariance Pilot v1

This pilot is the first covariance-aware growth/BAO block. It uses the official
SDSS DR16 LRG+ELG Fourier-space six-component compressed vector and covariance:

```text
z=0.70:  D_M/r_d, D_H/r_d, f sigma_8
z=0.845: D_M/r_d, D_H/r_d, f sigma_8
```

The baseline branch is a flat-Lambda-CDM distance and growth-index shell with
parameters:

```text
Omega_m, sigma8_0, q_bao
```

where `q_bao = c/(H0 r_d)` is a nuisance distance-scale carrier. The web branch
adds one source-native growth-channel amplitude:

```text
f sigma8 -> f sigma8 * (1 + mu_web W_web(z)).
```

The BAO entries are not directly modified by `W_web` in this pilot. The purpose
is to test whether a web-growth readout survives when the official BAO/RSD
covariance is retained.

This is not endpoint validation. A validated multi-probe test would require a
predeclared likelihood grammar across distance, growth, lensing, and CMB-safety
blocks.

# KiDS-1000 COSEBIs Theory-Vector Policy v1

This declares the theory-vector gate for the KiDS-1000 COSEBIs lensing route.
The parent policy remains endpoint-disabled and declarative. A separate
source-frozen unit-amplitude shell now materializes the 300-row vector interface
without using endpoint data.

Frozen requirements:

```text
statistic:                 COSEBIs
target vector length:      300 rows
active future channels:    W_WEB_ANISOTROPY, W_PATH_PROJECTION
disabled channels:         W_VOID_MATURITY, W_TIME_READOUT
current theory vector:     source-frozen unit-amplitude shell computed
endpoint scoring:          disabled
```

The current source-frozen shell is built from the frozen web/path mapping basis
and a predeclared unit-mean `mode^{-1/2}` mode-shape rule. It has unit amplitude
only: no KiDS residual, posterior chain, best-fit cosmology choice,
fit-improvement flag, observed data-vector value, post-hoc mode cut, or post-hoc
amplitude calibration may choose its form.

This is a theory-readiness and leakage-prevention artifact. It is not an
endpoint prediction, not a likelihood run, and not empirical validation.

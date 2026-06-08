# KiDS-1000 COSEBIs Theory-Vector Policy v1

This declares the future theory-vector gate for the KiDS-1000 COSEBIs lensing
route. It deliberately does not compute a theory vector.

Frozen requirements:

```text
statistic:                 COSEBIs
target vector length:      300 rows
active future channels:    W_WEB_ANISOTROPY, W_PATH_PROJECTION
disabled channels:         W_VOID_MATURITY, W_TIME_READOUT
current theory vector:     not computed
endpoint scoring:          disabled
```

The future theory vector may only be generated after the web/path projection
mapping, source-kernel policy, null controls, and scoring protocol are all
source-frozen. It must not use KiDS residuals, posterior chains, best-fit
cosmology choices, fit-improvement flags, or the observed data-vector values to
choose its form.

This is a theory-readiness and leakage-prevention artifact, not a lensing
prediction and not empirical validation.

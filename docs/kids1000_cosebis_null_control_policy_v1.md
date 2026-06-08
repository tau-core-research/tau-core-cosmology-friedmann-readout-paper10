# KiDS-1000 COSEBIs Null-Control Policy v1

This declares the first non-scoring null-control policy for the future
KiDS-1000 COSEBIs web/path lensing route.

Frozen control families:

```text
sky_rotation
tomographic_pair_shuffle
wrong_channel_activation
web_path_sign_flip
```

These controls are declared but not executed in this artifact. A future endpoint
must freeze the control seed policy and multiplicity before running them. The
control set must not be chosen using KiDS data-vector values, residuals,
posterior chains, best-fit cosmology choices, or fit-improvement flags.

This is a leakage-prevention artifact, not a lensing null-test result and not
empirical validation.

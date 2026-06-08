# KiDS-1000 COSEBIs Null-Control Seed Policy v1

This freezes the seed and multiplicity table for the future KiDS-1000 COSEBIs
null-control families.

The policy is deliberately not a control execution. It records deterministic
family seeds and planned multiplicities only. It contains no control scores, no
lensing predictions, no residuals, and no fit statistics.

Frozen families:

```text
sky_rotation
tomographic_pair_shuffle
wrong_channel_activation
web_path_sign_flip
```

The artifact is source-side protocol scaffolding for future scoring. It forbids
post-hoc seed selection, post-hoc control multiplicity changes, KiDS data-vector
values, posterior chains, residuals, and fit-improvement flags.

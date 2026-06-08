# KiDS-1000 COSEBIs Web/Path Mapping Policy v1

This declares the future source-side mapping gate for the KiDS-1000 COSEBIs
lensing route. It deliberately does not compute a mapping and does not build a
theory vector.

Frozen requirements:

```text
target statistic:      COSEBIs
target vector length:  300 rows
active channels:       W_WEB_ANISOTROPY, W_PATH_PROJECTION
current mapping:       not computed
endpoint scoring:      disabled
```

The future mapping requires source-frozen inputs before scoring:

```text
source_frozen_web_environment_catalog
source_frozen_lensing_path_mask_or_depth_map
source_frozen_redshift_kernel_mapping
source_frozen_null_sky_rotation_or_pair_shuffle
```

The mapping must not use KiDS data-vector values, residuals, posterior chains,
best-fit cosmology choices, post-hoc sky directions, or fit-improvement flags to
choose its form.

This is a source-grounding and leakage-prevention artifact, not a lensing
prediction and not empirical validation.

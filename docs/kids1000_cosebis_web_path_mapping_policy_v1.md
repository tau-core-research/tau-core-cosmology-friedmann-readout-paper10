# KiDS-1000 COSEBIs Web/Path Mapping Policy v1

This declares the source-side mapping gate for the KiDS-1000 COSEBIs lensing
route. The current release now includes a source-frozen 300-row mapping basis,
but it still does not build a theory vector, prediction, residual, fit
statistic, or endpoint score.

Frozen requirements:

```text
target statistic:      COSEBIs
target vector length:  300 rows
active channels:       W_WEB_ANISOTROPY, W_PATH_PROJECTION
current mapping:       source-frozen mapping basis available
endpoint scoring:      disabled
```

The current mapping basis uses source-frozen `F_overlap`, `D_path`, uniform
null-control `E_web`, and `C_norm`. Future endpoint scoring still requires:

```text
source_frozen_web_environment_catalog
source_frozen_lensing_path_mask_or_depth_map
source_frozen_null_sky_rotation_or_pair_shuffle
```

The available basis has 300 target rows and 15 unique tomographic-pair values.
It has pair/redshift/path variation, but no COSEBIs mode-shape and no theory
vector. `W_web` remains zero because no positive web/environment catalogue has
been promoted.

The mapping must not use KiDS data-vector values, residuals, posterior chains,
best-fit cosmology choices, post-hoc sky directions, or fit-improvement flags to
choose its form.

This is a source-grounding and leakage-prevention artifact, not a lensing
prediction and not empirical validation.

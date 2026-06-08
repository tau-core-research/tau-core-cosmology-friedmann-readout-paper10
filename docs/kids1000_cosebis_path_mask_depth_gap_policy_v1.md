# KiDS-1000 COSEBIs Path Mask/Depth Gap Policy v1

This records a source-side gap audit for the future KiDS-1000 COSEBIs
observer/path projection channel.

The selected KiDS-1000 cosmic-shear release tarball contains statistic FITS
files, chains, configuration files, and plotting scripts. In the present
package it does not provide a separate source-frozen footprint, depth map,
survey mask map, random catalogue, or equivalent path-load product from which a
`W_PATH_PROJECTION` mapping can be constructed.

The audit therefore freezes a blocker rather than a score:

```text
source_frozen_lensing_path_mask_or_depth_map -> external product required
```

This artifact does not compute a path mapping, does not build a theory vector,
and does not use KiDS data-vector values, residuals, posterior chains, or
fit-improvement information.

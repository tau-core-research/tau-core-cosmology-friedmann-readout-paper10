# KiDS-1000 COSEBIs Lensing Route v1

This route declares COSEBIs as the first narrow weak-lensing statistic route
for a future Paper 10 lensing pilot. The choice is source-side: the KiDS page
identifies COSEBIs as the fiducial analysis statistic for the KiDS-1000 cosmic
shear release, and the tarball contains a dedicated COSEBIs FITS product.

The selected member pattern is:

```text
KiDS1000_cosmis_shear_data_release/data_fits/cosebis_*.fits
```

Allowed future lensing channels:

```text
W_web
W_path
```

Disabled in this route:

```text
W_void
W_time
```

This is still not a scoring artifact. Before scoring, the following must be
frozen from source-side information only:

```text
data_vector_hdu_policy
covariance_hdu_policy
tomographic_bin_policy
theta_or_mode_cut_policy
mask_policy
lensing_readout_observable_policy
```

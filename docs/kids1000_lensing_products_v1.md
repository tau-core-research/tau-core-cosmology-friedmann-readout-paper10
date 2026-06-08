# KiDS-1000 Lensing Products v1

This gate fetches and checksum-locks the public KiDS-1000 cosmic-shear data
products tarball. It does not run a lensing likelihood and does not choose a
Tau Core lensing score.

The tarball is kept as a source-native raw product under:

```text
data/raw/weak_lensing/kids1000/KiDS1000_cosmic_shear_data_release.tgz
```

The endpoint remains disabled because a lensing score requires additional
source-side choices:

```text
tomographic_bin_policy
statistic_choice
covariance_block_policy
mask_policy
S8_or_data_vector_readout_policy
```

No lensing residuals, model predictions, fitted Tau parameters, or posterior
reweighting are used in this artifact.

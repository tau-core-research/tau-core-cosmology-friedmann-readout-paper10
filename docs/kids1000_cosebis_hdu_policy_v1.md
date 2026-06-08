# KiDS-1000 COSEBIs HDU Policy v1

This freezes the internal FITS role mapping for the selected KiDS-1000 COSEBIs
file. It is still not a lensing likelihood.

Frozen roles:

```text
COVMAT    -> covariance matrix, expected shape 300 x 300
En        -> COSEBIs data-vector table, expected rows 300
NZ_SOURCE -> source redshift distribution table, expected rows 119
```

The covariance is checked for positive definiteness, and the data-vector table
is checked for the expected source-side columns:

```text
BIN1, BIN2, ANGBIN, VALUE, ANG
```

This HDU policy does not define a theory prediction, does not choose a Tau Core
amplitude, and does not evaluate residuals. The remaining future gates are:

```text
tomographic_pair_mapping_policy
mode_cut_policy
covariance_inversion_policy
lensing_theory_model_policy
web_path_projection_mapping_policy
```

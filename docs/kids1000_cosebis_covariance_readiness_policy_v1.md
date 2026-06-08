# KiDS-1000 COSEBIs Covariance Readiness Policy v1

This freezes a non-scoring covariance-readiness diagnostic for the selected
KiDS-1000 COSEBIs covariance block.

Frozen covariance block:

```text
COVMAT -> expected 300 x 300 covariance matrix
```

The diagnostic records only source-side numerical properties:

```text
shape
symmetry error
minimum and maximum diagonal element
minimum and maximum eigenvalue
condition number
Cholesky-readiness
```

This policy does not save an inverse covariance, does not select a data-vector
mask or mode cut, does not choose a theory vector, and does not evaluate a
lensing likelihood. The remaining future gates are:

```text
theory_prediction_policy
data_vector_mask_policy
mode_cut_policy
tomographic_weight_policy
covariance_subselection_policy
covariance_inversion_policy
```

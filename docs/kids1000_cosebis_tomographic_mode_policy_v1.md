# KiDS-1000 COSEBIs Tomographic/Mode Policy v1

This freezes the source-side tomographic and COSEBIs-mode structure of the
selected KiDS-1000 COSEBIs data-vector HDU. It is a pre-score inventory only.

Frozen source-side structure:

```text
source bins:        5
tomographic pairs: 15 upper-triangular bin pairs
COSEBIs modes:     20 modes per pair
data-vector rows:  300
```

The policy records that the selected `En` table contains one complete block for
each upper-triangular tomographic pair:

```text
(1,1), (1,2), (1,3), (1,4), (1,5),
(2,2), (2,3), (2,4), (2,5),
(3,3), (3,4), (3,5),
(4,4), (4,5),
(5,5)
```

and modes `1..20` for each pair.

This policy does not choose a theory prediction, amplitude, mode cut, covariance
inverse, or Tau Core lensing score. The remaining future gates are:

```text
mode_cut_policy
tomographic_weight_policy
theory_prediction_policy
covariance_inversion_policy
web_path_projection_mapping_policy
```

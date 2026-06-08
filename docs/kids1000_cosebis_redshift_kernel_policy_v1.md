# KiDS-1000 COSEBIs Redshift-Kernel Policy v1

This freezes the source-side redshift-kernel summary for the selected
KiDS-1000 COSEBIs route.

Source HDU:

```text
NZ_SOURCE -> 119 rows
columns   -> Z_LOW, Z_MID, Z_HIGH, BIN1, BIN2, BIN3, BIN4, BIN5
```

The generated inventory records, for each source bin, the source-side
normalization area, mean redshift, and nonzero support interval. This is a
source-kernel readiness artifact only. It does not compute a lensing theory
vector, does not reweight redshift bins using endpoint behavior, and does not
use KiDS data-vector values, residuals, posterior chains, or fit improvement.

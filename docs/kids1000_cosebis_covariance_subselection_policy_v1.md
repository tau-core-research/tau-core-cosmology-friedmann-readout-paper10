# KiDS-1000 COSEBIs Covariance Subselection Policy v1

This freezes the first non-scoring covariance-subselection policy for the
selected KiDS-1000 COSEBIs data vector.

Frozen policy:

```text
data-vector rows retained: 300 / 300
covariance block retained: 300 x 300 / 300 x 300
subselection policy:       retain full covariance for all retained rows
```

Because the mask/mode-cut policy retains all COSEBIs rows, the covariance block
is not subsetted. The inventory records the row intervals associated with each
tomographic pair, but it does not save an inverse covariance and does not define
a likelihood.

This policy is a leakage-prevention artifact: no covariance block, row interval,
or tomographic pair is selected using endpoint residuals, posterior chains, or
fit improvement.

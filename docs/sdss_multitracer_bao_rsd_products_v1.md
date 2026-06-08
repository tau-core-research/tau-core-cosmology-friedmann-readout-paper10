# SDSS Multi-Tracer BAO/RSD Products v1

This product-freeze gate fetches the official SDSS final BAO/RSD multi-tracer
LRG+ELG compressed products referenced from the SDSS final BAO/RSD measurements
page. The fetched products include both configuration-space and Fourier-space
compressed measurements, each with its covariance matrix.

The next pilot uses only the Fourier-space six-component vector:

```text
z=0.70:  D_M/r_d, D_H/r_d, f sigma_8
z=0.845: D_M/r_d, D_H/r_d, f sigma_8
```

with the official 6x6 covariance supplied in the compressed product. This is a
stronger growth/BAO gate than the earlier diagonal six-point `f sigma_8` summary,
but it remains a pilot and not endpoint validation.

Endpoint leakage remains forbidden. The product manifest contains no fitted Tau
parameters, no residuals, and no endpoint score.

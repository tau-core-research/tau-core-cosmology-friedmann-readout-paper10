# KiDS-1000 Lensing Route v1

This artifact freezes a candidate public weak-lensing source route without
fetching or redistributing the raw lensing product.

The KiDS-1000 weak-lensing page states that the cosmic-shear tarball includes
sampled posteriors, FITS data vectors, covariance matrices, redshift
distributions, redshift-distribution covariance, CosmoSIS configuration files,
and plotting scripts. This is sufficient to declare a future lensing block
route, but not sufficient to score a Tau Core lensing channel.

Endpoint scoring remains forbidden until the following are frozen without
looking at lensing residuals:

```text
tomographic_bin_policy
statistic_choice_COSEBIs_or_2PCF_or_bandpowers
covariance_block_policy
mask_policy
S8_or_data_vector_readout_policy
```

The current check records only source-route metadata from a HEAD request:
status code, content length, content type, ETag, and last-modified date. It does
not contain KiDS catalogues, data vectors, covariance matrices, posterior
chains, model predictions, residuals, or fit statistics.

# Data Notice

This repository is a protocol scaffold for Paper 10. It does not redistribute
raw survey data, CMB maps, MCMC chains, FITS products, void catalogues, weak
lensing catalogues, or proprietary survey products.

The first release contains only compact protocol artifacts and smoke-test
tables. Future empirical versions should keep raw data acquisition separate and
document any online data dependencies explicitly.

The current source registry is a manifest, not a data release:

```text
data/source_manifest/paper10_source_freeze_manifest.csv
```

Rows marked `SOURCE_SELECTED_NOT_FETCHED` identify candidate public source
families that still need acquisition, checksums, and frozen transformation
rules. Rows marked `BLOCKED_SOURCE_SELECTION` would identify scientifically
required blocks for which no accepted public source product has yet been
selected. In the current manifest, the first source-selection audit has selected
candidate public source families for all required blocks, but none of them are
yet `FETCHED_FROZEN`.

Planned public data families include:

- DESI BAO / cosmology products for distance constraints.
- Public supernova compilations such as Pantheon+ or DES-SN products where
  license and redistribution terms allow derived summaries.
- Cosmic chronometer `H(z)` compilations with citation and provenance.
- Planck / NASA LAMBDA CMB products for early-universe safety and CMB-lensing
  controls.
- Public void catalogues and cosmic-web / large-scale-structure classifiers.
- Public growth and lensing summaries such as RSD `f sigma_8`, weak-lensing,
  CMB-lensing, and cluster-lensing products.

No result in this repository should be read as a measurement claim until those
source blocks are acquired, frozen, and audited under the protocol in the
manuscript.

Endpoint scoring is not allowed until the required source blocks are either
`FETCHED_FROZEN` or explicitly excluded by a predeclared pilot-scope rule.

The committed provenance cache contains only official landing/source pages,
not raw survey products. It is used to verify source routes and URLs, not to
compute cosmological observables.

The product-freeze plan also contains no raw survey products. It records product
roles and unresolved acquisition policies. Every current product row has
`endpoint_allowed=false`.

The pilot frozen-product manifest includes three public distance-side files
under `data/raw/` only to test acquisition, hashing, covariance-shape checks,
and local provenance. These files are not sufficient for endpoint scoring
because the endpoint mask, calibration, nuisance-parameter, or systematics
policies are not frozen.

The Pantheon+ scope artifacts under `data/derived/` are row masks and summaries
derived only from source-side fields. They do not contain model residuals,
fitted Tau parameters, or endpoint scores.

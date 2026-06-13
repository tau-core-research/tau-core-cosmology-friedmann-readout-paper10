# Observer/path metric-product requirements package v1

**Doc class:** source-product requirements package
**Status:** not endpoint replay; not validation

The observer/path strengthening gate identifies the quickest non-lensing
fragility route, but it also blocks the physical metric/lensing path branch.
The block is narrow: the current 12-object scope has no source-aligned numeric
convergence, shear, mass-map integral, or metric/lensing path product.

This package asks an external reviewer to evaluate only the source-product
requirements for reopening that route. It does not authorize endpoint scoring.

Required product family:

- one row per source object in the active observer/path scope, with the same
  rule applicable to the wider low-z route-audit universe when promoted,
- a source-aligned numeric metric/path observable such as kappa, shear,
  projected mass-map integral, or documented null-geodesic/metric-environment
  path weight,
- provenance for the map/catalogue, coordinate match, mask/coverage status, and
  any normalization rule,
- no use of Pantheon residuals, endpoint scores, fitted distance residuals, or
  post-hoc selection by improvement.

Current blocker evidence:

- R5 requirement: `independent metric/lensing-path proxy such as convergence/shear or mass map integral`
- metric route status: `BLOCKED_FOR_ENDPOINT_UNTIL_SOURCE_ALIGNED_NUMERIC_PRODUCT`
- source-aligned metric count: `0`
- route-audit numeric count: `0`
- route-audit rows: `424`
- active observer/path scope rows: `12`
- blocked rows: `424`
- route-audit statuses: `{'BLOCKED_NO_SOURCE_ALIGNED_METRIC_LENSING_PRODUCT': 424}`

Allowed reviewer outcomes:

- `ACCEPT_REQUIREMENTS_ONLY`: requirements are sufficient for a future
  acquisition/freeze package, but no replay is authorized.
- `REQUEST_SOURCE_PRODUCT_DETAIL`: reviewer needs a more specific map/catalogue
  and coordinate/mask policy.
- `REJECT_AS_ENDPOINT_LEAKAGE_RISK`: requirements would allow residual or
  endpoint leakage.

Claim boundary: `observer_path_metric_product_requirements_not_endpoint_not_validation`.

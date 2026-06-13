# Observer/path metric-product requirements review notes v1

## Decision

`ACCEPT_REQUIREMENTS_ONLY`

## Scope

This review covers only the source-product requirements for a future observer/path metric-product acquisition/freeze package.

It does not authorize endpoint replay, endpoint scoring, endpoint validation, physical validation, or a physical lensing-path claim.

## Basis inside the package

- Active observer/path scope rows: `12`
- Wider low-z route-audit rows: `424`
- Source-aligned numeric metric/path products currently available: `0`
- Metric/lensing path status: `BLOCKED_FOR_ENDPOINT_UNTIL_SOURCE_ALIGNED_NUMERIC_PRODUCT`
- Route-audit blocked rows: `424`
- Route-audit numeric product count: `0`

## Review result

The requirements are sufficiently specific as requirements-only guidance because they require an independently sourced source-aligned numeric metric/path observable, such as:

- convergence (`kappa`),
- shear,
- projected mass-map integral,
- documented null-geodesic or metric-environment path weight.

They also require provenance, coordinate matching, mask/coverage status, and normalization rules, while forbidding Pantheon residuals, endpoint scores, fitted residuals, and post-hoc improvement selection.

## Boundary retained

```text
forbidden_inputs_used=false
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
```

## Caveat

The physical metric/lensing path remains blocked for endpoint use until a future package actually provides and freezes the source-aligned numeric product per source object. This response accepts requirements only; it does not provide the product.

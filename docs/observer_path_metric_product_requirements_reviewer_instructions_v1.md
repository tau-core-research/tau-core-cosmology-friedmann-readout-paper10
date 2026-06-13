# External reviewer instructions: observer/path metric product requirements v1

You do not need repository access for this review. Use only the files included
in this zip package.

## What you are reviewing

This package does **not** ask whether Tau Core is correct and does **not**
authorize endpoint scoring. It asks only whether the stated source-product
requirements are sufficient to acquire or construct a future observer/path
metric-product without endpoint leakage.

The current blocker is:

- active observer/path scope rows: `12`
- wider low-z route-audit rows: `424`
- source-aligned numeric metric/path products currently available: `0`
- endpoint replay allowed: `false`
- validation claimed: `false`

## Files to inspect

1. `docs/observer_path_metric_product_requirements_package_v1.md`
   - Plain-language summary of the blocker and allowed outcomes.
2. `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`
   - Full source requirements; focus especially on `R5`.
3. `data/derived/observer_path_strengthening_gate_v1.csv`
   - Route-level gate showing that the physical metric/lensing path branch is
     blocked until a source-aligned numeric product exists.
4. `data/derived/observer_path_strengthening_gate_v1_summary.csv`
   - One-row summary of the current blocker.
5. `data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1.csv`
   - Wider low-z route audit; this documents that the current audit has no
     source-aligned numeric kappa/shear/mass-map/path-weight product.
6. `data/derived/observer_path_metric_product_requirements_review_response_template_v1.csv`
   - Fill this file and return it.

## Allowed reviewer responses

Use one of these outcomes in `reviewer_response` for each row:

- `ACCEPT_REQUIREMENTS_ONLY`
- `REQUEST_SOURCE_PRODUCT_DETAIL`
- `REJECT_AS_ENDPOINT_LEAKAGE_RISK`

## Required safety checks

Please leave or set these fields as:

- `forbidden_inputs_used=false`
- `endpoint_replay_allowed=false`
- `endpoint_validation_claimed=false`
- `physical_lensing_path_weight_claimed=false`

If any requirement would permit use of Pantheon residuals, fitted distance
residuals, endpoint scores, or post-hoc selection by improvement, mark the
relevant row as `REJECT_AS_ENDPOINT_LEAKAGE_RISK` and explain why.

## What would count as a useful future source product

A future acquisition/freeze package should provide, per source object, at least
one independently sourced numeric metric/path observable such as:

- convergence (`kappa`),
- shear,
- projected mass-map integral,
- documented null-geodesic or metric-environment path weight.

It should also document coordinate matching, coverage/mask status, provenance,
and normalization without using endpoint residuals or score improvement.

Claim boundary: `observer_path_metric_product_requirements_not_endpoint_not_validation`.

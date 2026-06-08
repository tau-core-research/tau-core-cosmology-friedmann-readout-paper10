# Paper 10 Product-Freeze Plan

The source manifest selects public source families. The product-freeze plan is
the next layer down: it states which product type must be acquired from each
source family before a real-data pilot can begin.

The product-freeze plan is:

```text
data/source_manifest/paper10_product_freeze_plan.csv
```

## Why This Layer Exists

Source-family selection is not enough. For example, saying "Planck" or
"KiDS-1000" does not freeze:

- which data product,
- which covariance or chain,
- which mask or tomographic binning,
- which transformation rule,
- or which local artifact path.

The product-freeze plan makes those unresolved decisions explicit.

## Status Labels

`PRODUCT_SELECTED_NOT_FETCHED`

The product role and source route are declared, but the exact file/product is
not yet acquired and checksummed.

`PRODUCT_FETCHED_FROZEN`

Future status only. The exact product has been downloaded or archived, the
checksum is recorded, and the transformation rule is frozen.

`PRODUCT_BLOCKED`

The source family exists, but the exact product route is not acceptable yet.

## Endpoint Rule

Every current row has:

```text
endpoint_allowed=false
```

This is intentional. The product-freeze plan is a preflight artifact, not an
endpoint dataset.

Endpoint scoring becomes allowed only after a narrower pilot manifest promotes
specific rows to `PRODUCT_FETCHED_FROZEN` and records:

- exact product URL or immutable archive identifier,
- local path,
- checksum,
- transformation rule,
- covariance policy,
- mask/selection policy,
- and forbidden endpoint fields.

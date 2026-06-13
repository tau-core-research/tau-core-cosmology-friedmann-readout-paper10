# Paper10 DESI shape-core source support scan v1

**Doc class:** source-side support scan
**Reader role:** reviewer / data-acquisition auditor
**Status:** existing frozen-source scan, not replay, not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This scan checks whether the already frozen cosmic-chronometer table contains
independent in-interval support for the two core-sensitive DESI shape rows.

Result:

- The P0 target `DESI_SHAPE_ROW_2_CORE_SUPPORT` has an existing independent
  in-interval clock point at `z=1.037`, from `Moresco et al. (2012)`.
- This partially strengthens row 2 because the current row-2 endpoints are both
  supported by the Simon et al. reference family.
- It does not make the DESI shape route endpoint-ready: the Moresco point is
  in-interval support, not a full endpoint-pair replacement and not a replay
  authorization.

Claim boundary:

```text
paper10_desi_shape_core_source_support_scan_not_validation
```

The next allowed action is to promote the row-2 support into a reviewed source
attachment, or to seek endpoint-pair independence before any replay promotion.

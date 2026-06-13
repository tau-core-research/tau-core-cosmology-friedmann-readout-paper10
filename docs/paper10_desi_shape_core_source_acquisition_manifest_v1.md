# Paper10 DESI shape-core source acquisition manifest v1

**Doc class:** source-side acquisition manifest
**Reader role:** reviewer / data-acquisition handoff
**Status:** frozen target manifest, not fetched, not replay, not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

The DESI shape-route robustness stress showed that the permission-only replay
signal is carried mainly by the middle shape rows, especially rows 1 and 2.
This manifest freezes the next source-acquisition targets before any new source
fetch or replay.

Priority:

- `P0`: `DESI_SHAPE_ROW_2_CORE_SUPPORT`, because row 2 is core-sensitive and
  currently source-caveated by a single-reference-family pair.
- `P1`: `DESI_SHAPE_ROW_1_CORE_SUPPORT`, because row 1 is the most required row
  and should receive confirmatory independent support.

Allowed source types include peer-reviewed cosmic chronometer \(H(z)\), public
clock compilations, source-native BAO/CC shape support, or an independent
time-readout shape observable.  Endpoint residuals, endpoint scores, posterior
chains, and validation language remain forbidden.

Claim boundary:

```text
paper10_desi_shape_core_source_acquisition_manifest_not_validation
```

The manifest does not fetch new sources and does not authorize endpoint replay.

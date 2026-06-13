# Paper10 DESI shape-row sensitivity source audit v1

**Doc class:** source-side diagnostic ledger
**Reader role:** reviewer / reproducibility auditor
**Status:** permission-replay follow-up, not endpoint validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This ledger explains the narrow-margin DESI shape-route replay without opening
a new endpoint.  It maps each adjacent `CLOCK_SLOPE_SHAPE` row to its radial
BAO/CC support interval and to the leave-one robustness loss.

The key distinction is:

- dropping shape row 0 almost preserves the full score, so row 0 is not the
  main carrier of the signal;
- rows 1 and 2 are the core-sensitive middle shape rows;
- row 2 is source-caveated because both endpoints are supported by the same
  current CC reference family in the existing manifest.

Claim boundary:

```text
row_sensitivity_explained_as_middle_shape_row_core_but_source_caveated_not_validation
```

This is not endpoint validation and not physical validation.  The recommended
next action is independent clock or shape support for rows 1 and 2 before any
promotion of the DESI shape route.

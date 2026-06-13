# Paper10 DESI shape row2 left strict-support scout v1

**Doc class:** source-side strict endpoint-support scout
**Reader role:** reviewer / source-acquisition auditor
**Status:** negative source-side scout, not replay, not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This scout checks the frozen cosmic-chronometer table after the
row-2 source-window review reopened the left endpoint only as caveated
source context. It asks a narrow question: is there an independent
source in the strict row-2 left endpoint window?

Frozen result:

- row-2 left endpoint: `0.934`
- strict window: `0.05`
- strict independent support count: `0`
- nearest candidate: `Simon et al. (2005)` at `z=0.9`
- nearest independent candidate: `Stern et al. (2010)` at `z=0.88`
- endpoint replay allowed: `false`

Nearest frozen CC candidates:

| Reference | z | abs delta-z | class |
| --- | ---: | ---: | --- |
| Simon et al. (2005) | 0.9 | 0.034 | strict_same_family_context |
| Stern et al. (2010) | 0.88 | 0.054 | relaxed_independent_near_window_context |
| Moresco et al. (2012) | 0.8754 | 0.0586 | relaxed_independent_near_window_context |

Interpretation:

The frozen CC table contains near-window context, but no strict
independent left-endpoint support. This preserves a negative
source-side result: the P0 strict-support route remains open.

Claim boundary:

```text
paper10_desi_shape_row2_left_strict_support_scout_not_validation
```

Machine verdict: `row2_left_strict_support_absent_in_frozen_cc_table`.

# Paper10 DESI shape row2 source-native shape-support scout v1

**Doc class:** source-native BAO shape-support scout
**Reader role:** reviewer / source-acquisition auditor
**Status:** source-side support present, not replay, not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This scout addresses the second P0 target in the post-window-review
source plan: source-native shape support for the row-2 interval. It
uses only the frozen DESI DR2 BAO mean vector and covariance block.
It does not use endpoint residuals, endpoint scores, or fit feedback.

Frozen result:

- row-2 interval: `0.934-1.321`
- source-native rows found: `4`
- covariance positive definite: `true`
- shape vector: `delta_log_DM_over_rs=0.246281910984;delta_log_DH_over_rs=-0.218701863111;delta_log_anisotropy_DM_over_DH=0.464983774095;slope_log_DM_over_rs=0.636387366883;slope_log_DH_over_rs=-0.565121093311`
- row2 promotion ready: `false`
- endpoint replay allowed: `false`

Frozen source rows:

| Row | z | quantity | value | role |
| ---: | ---: | --- | ---: | --- |
| 5 | 0.93400000 | DM_over_rs | 21.57563956 | row2_left_transverse_shape |
| 6 | 0.93400000 | DH_over_rs | 17.64149464 | row2_left_radial_shape |
| 7 | 1.32100000 | DM_over_rs | 27.60085612 | row2_right_transverse_shape |
| 8 | 1.32100000 | DH_over_rs | 14.17602155 | row2_right_radial_shape |

Interpretation:

Row 2 has source-native DESI BAO shape information at both interval
ends (`DM/rs` and `DH/rs`) with a well-formed covariance subblock.
This is stronger source context than a clock near-miss, but it is not
a replay authorization and does not by itself promote the route.

Claim boundary:

```text
paper10_desi_shape_row2_source_native_shape_support_scout_not_validation
```

Machine verdict: `row2_source_native_desi_bao_shape_support_present_but_not_promotion_ready`.

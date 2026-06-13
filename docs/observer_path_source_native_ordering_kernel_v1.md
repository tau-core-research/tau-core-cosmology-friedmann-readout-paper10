# Observer/path source-native ordering kernel v1

**Doc class:** source-side kernel-bank construction
**Status:** not endpoint replay; not validation; no residual fields
**Claim boundary:** `observer_path_source_native_ordering_kernel_source_side_not_endpoint`

The previous metric-environment product improved the baseline but
failed the rank-reversal control. This artifact freezes a small
source-native ordering-bank before any new scoring claim. The bank
uses only the already frozen metric-environment product, observer
orientation basis, and source redshift coordinate.

Kernel families:

- `K_order_metric_environment`: direct metric-environment carrier.
- `K_order_los_web_gate`: LOS/web gate modulated by path-void support.
- `K_order_void_web_los_balanced`: balanced source-side environment rule.
- `K_order_metric_los_skyz`: metric environment modulated by LOS and sky-z.
- `K_order_metric_observer_x_z`: metric environment modulated by observer x and centered redshift.
- `K_order_metric_environment_gradient`: web-minus-LOS environment gradient.

This is a candidate bank for a preauthorization screen only. It does
not authorize endpoint replay and does not claim physical lensing.

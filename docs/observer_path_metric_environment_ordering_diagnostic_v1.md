# Observer/path metric-environment ordering diagnostic v1

**Doc class:** source-side ordering diagnostic
**Status:** not endpoint replay; not validation; no distance residuals
**Claim boundary:** `observer_path_metric_environment_ordering_diagnostic_source_side_not_endpoint`

The metric-environment fast screen improved relative to the baseline
but failed the rank-reversal control. This diagnostic records the
source-side ordering of the metric-environment product and compares
it to frozen source observables. It is not a retuning step.

Summary:

- rows: `12`
- best candidate family: `metric_environment_path`
- best control branch: `rank_reverse`
- candidate minus best-control delta chi2: `0.12520399356`
- Spearman(metric environment, zHD): `-0.195804195804`
- Spearman(metric environment, W_path): `-0.048951048951`
- verdict: `SOURCE_ORDER_NOT_CONTROL_RESISTANT_REQUIRES_SOURCE_NATIVE_REORDERING_NOT_ENDPOINT`

Interpretation: the current source-side product is too weakly
control-resistant for replay promotion. A next kernel must provide a
source-native ordering rule that is frozen before endpoint scoring.

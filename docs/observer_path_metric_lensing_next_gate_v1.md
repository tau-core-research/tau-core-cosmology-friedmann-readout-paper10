# Observer/path metric-lensing next gate v1

**Doc class:** next-action gate
**Status:** not endpoint replay; not validation
**Claim boundary:** `observer_path_metric_lensing_next_gate_not_endpoint_not_validation`

This gate prevents the observer/path route from turning a weak
metric-environment proxy into an endpoint claim. It combines the
acquisition status, the metric-environment fast screen, and the
source-native ordering-bank screen.

Summary:

- caveated proxy available: `true`
- ACT DR6 source-side kappa sampling available: `true`
- ACT DR6 source-frozen path-weight candidate available: `true`
- ACT DR6 mask-positive rows: `168/424`
- physical metric/lensing path product available: `false`
- metric-environment screen survives controls: `false`
- source-native ordering screen survives controls: `false`
- endpoint replay allowed: `false`
- next required action: `external_review_and_replay_authorization_for_act_path_weight_candidate`
- verdict: `ACT_DR6_PATH_WEIGHT_CANDIDATE_READY_BUT_REVIEW_BLOCKS_REPLAY`

Interpretation: the current quick products are useful diagnostics
but do not authorize replay. The focused next step is external
review and replay authorization for the ACT path-weight candidate,
including explicit null-control handling, before any endpoint scoring.

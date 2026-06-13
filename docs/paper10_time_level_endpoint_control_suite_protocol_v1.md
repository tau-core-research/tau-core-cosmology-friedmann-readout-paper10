# Paper 10 time-level endpoint control-suite protocol v1

**Doc class:** source-side endpoint-control protocol
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time-level external-r_d readiness gate

This protocol freezes the control families that a future `time_level_route`
endpoint would have to survive.  It declares the control suite only.  It does
not run endpoint scores, does not select a successful branch, and does not
authorize replay.

Required control families:

```text
rd_off_control
external_prior_width_stress
wrong_prior_control
BAO_pair_drop_control
CC_match_window_stress
level_slope_swap_control
redshift_order_shuffle_control
```

Minimum requirements:

```text
all_control_families_declared_before_endpoint
seeds_frozen_before_replay
control_outputs_reported_before_interpretation
```

Forbidden inputs:

```text
Pantheon_distance_residuals
fit_statistics
endpoint_scores
late_time_fit_parameters
posthoc_control_selection
posthoc_seed_selection
control_family_dropped_after_score
```

This closes only the protocol-definition part of the endpoint-control blocker.
The route remains blocked until radial-BAO support is expanded and the declared
controls are actually frozen and replayed under a separate authorization gate.

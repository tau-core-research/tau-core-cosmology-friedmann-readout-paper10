# Paper 10 BAO r_d marginalization protocol v1

**Doc class:** source-side nuisance/marginalization protocol
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time-level route nuisance/interface freeze plan

This protocol freezes the interface needed before the radial-BAO time-level
route can use absolute BAO information.  The source observable is

```text
D_H / r_d = c / (H(z) r_d)
```

so

```text
-log(D_H / r_d) = log H(z) + beta_rd
beta_rd := log(r_d) - log(c)
```

in consistent units.  The nuisance parameter is therefore `beta_rd`, not a
free Tau Core signal.

Allowed handling:

```text
analytic_linear_nuisance_projection_or_predeclared_rd_prior_marginalization_only
```

Required source-side inputs:

```text
radial_BAO_DH_over_rd_rows
matched_CC_logH_support
rd_prior_response_or_broad_beta_grid_policy
unit_convention_c_km_s
```

Forbidden inputs:

```text
Pantheon_distance_residuals
fit_statistics
endpoint_scores
late_time_fit_parameters
posthoc_rd_choice
posthoc_beta_grid_from_endpoint
BAO_support_for_clock_slope_claim
```

Required controls:

```text
rd_off_control
external_prior_width_stress
wrong_prior_control
BAO_pair_drop_control
CC_match_window_stress
```

This closes only the protocol-definition part of the `r_d` marginalization
blocker.  It does not supply enough BAO support for an endpoint, does not
compute a likelihood, and does not authorize replay.

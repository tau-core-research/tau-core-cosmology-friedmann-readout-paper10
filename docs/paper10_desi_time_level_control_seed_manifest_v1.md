# DESI Time-Level Control Seed Manifest V1

**Doc class:** source-side control seed manifest.

**Reader role:** Paper 10 endpoint-control auditor.

**Status:** seed manifest only; not control replay; not endpoint validation.

**Canonical parent:** `paper10_time_level_endpoint_control_suite_protocol_v1.md`.

This manifest freezes deterministic seeds for the seven time-level endpoint
control families declared before replay:

```text
rd_off_control
external_prior_width_stress
wrong_prior_control
BAO_pair_drop_control
CC_match_window_stress
level_slope_swap_control
redshift_order_shuffle_control
```

The scope is the first CC-matched DESI five-row route, after the high-z
`z=2.33` row is predeclared as holdout/future support.

## Claim Boundary

```text
paper10_desi_time_level_control_seed_manifest_not_validation
```

The manifest does not run controls, compute scores, or authorize endpoint
replay. It only prevents later posthoc control-family or seed selection.

## Current Verdict

```text
desi_time_level_control_seed_manifest_frozen_not_replayed
```

# Cosmology Activation Parameter Freeze Plan v1

The activation-rule manifest declares non-numeric shells. This file declares
how the scales and optional parameters in those shells may later be frozen:

```text
data/source_manifest/cosmology_activation_parameter_freeze_plan_v1.csv
```

This is still not an endpoint dataset. It is a source-freeze plan for the
future numerical values.

## Why This Layer Exists

The activation shells contain symbols such as:

```text
S_void_star
optional_q
Q_env_star
class_weight_table
P_lens_star
mask_weight_policy
Delta_clock_star
redshift_bin_policy
```

If these were chosen after looking at distance, growth, or lensing residuals,
the later pilot would become curve rescue. The parameter-freeze plan prevents
that by declaring source-native freeze routes before endpoint scoring.

## Current Status

All rows are:

```text
PARAMETER_FREEZE_ROUTE_DECLARED_NOT_NUMERIC
endpoint_scoring_allowed=false
```

The future values are expected in:

```text
data/derived/cosmology_parameter_freeze_values_v1.csv
```

That future value file does not exist yet and is not required for the current
protocol scaffold.

## Claim Boundary

This plan does not claim that the listed scales exist as Tau-side constants.
It only states how a future source-native numerical freeze must be performed
without target residual leakage.

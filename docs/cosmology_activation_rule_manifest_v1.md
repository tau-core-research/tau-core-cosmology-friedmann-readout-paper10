# Cosmology Activation Rule Manifest v1

The channel manifest declares the four allowed cosmological readout channels.
The activation-rule manifest declares the first non-numeric rule shells for
those channels:

```text
data/source_manifest/cosmology_activation_rule_manifest_v1.csv
```

This is still below endpoint status. It does not compute a cosmological
likelihood and it does not authorize a Tau Core signal claim.

## Why This Layer Exists

Without an activation-rule layer, a future analysis could choose a convenient
functional form after seeing the endpoint residuals. The activation-rule
manifest prevents that by requiring each channel to have:

```text
source inputs;
normalization policy;
formula shell;
allowed free parameters;
parameter-freeze policy;
forbidden endpoint inputs;
null controls;
output range.
```

## Declared Rule Shells

| Rule | Channel | Shell | Status |
| --- | --- | --- | --- |
| `ACT_VOID_MATURITY_V1` | `W_VOID_MATURITY` | `Xi_void=S_void/S_void_star; W_void=Xi_void/(1+Xi_void)` | non-numeric |
| `ACT_WEB_ANISOTROPY_V1` | `W_WEB_ANISOTROPY` | `Q_web=Q_env/Q_env_star; W_web=tanh(Q_web)` | non-numeric |
| `ACT_PATH_PROJECTION_V1` | `W_PATH_PROJECTION` | `P_path=P_lens/P_lens_star; W_path=P_path/(1+abs(P_path))` | non-numeric |
| `ACT_TIME_READOUT_V1` | `W_TIME_READOUT` | `T_read=Delta_clock/Delta_clock_star; W_time=T_read/(1+abs(T_read))` | non-numeric |

## Claim Boundary

These are protocol shells only. The scales such as `S_void_star`,
`Q_env_star`, `P_lens_star`, and `Delta_clock_star` must later be frozen from
source-native information, not from distance, growth, or lensing residuals.

The current status is:

```text
RULE_SHELL_DECLARED_NOT_NUMERIC
endpoint_scoring_allowed=false
```

The companion parameter-freeze plan is:

```text
data/source_manifest/cosmology_activation_parameter_freeze_plan_v1.csv
docs/cosmology_activation_parameter_freeze_plan_v1.md
```

## Projection-Induction Role

These shells are compatible with the projection-induction gate only as first
activation candidates. A future derivation would still need to show:

```text
source-side mode
-> activated channel variable
-> quotient-safe class
-> closure-stable readout
-> 4D observable or closure source.
```

Until then, the rule shells are reproducible protocol constraints, not Tau-side
derivations.

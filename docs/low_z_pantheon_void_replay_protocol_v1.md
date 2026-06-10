# Low-z Pantheon Void Replay Protocol v1

**Doc class:** frozen replay-protocol shell  
**Status:** frozen, not run, not validation  

This protocol freezes the scoring grammar for a possible future low-redshift
Pantheon void replay. It does not run the replay and does not authorize a
replay by itself.

## Parent scope

The parent scope is:

```text
LOW_Z_PANTHEON_VOID_SCOPE_CANDIDATE_POLICY_V1
```

It contains `424 / 1371` Pantheon rows selected only by the frozen low-z
void-support rule:

```text
zHD <= void_catalog_z_support_max_proxy
W_void_source_native_basis > 0
```

## Included block

Only one observable block is active:

```text
Pantheon_distance_low_z_void_supported_subset
```

The protocol is deliberately not a full-Pantheon endpoint and not a multiblock
cosmology validation.

## Active and disabled channels

Active:

```text
W_VOID_MATURITY
```

Disabled:

```text
W_WEB_ANISOTROPY
W_PATH_PROJECTION
W_TIME_READOUT
```

The low-z route exists only to test whether the current low-z void source basis
has any internally consistent distance-side replay signal on its own supported
scope.

## Frozen criterion shell

The future replay, if separately authorized, must use:

```text
AIC_lowz = chi2_lowz_distance + 2*k_shared
```

`BIC_lowz` may be reported only after `n_eff` is fixed to the included low-z
rows.

## Required controls

The replay must include:

- `baseline_only`
- `void_only`
- `wrong_void_sign`
- `wrong_void_threshold`
- `deterministic_shuffled_void_within_low_z_mask`
- `zero_void_amplitude`

## Claim boundary

This is not scoring and not validation:

```text
LOW_Z_VOID_REPLAY_PROTOCOL_FROZEN_NOT_RUN
```

No residuals, likelihoods, information criteria, endpoint ranks, or physical
validation claims are produced by this protocol artifact.

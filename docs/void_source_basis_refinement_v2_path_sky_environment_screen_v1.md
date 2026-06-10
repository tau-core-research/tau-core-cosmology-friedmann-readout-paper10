**Doc class:** preauthorization diagnostic screen
**Reader role:** Paper10 source-side projection-basis search
**Status:** fast path/sky/environment screen; not endpoint validation
**Canonical parent:** README.md

# V2 Path Sky/Environment Screen V1

This screen is the next fast search step after simple path transforms failed
control resistance. It remains a preauthorization diagnostic only.

In Tau Core language, the motivation is that measurement readouts are
observer/path dependent: the observed distance channel is not treated as a
view-from-nowhere scalar, but as a four-dimensional readout along a
source-observer projection route. This screen tests only the source-frozen
operational shadow of that idea.

The candidate basis bank uses only already frozen source-side quantities from:

- the 12-row partial path source values,
- the Pantheon RA/DEC to KiDS tile crossmap,
- the low-z line-of-sight environment ledger,
- the low-z void-geometry join.

No distance residual, endpoint score, fit statistic, posterior chain, KiDS data
vector, or post-hoc sky/path label is used to define the basis vectors.

## Candidate Basis Bank

The screen tests path-weighted source-side projection components:

```text
W_path
W_path_x_sky_x
W_path_x_sky_y
W_path_x_sky_z
W_path_x_tile_offset_ra
W_path_x_tile_offset_dec
W_path_x_los_log_count
W_path_x_los_density_excess
W_path_x_nearest_env_inverse_sep
W_path_x_nearest_env_density_excess
W_path_x_void_wall_proximity
W_path_x_signed_void_wall_proximity
W_path_x_inside_void
W_path_x_void_angular_proximity
```

All vectors are normalized by maximum absolute value on the same 12-row source
scope. Missing line-of-sight environment density values are treated as zero
environment support before normalization, because those rows have
`los_environment_count=0`.

## Controls

Each candidate is compared to:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
```

The screen can only justify a later authorization package if a source-side
candidate beats both the baseline and the frozen controls.

## Current Result

The global best candidate is `W_path_x_los_density_excess`, with a small
baseline improvement but no global control resistance. The candidate ranks
behind several controls, so the screen verdict is not positive endpoint
evidence.

One narrower follow-up signal is visible: `W_path_x_sky_z` survives its own
family controls in this 12-row screen. This is only a source-side follow-up
candidate, not a validation result. It suggests that observer/sky-orientation
components deserve a separate source-grounded authorization package before any
formal replay.

## Claim Boundary

```text
v2_path_sky_environment_screen_not_endpoint_not_validation
```

This is not an endpoint replay, not validation, and not a physical
lensing-path weight claim.

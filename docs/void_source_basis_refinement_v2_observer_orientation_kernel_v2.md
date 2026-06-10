**Doc class:** source-side kernel freeze
**Reader role:** Paper10 observer/path projection refinement
**Status:** predeclared kernel; not scoring and not validation
**Canonical parent:** README.md

# V2 Observer-Orientation Kernel

The previous `W_path_x_sky_z` replay found a narrow observer-orientation signal
on the 12-row partial path scope. This file freezes the next source-side kernel
before any new replay.

The current replay used the raw equatorial sky-z component:

```text
K_reference = W_path * sky_z
sky_z = sin(dec)
```

The V2 primary kernel removes the scope monopole of the sky-z coordinate:

```text
mean_sky_z = mean(sky_z over the 12 predeclared source rows)
K_v2_raw = W_path * (sky_z - mean_sky_z)
K_v2 = K_v2_raw / max(abs(K_v2_raw))
```

This keeps the sky-z direction while making the source-side candidate a
dipole-like observer-orientation proxy instead of a raw declination offset. It
uses only RA, DEC, the already frozen partial `W_path` source value, and the
predeclared 12-row scope.

## Required Controls For A Later Replay

Any later replay must compare the primary V2 kernel to:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
axis_x_reference
axis_y_reference
```

The x/y axis references are not allowed to become post-hoc replacements unless
a separate source-side authorization gate is opened.

## Claim Boundary

```text
v2_observer_orientation_kernel_v2_source_side_not_scoring
```


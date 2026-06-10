**Doc class:** replay authorization review package
**Reader role:** Paper10 observer/path projection reviewer
**Status:** permission package scaffold; not endpoint validation
**Canonical parent:** README.md

# V2 Observer-Orientation Kernel Replay Authorization

This package asks whether the predeclared centered observer-orientation kernel
may be replayed once on the same 12-row partial path scope.

The primary kernel is:

```text
K_v2 = W_path * (sky_z - mean_sky_z_scope)
```

This is a source-side refinement of the earlier `W_path * sky_z` replay. The
centering rule removes the scope monopole of the sky-z coordinate; it does not
use distance residuals, endpoint scores, fit statistics, posterior chains, or
post-hoc tuning.

## Allowed Decision

The reviewer may return:

```text
GO_OBSERVER_ORIENTATION_V2_REPLAY_PERMISSION_ONLY
```

This grants permission for one later replay only. It does not permit validation
language, population evidence language, or physical path-weight claims.

## Required Controls

Any replay must include:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
axis_x_reference
axis_y_reference
```

## Claim Boundary

```text
v2_observer_orientation_kernel_v2_replay_authorization_not_validation
```

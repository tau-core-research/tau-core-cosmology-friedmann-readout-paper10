**Doc class:** preauthorization diagnostic screen
**Reader role:** Paper10 source-basis search / claim-boundary audit
**Status:** fast source-transform screen; not endpoint validation
**Canonical parent:** README.md

# V2 Path Transform-Bank Screen V1

This artifact defines a faster search route after the first path-coupled
screen failed control resistance. It does not authorize endpoint replay and it
does not claim validation.

The screen asks a narrow question:

```text
Do any simple source-side transforms of the already frozen 12-row path
tile-separation control survive a quick candidate/control screen well enough
to justify a later reviewer authorization package?
```

The path transforms are derived only from the already frozen source-side
nearest KiDS tile separation and partial path value. They are not derived from
distance residuals, fit improvements, endpoint scores, sky-direction
post-selection, or path-weight tuning.

## Transform Bank

The frozen transform bank is:

```text
existing_W_path
tile_proximity_raw
tile_margin
tile_inverse_distance
tile_gaussian_sigma_0p5
tile_gaussian_sigma_1p0
tile_gaussian_sigma_2p0
tile_binary_core_1deg
tile_binary_near_1p5deg
tile_rank_quantile
```

Each transform is combined with four coupling modes:

```text
none
void
web
void_web
```

The `void` and `web` modes use the already frozen `W_void_centered` and
`W_web_centered` source vectors. All vectors are normalized by maximum absolute
value on the same 12-row source scope.

## Controls

Each candidate family is compared with:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
```

The screen is considered interesting only if a candidate beats the baseline and
the frozen controls. Even then, the only allowed conclusion is that a separate
authorization package may be prepared.

## Claim Boundary

```text
v2_path_transform_bank_screen_not_endpoint_not_validation
```

This artifact is a search screen, not a physics result and not an endpoint
validation.

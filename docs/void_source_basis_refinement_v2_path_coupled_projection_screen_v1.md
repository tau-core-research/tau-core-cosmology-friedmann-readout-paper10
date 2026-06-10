**Doc class:** preauthorization diagnostic screen
**Reader role:** Paper10 reproducibility / claim-boundary audit
**Status:** source-frozen fast screen; not endpoint validation
**Canonical parent:** README.md

# V2 Path-Coupled Projection Screen V1

This artifact defines a fast preauthorization screen for the V2 path channel.
It is not an endpoint replay authorization, not a validation claim, and not a
physical lensing-path weight claim.

The screen reuses only already frozen source-side values:

- `W_path_source_value` from the 12-row partial path scope,
- `W_void_centered` from the V2 void-morphology values,
- `W_web_centered` from the V2 web-morphology values.

The scope is exactly the same 12 predeclared rows used by the partial
permission-only `W_path` replay. No new row selection, sky-direction selection,
endpoint residual, fit statistic, posterior chain, or KiDS data-vector value is
used to construct the screen vectors.

## Candidate Families

The screen compares four source-frozen candidate vector families:

```text
W_path
W_path_x_W_void_centered
W_path_x_W_web_centered
W_path_x_W_void_centered_x_W_web_centered
```

Each vector is normalized by its maximum absolute value on the 12-row source
scope. This is a bounded diagnostic normalization rule, not a physical
amplitude derivation.

## Controls

For each candidate family, the screen also evaluates:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
```

The controls are deterministic and use the frozen seed `20260610`.

## Claim Boundary

The claim boundary is:

```text
v2_path_coupled_projection_screen_not_endpoint_not_validation
```

If a coupled family wins this screen, the allowed next step is only to prepare a
separate reviewer/authorization package for that family. It does not by itself
authorize endpoint scoring, endpoint validation, or a physical interpretation
of the path weight.

**Doc class:** replay authorization review package
**Reader role:** Paper10 source-side observer/path projection reviewer
**Status:** permission package scaffold; not endpoint validation
**Canonical parent:** README.md

# V2 Sky-Z Replay Authorization Review V1

This package asks a narrow question only:

```text
May the predeclared W_path_x_sky_z observer-orientation candidate be replayed
once on the already frozen 12-row partial path scope?
```

It does not contain endpoint residuals, endpoint scores, posterior chains,
KiDS data vector values, or physical lensing-path weight claims. It also does
not authorize validation claims.

## Why This Package Exists

The V2 path sky/environment screen was globally non-positive:

```text
global verdict: path_sky_environment_candidate_not_control_resistant_in_fast_screen
```

However, the `W_path_x_sky_z` family survived its own frozen family controls:

```text
family: W_path_x_sky_z
delta chi2 vs baseline: -0.44407920978
delta chi2 vs best family control: -0.06205941383
controls better than candidate: 0
```

This is a source-side follow-up signal for observer/sky-orientation dependence,
not endpoint evidence.

## Allowed Decision

The reviewer may return:

```text
GO_SKY_Z_REPLAY_PERMISSION_ONLY
```

or a no-go decision. A GO decision permits only one future replay of the
predeclared `W_path_x_sky_z` family on the 12-row partial path scope. It does
not permit endpoint-validation language.

## Forbidden Claims

```text
endpoint validation
physical lensing-path weight
population evidence
new gravitational law evidence
post-hoc sky-direction selection
```

## Claim Boundary

```text
v2_sky_z_replay_authorization_review_not_validation
```

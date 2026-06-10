**Doc class:** source-side follow-up review package
**Reader role:** Paper10 observer/path projection audit
**Status:** reviewer package scaffold; not endpoint validation
**Canonical parent:** README.md

# V2 Observer-Dependence Follow-Up V1

Tau Core motivates an observer/path-dependent readout principle: a measured
cosmological observable is not treated as a view-from-nowhere scalar, but as a
four-dimensional readout along a source-observer projection route. In the
current Paper10 operational layer, this principle must still be tested through
source-frozen observables and controls.

The current fast screen result is:

```text
screen: V2_PATH_SKY_ENVIRONMENT_SCREEN_V1
global verdict: path_sky_environment_candidate_not_control_resistant_in_fast_screen
follow-up family: W_path_x_sky_z
family delta chi2 vs baseline: -0.44407920978
family delta chi2 vs best family control: -0.06205941383
family controls better than candidate: 0
```

This is not endpoint validation. The global screen remains non-positive because
the best overall candidate is not globally control-resistant. However,
`W_path_x_sky_z` survives its own predeclared family controls, so it is a
source-side follow-up candidate for the observer-dependence principle.

## Why `sky_z` Matters

`sky_z` is the sine of the source declination in the source-observer sky frame.
Multiplying it by `W_path` tests whether the partial path projection control
has an orientation-dependent component. This is a minimal operational shadow of
observer-dependence, not a full physical path kernel.

## Allowed Claim

The allowed claim is:

```text
The V2 path sky/environment screen contains a narrow source-side follow-up
signal for observer/sky-orientation dependence in W_path_x_sky_z.
```

The forbidden claims are:

```text
endpoint validation
physical lensing-path weight
population evidence
new gravitational law evidence
post-hoc sky-direction selection
```

The only allowed next action is a separate replay authorization package for
`W_path_x_sky_z`, with `endpoint_validation_claimed=false`.

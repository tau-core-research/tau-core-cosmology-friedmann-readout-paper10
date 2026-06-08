# Pantheon Void/Web Proxy Full-Covariance Pilot v1

This is the first two-channel cosmology pilot after the homogeneous
`W_tau(a)` stress test.

## Status

```text
VOID_WEB_PROXY_FULL_COV_PILOT_NOT_VALIDATION
```

The pilot is not empirical validation and not a source-grounded Tau Core
cosmology result. It is a full-covariance scoring grammar test with only two
active channels:

```text
W_VOID_MATURITY
W_WEB_ANISOTROPY
```

The path and time channels are explicitly disabled:

```text
W_PATH_PROJECTION
W_TIME_READOUT
```

## Why It Exists

The homogeneous Pantheon+ pilot tested only one smooth late-time shell. This
pilot checks whether the code path can carry two frozen source-side channel
bases through the retained Pantheon+ STAT+SYS covariance scoring.

Because no source-native void or cosmic-web catalogue values are frozen yet,
the current `W_void` and `W_web` columns are redshift/scale-factor proxy bases
inside the design matrix. They are leakage-safe scaffold columns, not physical
void/web measurements.

## Controls

The scoring grid includes:

```text
baseline_only
void_web_proxy_shell
void_only
web_only
wrong_web_sign
deterministic_shuffled_void_web
```

## Claim Boundary

The output may be used to debug the two-channel full-covariance scoring ladder.
It must not be used as evidence that void maturity or cosmic-web anisotropy has
been detected.

## Current Result

On the frozen Pantheon+ full-covariance pilot:

```text
Delta chi2(void_web - baseline) = -0.05994162
Delta AIC(void_web - baseline)  = +3.94005838
```

The improvement in \(\chi^2\) is tiny and the AIC is worse because the proxy
shell carries more effective parameters. In addition, the current wrong/shuffled
controls can match or beat the proxy branch. This is therefore a successful
pipeline smoke test and a negative model-selection result for the present proxy
shell, not evidence for a cosmological signal.

The next allowed step is to replace the proxy bases with source-frozen public
void and cosmic-web products, then repeat the same controls.

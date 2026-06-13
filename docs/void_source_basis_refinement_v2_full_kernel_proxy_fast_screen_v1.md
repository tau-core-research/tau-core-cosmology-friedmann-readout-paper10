# Void Source-Basis Refinement v2: Full-Kernel Proxy Fast Screen v1

**Doc class:** preauthorization numerical diagnostic protocol.
**Status:** source-side fast screen only; not endpoint replay; not validation.
**Canonical parent:** Paper 10 observer/path projection refinement notes.

## Purpose

This screen tests whether the narrow observer-basis result

```text
W_path x sky_x x z_centered
```

can be strengthened by multiplying it with already frozen source-side void, web,
line-of-sight environment, and void-geometry proxy components.

The word `full` is used here only in the limited sense of moving toward a fuller
Tau Core observer/path kernel.  This artifact is not a full physical path kernel,
does not claim a physical lensing path weight, and does not authorize endpoint
validation.

## Candidate construction

The base vector is the previously authorized observer-basis candidate:

```text
B_obs = W_path * sky_x * z_centered
```

The screen tests:

```text
B_obs
B_obs * void morphology proxies
B_obs * web morphology proxies
B_obs * line-of-sight environment proxies
B_obs * void geometry proxies
B_obs * a small set of predeclared mixed proxy products
```

All vectors are normalized on the same 12-object partial path scope.  Missing
line-of-sight environment values are filled only by the source-scope median before
centering; no endpoint residuals or fit statistics are used.

## Control policy

Each candidate family is compared with:

```text
off
wrong_sign
deterministic_shuffle
rank_reverse
```

The deterministic shuffle uses the same replay-compatible seed convention as the
authorized observer-basis screen.

## Claim boundary

Allowed conclusion:

```text
preauthorization diagnostic evidence that a particular source-frozen proxy
combination is worth separate reviewer authorization.
```

Forbidden conclusions:

```text
endpoint validation
population validation
physical lensing path weight proof
post-hoc path-kernel discovery
Tau Core cosmology confirmation
```

If a candidate survives this screen, it must still go through a separate reviewer
authorization package before any endpoint replay.

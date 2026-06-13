# Full-Kernel Proxy Component Audit v1

**Doc class:** post-screen component audit.
**Status:** diagnostic only; not endpoint replay; not validation.
**Canonical parent:** Paper 10 observer/path projection refinement notes.

## Purpose

The full-kernel-proxy fast screen showed that adding source-side void, web,
line-of-sight, and void-geometry multipliers does not automatically improve the
current observer-basis carrier.  This audit explains the result by grouping the
candidate families by component class and comparing them to the base carrier:

```text
W_path_x_sky_x_x_zcenter
```

## Result

No enriched proxy family outperforms the base observer-basis carrier.  The class
summary is:

```text
base observer-basis: survives controls and remains best
mixed web x LOS: survives local controls but is weaker than base
mixed void x web: close to base but fails controls
void geometry: baseline-improving but control-failed
line-of-sight environment: baseline-improving but control-failed
void morphology: weak/control-failed
web morphology: weak/control-failed
```

## Interpretation

The result is a useful constraint, not a validation failure. It says that the
available proxy factors are not yet the source-native variables needed for a
full Tau Core observer/path kernel. A stronger kernel should therefore be
derived from better path/environment/readout observables rather than obtained by
stacking all available proxy columns.

## Claim boundary

Allowed conclusion:

```text
extra proxy factors do not outperform the base observer-basis carrier in this
12-object diagnostic screen.
```

Forbidden conclusions:

```text
population validation
endpoint validation
physical lensing path proof
failure of observer/path projection as a Tau Core channel
```

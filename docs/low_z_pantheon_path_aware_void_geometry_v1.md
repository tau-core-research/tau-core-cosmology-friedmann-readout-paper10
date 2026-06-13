# Low-z Pantheon Path-Aware Void Geometry v1

**Doc class:** source-side path/void geometry observable.
**Status:** not scoring; not endpoint replay; not validation.
**Canonical parent:** full observer/path kernel source requirements.

## Purpose

The earlier void-geometry join recorded the nearest void to the source position.
That is useful, but it is not path-aware: it does not ask whether the
observer-to-source segment passes near or through a void.  This artifact
constructs a residual-blind path-aware geometry proxy.

## Frozen geometry rule

For each frozen low-z Pantheon row:

1. Use the observer at the origin of the low-z comoving proxy coordinates.
2. Build the observer-to-source segment.
3. For every source-native VoidFinder void, compute closest approach to that
   segment.
4. Select the void with minimal impact parameter to the segment.
5. Record:
   - closest-approach phase along the source segment;
   - impact parameter;
   - effective-radius crossing margin;
   - whether the segment intersects the effective void sphere;
   - entry/exit fractions when an intersection exists;
   - chord length and path-depth fraction.

## Current coverage

```text
low-z rows:                     424
path effective-void crossings:  180
partial path-scope rows:         12
partial path-scope crossings:    10
maximum path-depth fraction:      0.439054
```

## Interpretation

This is progress toward the R3 source requirement because void geometry is now
defined relative to the source-observer path, not only relative to the source
position.  It is still not a full metric/lensing path term. The geometry is a
low-z Euclidean proxy and does not include metric weighting, lensing convergence,
or a derived null-geodesic bundle integral.

## Claim boundary

Allowed:

```text
path-aware void geometry exists as a source-side low-z observable.
```

Forbidden:

```text
endpoint replay authorization
validation
physical lensing-path proof
full observer/path kernel claim
```

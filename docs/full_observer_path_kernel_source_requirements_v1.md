# Full Observer/Path Kernel Source Requirements v1

**Doc class:** source-grounding requirements gate.
**Status:** not scoring; not endpoint replay; not validation.
**Canonical parent:** Paper 10 observer/path projection refinement.

## Why this gate exists

The current observer-basis replay shows a narrow source-side signal, but the
full-kernel proxy bank shows that simply multiplying by all available void, web,
line-of-sight, and geometry proxies does not improve the result.  The next step
is therefore not more proxy stacking. It is source-native observable grounding.

The first partial source observables now cover R2, R3, and R4, while R5 and R6
have route/coverage audits:

- R2: a five-shell line-of-sight density profile from the SDSS DR17 MCPM
  catalogue.
- R3: a low-z observer-to-source segment/void crossing geometry observable.
- R4: a source-centered tangent-plane web dipole/quadrupole anisotropy proxy.
- R5: KiDS/CMB lensing source routes and KiDS tile coverage are recorded, but
  no source-aligned kappa, shear, mass-map integral, or physical lensing path
  weight is computed.
- R6: CC \(H(z)\), SDSS BAO/RSD, and CMB route families are present.  A
  source-side `Delta_clock_star` candidate is frozen from the CC median
  `errHz/Hz`, and a source-side CC redshift-bin support policy candidate is
  frozen.  A residual-blind uncertainty-channel `Delta_clock` candidate is also
  frozen from the assigned CC fractional uncertainty contrast.  A
  source-normalized `W_time` basis candidate is frozen, but it is not endpoint
  authorized and not validation.

These are still partial observables. They are not endpoint replay, not
validation, and not physical metric/lensing path claims.

## Required source observables

The full observer/path kernel needs at least:

1. Full sky direction and observer-frame basis.
2. A radial line-of-sight environment profile or integral.
3. Path-aware void geometry, not only nearest-void scalar proximity.
4. Directional web anisotropy projected along the source-observer direction.
5. Independent metric/lensing-path information before any physical path-weight
   claim.
6. Independent time/readout phase evidence and replay authorization before any
   \(W_{\rm time}\) scoring.

## Claim boundary

This gate does not authorize endpoint replay. It defines what must be
source-frozen before a future full observer/path kernel can be treated as more
than a reduced proxy. The current Paper 10 result remains:

```text
restricted observer/projection proxy survives a narrow permission-only replay;
full observer/path kernel remains future work.
```

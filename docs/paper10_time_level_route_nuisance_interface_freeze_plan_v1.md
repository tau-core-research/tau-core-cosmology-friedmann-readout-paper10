# Paper 10 time-level route nuisance/interface freeze plan v1

**Doc class:** source-side nuisance/interface freeze plan
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time/readout level-slope route split ledger

This plan freezes the current allowed use of the `time_level_route`.

The available source observable is SDSS radial BAO:

```text
D_H/r_d = c / (H(z) r_d)
```

Therefore `-log(DH_over_rd)` is an expansion-level / `logH`-like observable
only up to the unresolved sound-horizon nuisance \(r_d\). The current route may
use it only for two-point directional source-side alignment against nearest CC
`logH` support. It may not use it to claim an absolute \(H(z)\) scale, endpoint
replay, or validation.

Forbidden moves:

- fitting \(r_d\) from Pantheon residuals;
- claiming absolute `logH` without an \(r_d\) policy;
- using radial BAO as support for the CC `clock_slope` route;
- opening endpoint scoring from the two BAO radial points.

Required next source gate:

```text
freeze an external rd prior or rd-marginalization policy,
and expand radial BAO support before endpoint scoring.
```

# Paper 10 time/readout level-slope route split ledger v1

**Doc class:** source-side route split ledger
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time/readout route synthesis gate

This ledger separates two \(W_{\rm time}\) route candidates after the joint
CC+BAO audit:

- `time_level_route`: expansion-level / `logH`-like readout route;
- `time_slope_route`: clock-slope / `dlogH/dlog(1+z)` readout route.

The split is necessary because the radial BAO audit supplies an independent
expansion-level observable, but the joint audit shows that it does not currently
support the CC `clock_slope` route.

Current claim boundary:

```text
source-side route split only;
not endpoint replay;
not validation;
not a Tau Core time-projection proof.
```

Operational consequences:

- the level route has independent BAO support but remains two-point
  underresolved and \(r_d\)-blocked;
- the slope route has a CC candidate signal but remains blocked by global
  controls and reviewer authorization;
- neither route may be used for endpoint scoring until its blockers are closed
  under a frozen nuisance/interface policy.

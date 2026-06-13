# Paper10 DESI Row-4 Window Review v1

**Doc class:** external source-side review package description
**Reader role:** external reviewer without repository access
**Status:** blank review handoff; not replay; not validation
**Canonical parent:** `README.md`

This package asks a narrow source-side question:

> Should the DESI row-4 cosmic-clock support window remain strictly
> `|Delta z| <= 0.10`, or may the nearest non-Simon chronometer point
> `Moresco 2015, z=1.363, H=160+/-33.6 km/s/Mpc` be accepted as caveated
> near-window source context for `z_eff=1.484`?

The package exists because the strict search found:

- Simon et al. (2005) points at `z=1.43` and `z=1.53`, inside the row-4 window
  but not independent of the existing Simon-family blocker.
- Moresco (2015) at `z=1.363`, independent of Simon but outside the frozen
  `|Delta z| <= 0.10` window by `0.021`.
- Tomasetti et al. (2023) at `z=1.26`, independent but clearly outside the
  row-4 window.

Reviewer task:

1. Decide whether the strict window should remain unchanged.
2. Decide whether the Moresco (2015) near-miss may be retained as caveated
   source-side row-4 support.
3. State the maximum allowed consequence.

Claim boundary:

- the package contains no endpoint residuals, endpoint scores, or fit
  statistics;
- it does not authorize endpoint replay;
- it does not claim validation;
- it does not claim physical validation;
- any future endpoint replay would require a separate replay-authorization
  package after the source-window decision is frozen.

Preferred conservative outcome:

`KEEP_STRICT_WINDOW` or `RETAIN_AS_CONTEXT_ONLY` keeps row 4 blocked.

Most permissive allowed outcome in this package:

`SOURCE_REOPEN_ONLY_NO_REPLAY`.

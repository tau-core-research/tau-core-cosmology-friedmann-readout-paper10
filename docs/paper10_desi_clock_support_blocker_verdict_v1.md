# DESI Clock-Support Blocker Verdict v1

This source-side verdict closes the current DESI clock-support search loop. It
does not authorize endpoint replay and does not claim validation.

The preceding acquisition manifest froze two targets, and the candidate scan
found useful context/cross-probe sources but no gate-closing independent clock
support. Therefore the DESI time-readout route remains blocked.

## Active Blockers

1. `ROW4_INDEPENDENT_CLOCK_REDUNDANCY_MISSING`

   Row 4 at `z_eff=1.484` has relaxed-window support only from Simon et al.
   (2005). The nearby eBOSS QSO BAO/RSD route at `z_eff=1.48` is retained as a
   cross-probe control, not as clock support.

2. `ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING`

   Row 5 at `z_eff=2.33` has Ly-alpha BAO support, but not independent
   clock/time-readout support. The frozen cosmic-chronometer table ends at
   `z=1.965`, so extrapolation remains forbidden.

## Reopen Conditions

The route can only be reopened if one of these source-side conditions is met
before replay:

- an independent CC/clock source near `z=1.484` is frozen for row 4; or
- an independent high-z clock/source-native time-readout route covers or
  brackets `z=2.33` without extrapolation.

Until then, replay and validation language remain disallowed.

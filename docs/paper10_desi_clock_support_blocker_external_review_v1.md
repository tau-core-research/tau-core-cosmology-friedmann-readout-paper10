# DESI clock-support blocker external review package v1

**Doc class:** external source-acquisition review handoff.
**Reader role:** independent reviewer without repository access.
**Status:** blank review package; not endpoint replay; not validation.
**Canonical parent:** Paper10 DESI time-readout source-side blocker chain.

## Purpose

This package asks an external reviewer to inspect two active source-side
blockers in the DESI clock/time-readout route:

1. radial row 4 at `z_eff=1.484`, where the current relaxed-window clock support
   is not independent enough;
2. radial row 5 at `z_eff=2.33`, where Ly-alpha BAO exists but independent
   clock/source-native time-readout support has not been frozen.

The review must remain source-side. It must not use endpoint residuals,
endpoint scores, late-time fit parameters, or any post-hoc clock smoothing.

## What the reviewer should decide

The reviewer should fill:

```text
data/derived/paper10_desi_clock_support_blocker_external_review_response_template_v1.csv
```

The four questions are:

- whether row 4 has an independent clock/chronometer or source-native
  time-readout source near `z=1.484`;
- whether row 5 has independent high-redshift clock/source-native time-readout
  support covering or bracketing `z=2.33` without extrapolation;
- whether BAO/RSD and Ly-alpha BAO sources should remain cross-probe/context
  controls unless independent clock evidence is attached;
- whether the review used only source-side literature evidence and did not
  authorize endpoint replay.

## Claim boundary

This package cannot authorize replay and cannot claim validation. A completed
positive response would only reopen a source-acquisition gate. A separate
replay authorization package would still be required before endpoint scoring.

Claim boundary:

```text
paper10_desi_clock_support_blocker_external_review_not_validation
```

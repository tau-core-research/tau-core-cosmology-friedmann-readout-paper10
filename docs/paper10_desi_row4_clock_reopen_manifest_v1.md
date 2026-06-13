# DESI row-4 clock acquisition reopen manifest v1

**Doc class:** source-acquisition reopen manifest.
**Reader role:** Paper10 DESI clock/time-readout source-side audit.
**Status:** row-4 acquisition reopened; not replay; not validation.
**Canonical parent:** DESI clock-support blocker external review.

## Purpose

The completed external source-side review partially reopens the DESI row-4 clock
support gate only. The reviewer reported independent cosmic-chronometer support
bracketing the target `z_eff=1.484` at:

- `z=1.43`;
- `z=1.53`.

This is enough to reopen source acquisition for row 4. It is not enough to
authorize endpoint replay.

## Boundary

Row 5 at `z=2.33` remains blocked. BAO/RSD and Ly-alpha BAO remain
cross-probe/context controls unless independent clock or source-native
time-readout evidence is attached.

The next admissible action is to cache/freeze the source-native row-4 bracket
entries, including values, uncertainties, reference provenance, and covariance
status where available.

Claim boundary:

```text
paper10_desi_row4_clock_reopen_manifest_not_validation
```

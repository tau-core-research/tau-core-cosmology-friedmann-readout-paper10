# Low-z Pantheon time/readout clock-rate phase candidate v1

**Doc class:** source-side time/readout candidate
**Status:** source-frozen candidate, not replay, not validation
**Canonical parent:** Paper 10 R6 time/readout source audit

This artifact replaces the previous uncertainty-only `W_time` stress proxy with
a more direct source-native clock/readout candidate from the fetched cosmic
chronometer `H(z)` table.

It freezes three residual-blind source-side columns for each low-z Pantheon+
row:

- `W_time_clock_level_basis`: assigned CC `log H(z)` level, source-normalized;
- `W_time_clock_slope_basis`: finite-difference `d log H / d log(1+z)` around
  the assigned CC support bin, source-normalized;
- `W_time_clock_phase_basis`: normalized product of the level and slope bases.

The artifact does not smooth `H(z)` using endpoint residuals, does not select
clock anomalies, does not authorize replay, and does not claim validation.

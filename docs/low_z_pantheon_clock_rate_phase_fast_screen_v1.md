# Low-z Pantheon clock-rate phase fast screen v1

**Doc class:** preauthorization diagnostic fast screen
**Status:** source-frozen, not replay, not validation
**Canonical parent:** Paper 10 R6 time/readout source audit

This screen tests three source-frozen `W_time` families built from cosmic
chronometer `H(z)` values:

- `clock_level`: assigned CC `log H(z)` level;
- `clock_slope`: finite-difference `d log H / d log(1+z)`;
- `clock_phase`: normalized product of level and slope bases.

The screen exists only to decide whether a stronger `W_time` family is worth a
later reviewer-gated authorization package. It is not endpoint replay and not
validation.

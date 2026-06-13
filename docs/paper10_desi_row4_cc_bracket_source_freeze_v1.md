# DESI row-4 CC bracket source freeze v1

**Doc class:** source-native clock-value freeze and independence audit.
**Reader role:** Paper10 DESI time-readout source-side gate.
**Status:** values frozen; independence blocker not released; not replay; not validation.
**Canonical parent:** DESI row-4 clock acquisition reopen manifest.

## Frozen source values

The reviewer-reported bracket around DESI row 4 (`z_eff=1.484`) is now frozen as:

| z | H(z) | sigma_H | method | source family |
|---|---:|---:|---|---|
| 1.43 | 177 | 18 | full-spectrum fitting | Simon et al. (2005) |
| 1.53 | 140 | 14 | full-spectrum fitting | Simon et al. (2005) |

The values are taken from the compiled cosmic-chronometer table summarized by
Moresco, where both entries are attributed to Simon, Verde & Jimenez (2005).

## Gate implication

This freeze improves the explicit row-4 source record, but it does not release
the original independence blocker. The prior blocker required independent clock
or source-native time-readout support near `z=1.484` **not reusing** the current
Simon et al. reference family. These two bracket entries are source-native CC
values, but they reuse that reference family.

Therefore:

- row 4 has frozen bracket values;
- row 4 still does not have independent reference-family redundancy;
- row 4 cannot enter endpoint replay from this freeze alone;
- row 5 remains blocked.

Claim boundary:

```text
paper10_desi_row4_cc_bracket_source_freeze_not_validation
```

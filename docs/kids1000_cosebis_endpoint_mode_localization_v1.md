# KiDS-1000 COSEBIs Endpoint Mode Localization v1

This post-score localization audit follows the jackknife result. The
jackknife shows that the endpoint score is not carried by a single source bin
or tomographic pair, but it remains mode-band dependent. This audit therefore
scores predeclared single-mode, cumulative-low-mode, and low-mode-removal
subsets without changing the source-frozen theory vector.

The frozen subsets are:

- `single_mode_1` through `single_mode_20`;
- `cumulative_low_modes_1_to_m` for `m = 1,...,20`;
- `without_low_modes_1_to_m` for `m = 1,...,19`.

Current result:

- total subsets: `59`;
- single modes with negative Delta chi-square: `9/20`;
- single modes with negative Delta AIC: `6/20`;
- cumulative-low subsets with negative Delta chi-square: `20/20`;
- low-removal subsets with negative Delta chi-square: `4/19`;
- best single-mode subset: `single_mode_1`, Delta chi-square
  `-101.5735188246`;
- best cumulative-low subset: `cumulative_low_modes_1_to_3`, Delta chi-square
  `-237.1074068478`;
- first non-improving low-removal subset: `without_low_modes_1_to_5`, Delta
  chi-square `0.0`;
- localization verdict: `low_modes_1_to_5_dominate_endpoint_signal`.

Interpretation boundary:

The endpoint signal is not single-bin or single-pair localized, but it is
strongly low-mode localized. In this COSEBIs implementation, the candidate
signal is carried mainly by the lowest angular/mode structure: modes `1-3`
give the strongest cumulative score, modes `1-5` carry the broad low-band
signal, and removing modes `1-5` removes the improvement. This is a useful
diagnostic, not validation. The next scientific question is whether the
source-frozen Tau readout shell has a source-side reason to predict low-mode
dominance, and whether this survives against external lensing covariance,
scale-cut, and mock tests.

Claim boundary:

```text
kids1000_cosebis_endpoint_mode_localization_not_validation
```

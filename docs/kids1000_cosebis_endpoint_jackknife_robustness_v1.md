# KiDS-1000 COSEBIs Endpoint Jackknife Robustness v1

This post-score robustness audit asks whether the endpoint candidate signal is
localized to a single source bin, a single tomographic pair, or a narrow COSEBIs
mode band. It does not alter the source-frozen theory vector and does not
select or retune channels.

The frozen masks are:

- `leave_one_source_bin`: remove every row touching one selected source bin;
- `leave_one_tomographic_pair`: remove one of the 15 tomographic pairs;
- `mode_band`: score only low `1-5`, mid `6-10`, or high `11-20` modes;
- `complement_mode_band`: remove one of the same three mode bands.

Current result:

- total subsets: `27`;
- leave-one source-bin/pair subsets: `20`;
- leave-one subsets with negative Delta chi-square: `20/20`;
- leave-one subsets with negative Delta AIC: `20/20`;
- mode-band subsets with negative Delta chi-square: `2/3`;
- mode-band subsets with negative Delta AIC: `2/3`;
- full-reference Delta chi-square: `-183.6152665217`;
- best subset: `leave_source_bin_1`, Delta chi-square `-199.2701034089`;
- weakest subset: `without_mode_band_low_1_5`, Delta chi-square `0.0`;
- localization verdict: `not_single_source_bin_or_pair_under_leave_one_chi2`.

Interpretation boundary:

The leave-one result argues against the endpoint score being carried by a
single source bin or single tomographic pair under this first jackknife. The
mode-band result is more caveated: the high-only subset and the low-removed
subset do not improve over the zero baseline after the same nonnegative
single-amplitude refit. The claim-safe reading is therefore that the signal is
not a single-bin/pair artifact, but it remains mode-structure dependent and is
not a KiDS validation claim.

Claim boundary:

```text
kids1000_cosebis_endpoint_jackknife_robustness_not_validation
```

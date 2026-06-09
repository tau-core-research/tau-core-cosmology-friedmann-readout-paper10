# KiDS-1000 COSEBIs Tomographic Control Plausibility Audit V1

**Doc class:** post-score control plausibility audit  
**Reader role:** reviewer-facing explanation of better tomographic controls  
**Status:** diagnostic audit; not validation and not a physical alternative  
**Canonical parent:** `README.md`

## Purpose

The first KiDS COSEBIs endpoint score is low-tail but not an absolute winner:
some tomographic controls score better than the source-frozen candidate. This
audit asks whether those better controls should be interpreted as physical
alternatives or as evidence that the current tomographic source-bin mapping is
too coarse.

## Method

The audit reads the top 25 tomographic controls from the committed
tomographic-structure robustness run and the source-side redshift kernel
inventory. It computes only interpretive geometry diagnostics:

- whether a mapping is a global source-bin relabeling,
- how many tomographic pairs are changed,
- whether auto/cross pair type is preserved,
- the mean and maximum shift in pair mean redshift,
- the mean shift in pair redshift separation.

It does not compute new scores, retune amplitudes, or select a new endpoint
candidate.

## Result

The better controls fall into two classes:

1. non-global auto/cross-preserving pair shuffles, which preserve pair type but
   break the source-bin ordering geometry;
2. one adjacent global bin-label permutation, which could only become a
   physical source-systematic candidate if independently supported by
   photometric-redshift or tomographic calibration evidence.

No better control is accepted as a physical alternative in the current source
state.

## Verdict

`better_tomographic_controls_are_control_only_or_source_systematic_candidates_not_physical_alternatives`

Thus the controls do not refute the endpoint signal, but they do block a
validation claim. The next clean step is an independent photometric-redshift or
tomographic-calibration holdout before promoting any tomographic alternative.

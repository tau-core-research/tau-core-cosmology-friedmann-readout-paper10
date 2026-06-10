# Void Source-Basis Refinement R4 Independence Preflight v1

**Doc class:** source-side preflight audit  
**Status:** redshift/source-row independence preflight; not scoring; not validation

This artifact audits whether the R1-R3 source-side void-refinement features are
mostly redshift or source-row-index proxies. It does not compute endpoint
scores, authorize replay, tune amplitudes, or claim physical validation.

## Tested features

The preflight checks:

- nearest void center distance;
- nearest void wall distance;
- angular separation to nearest void center;
- inside/outside nearest effective void radius;
- line-of-sight environment count;
- line-of-sight median matter density;
- nearest line-of-sight environment density.

Each feature is correlated against `zHD` and `source_row_index` using both
Pearson and Spearman correlations. A feature is marked low-correlation only if
all absolute correlations are at or below `0.30`.

## Current interpretation

Distance-like void features remain moderately redshift-correlated, while
angular, inside/outside, and line-of-sight environment features provide lower
correlation candidates. This is a source-side preflight result only: it does not
select a final refined basis and does not reopen an endpoint.

## Remaining gates

R5 control-resistance preflight and R6 independent leakage review are still
required before any replay request.

## Claim boundary

```text
r4_independence_preflight_not_scoring_not_validation
```

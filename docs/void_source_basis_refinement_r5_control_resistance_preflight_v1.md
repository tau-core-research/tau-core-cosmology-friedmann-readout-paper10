# Void Source-Basis Refinement R5 Control-Resistance Preflight v1

**Doc class:** source-side control preflight  
**Status:** control families frozen; not scoring; not validation

This artifact freezes a control-resistance suite for the R4 source-side void
features that passed the redshift/source-row independence preflight. It does not
compute endpoint scores, authorize replay, tune amplitudes, or claim physical
validation.

## Admitted source features

R5 admits only the R4 low-correlation features. In the current run these are:

- angular separation to the nearest void center;
- inside/outside nearest effective void radius;
- line-of-sight environment count;
- line-of-sight median matter density;
- nearest line-of-sight environment density.

The distance-like nearest-void-center and wall-distance features remain excluded
from this R5 control suite because R4 marked them as moderately redshift
correlated.

## Frozen control families

For each admitted feature, R5 freezes five source-side controls:

- `zero_control`: set the normalized source feature to zero;
- `wrong_sign_control`: flip the normalized source feature sign;
- `deterministic_row_shuffle_control`: permute the normalized source feature
  with a frozen seed;
- `threshold_low_control`: source-frozen lower-quartile binary indicator;
- `threshold_high_control`: source-frozen upper-quartile binary indicator.

Missing line-of-sight density values are mapped to zero in the normalized
control-vector shell. This is a preflight encoding choice, not a physical claim.

## Artifacts

```text
data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1.csv
data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv
data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv
```

The control manifest records the frozen rules. The vector artifact records the
candidate source vector and its controls for each low-z Pantheon row and each
admitted feature.

## Remaining gates

R6 independent leakage review remains required before any new void replay
request. R5 alone does not make the refined void basis source-unique,
endpoint-ready, or physically validated.

## Claim boundary

```text
r5_control_resistance_preflight_not_scoring_not_validation
```

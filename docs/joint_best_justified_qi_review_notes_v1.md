# Joint best-justified Q_i review notes v1

## Decision

`QI_REVIEW_ACCEPTED_OR_CAVEATED_SOURCE_SIDE_NOT_VALIDATION`

## Scope

This is a source-side review of the Paper10 best-justified joint-kernel support factors `Q_i`.
It does not compute a new endpoint score, does not authorize endpoint replay, and does not claim endpoint or cosmological validation.

## Row-level review

- `QI_REVIEW_01_SOURCE_GATES`: accepted with caveats. Gate entries are defensible as source-side protocol support factors, not physical amplitudes or likelihood weights.
- `QI_REVIEW_02_KIDS_COSEBIS`: accepted with caveats. Positive support is defensible, but tomographic/operator-level blockers remain.
- `QI_REVIEW_03_OBSERVER_PATH`: accepted with caveats. Support remains narrow and limited to the frozen 12-object permission-replay route.
- `QI_REVIEW_04_DESI_SHAPE`: accepted with caveats. Source/readout support is defensible, but the small row-sensitive margin remains explicit.
- `QI_REVIEW_05_ZERO_SUPPORT_BRANCHES`: accepted source-side. ACT Kpath, void/web, time basis, distance shell, and sky-z remain correctly excluded from positive joint support under the current ledgers.
- `QI_REVIEW_06_EXPONENT_POLICY`: accepted with caveats. Equal `alpha_a=1/7` is acceptable as a frozen preflight default, but a validation-facing endpoint needs a separately frozen source-reviewed exponent policy.
- `QI_REVIEW_07_PROMOTION_RULE`: accepted source-side. No validation-facing promotion is allowed before a separate covariance-aware joint likelihood or likelihood surrogate exists.

## Claim boundary

`qi_review_response_source_side_only_not_scoring`

## Guard flags

```text
forbidden_inputs_used=false
endpoint_scores_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
```

## Next gate

A separate covariance-aware joint likelihood prototype with shuffled-channel, wrong-channel, sign-flip, block-drop, and null/readout controls remains required before any validation-facing interpretation.

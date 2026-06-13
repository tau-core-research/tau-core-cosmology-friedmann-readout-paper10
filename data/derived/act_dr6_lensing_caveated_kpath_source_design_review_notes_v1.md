# ACT DR6 caveated K_path source-design review notes v1

## Decision

`ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY`

## Scope

This review accepts the ACT DR6 baseline kappa source object only as a caveated, dimensionless, source-side `K_path` shape proxy design for a later separate permission-only replay review.

It does not authorize endpoint replay, endpoint validation, physical lensing-path weight promotion, dark-sector inference, or any current-branch family verdict.

## Accepted source-side elements

- `ACT_DR6_baseline_kappa_alm_with_mask_and_null_variants` can be carried as a caveated source product.
- The median/MAD normalization can be carried only as a dimensionless shape proxy.
- Partial coverage is explicit: 424 source rows, 168 ACT mask-positive rows, and outside-mask rows receive zero source weight.
- Curl and `f150-f090` frequency-difference products must remain `K_null` controls.

## Required caveats

The current ACT branch remains quarantined / control-dominated. The included replay summary indicates that the candidate is not control-resistant; therefore this review cannot be read as validation or evidence of a physical lensing-path signal.

## Boundaries retained

```text
forbidden_inputs_used=false
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
dark_sector_inference_allowed=false
```

## Completion check

`pass`

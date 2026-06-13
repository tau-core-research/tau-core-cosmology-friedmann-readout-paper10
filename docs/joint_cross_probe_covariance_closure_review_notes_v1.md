# Joint cross-probe covariance closure review notes v1

## Decision

`JOINT_BLOCK_DIAGONAL_INDEPENDENCE_PRECONDITION_CAVEATED_CLOSED_NOT_SCORING`

## Closure route

`caveated_block_diagonal_independence`

## Reviewer interpretation

The package does not provide a source-native/source-frozen cross-probe covariance product, so the covariance-product route remains unavailable.

The package does, however, support a caveated block-diagonal independence precondition for a later, separately-authorized scoring/replay package. This relies only on source-side package contents: frozen active block scopes, existing within-block covariance/statistic shells, and the prior block-diagonal protocol shell. It does not use endpoint residuals, new endpoint scores, fit improvements, posterior chains, or post-score control ranks.

## Mandatory caveats to carry forward

- Shared cosmological parameters may correlate all blocks.
- Shared sky/mask and line-of-sight overlap are not captured by a cross-probe covariance product.
- Redshift/kernel overlap is not converted into a full covariance model.
- Nuisance/calibration/photo-z/distance-ladder/BAO/lensing correlations are not jointly marginalized.
- There is no population-level cross-probe covariance product.
- Any block-diagonal use must remain caveated and limited to a later separately-authorized protocol.

## Boundary

```text
forbidden_inputs_used=false
cross_probe_covariance_product_available=false
block_diagonal_independence_source_justified=true
future_scoring_precondition_closure_allowed=true
separate_scoring_authorization_required=true
hard_blocker_remains_open=false
endpoint_scoring_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
```

This is not scoring, not endpoint validation, and not cosmological validation.

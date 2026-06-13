# Reviewer handoff: Joint cross-probe covariance closure v1

You do not need repository access to complete this review.

## Task

Review whether Paper10's joint route can close the outstanding
cross-probe covariance / independence blocker across these active blocks:

- KiDS/COSEBIs low-mode lensing
- observer/path low-z
- DESI shape/readout

This is a source-side review only. It is not endpoint scoring, not
endpoint validation, and not cosmological validation.

## Fill this file

`data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv`

For every row, set `review_completed=true`, provide
`reviewer_id_or_role`, `reviewer_response`, and `reviewer_rationale`.
If you accept either a covariance-product route or an independence route,
also provide `source_reference_or_url`.

## Forbidden inputs

Do not use endpoint residuals, new endpoint scores, fit improvements,
posterior chains, or post-score control ranks. Keep
`forbidden_inputs_used=false` unless this rule was violated.

## Safe outcomes

The allowed outcomes are:

1. keep the blocker open;
2. identify a source-native/source-frozen cross-probe covariance product;
3. accept a caveated block-diagonal independence precondition.

Even outcomes 2 or 3 do not authorize scoring. A separate scoring
authorization package is required later.

## Current package checksum

- review package zip sha256: `685d8e5fdbc606b07a687919ef80b31eb1d622899e7006da8e790eaa2a51ea11`

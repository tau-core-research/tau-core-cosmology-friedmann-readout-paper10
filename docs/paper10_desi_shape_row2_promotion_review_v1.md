# Paper10 DESI shape row2 promotion review v1

**Doc class:** external source-side promotion review package guide
**Reader role:** independent reviewer without repository access
**Status:** promotion-review handoff only, not replay, not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This package asks whether Row2 has enough source-side support to prepare a
separate future replay-authorization package.

It does not ask the reviewer to approve endpoint replay, endpoint validation,
physical validation, or route success. The strongest allowed positive outcome is
permission to prepare a separate replay-authorization review.

Reviewed status:

```text
Moresco2012 caveat reduced: true
Source-native DESI BAO shape caveat reduced: true
Row2 source caveat reduced: true
Endpoint-pair independence satisfied: false
Row2 promotion ready: false
Endpoint replay allowed: false
```

Allowed response strings:

```text
Q1_COMBINED_SOURCE_STATUS:
  accept_combined_source_caveat_reduction
  reject
  needs_more_context

Q2_ENDPOINT_PAIR_INDEPENDENCE_BLOCKER:
  accept_blocker_remains
  reject

Q3_PROMOTION_SCOPE:
  accept_prepare_separate_replay_authorization_review
  no_promotion
  needs_more_context

Q4_CLAIM_BOUNDARY:
  accept
```

Return instruction:

Fill `data/derived/paper10_desi_shape_row2_promotion_review_response_template_v1.csv`,
set `review_completed=true` on all rows, keep every replay/validation flag
false, and return the filled CSV in a ZIP. Do not rename the CSV unless the
returned name is `paper10_desi_shape_row2_promotion_review_response_v1.csv`.

Forbidden inputs:

- endpoint residuals,
- endpoint scores,
- fit statistics,
- posterior chains,
- post-hoc shape selection,
- validation language.

Claim boundary:

```text
paper10_desi_shape_row2_promotion_review_not_replay_not_validation
```

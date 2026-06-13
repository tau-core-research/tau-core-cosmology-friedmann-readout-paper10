# Paper10 DESI shape row2 source-native shape-support review v1

**Doc class:** external source-side review package guide
**Reader role:** independent reviewer without repository access
**Status:** source-side review only, not replay, not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This review package asks whether the frozen source-native DESI DR2 BAO shape
information for shape row 2 may be retained as caveat-reducing source-side
support.

The package does not ask the reviewer to approve endpoint replay, endpoint
validation, physical validation, or shape-route promotion. The strongest allowed
positive decision is that the attached source-native DESI BAO vector is valid
source context for the row-2 interval.

The reviewed object is:

```text
row-2 interval: z=0.934--1.321
source rows: DM/rs and DH/rs at both endpoints
shape vector:
  delta_log_DM_over_rs = 0.246281910984
  delta_log_DH_over_rs = -0.218701863111
  delta_log_anisotropy_DM_over_DH = 0.464983774095
```

Reviewer task:

1. Confirm whether the DESI BAO row identities and values are correctly copied.
2. Confirm whether the covariance subblock is source-native and usable as
   source-side shape context.
3. Decide whether the shape vector may reduce the row-2 source caveat.
4. Keep all replay and validation flags false.

Allowed response strings:

```text
Q1_SOURCE_IDENTITY:
  accept
  accept_source_identity
  reject
  needs_more_context

Q2_COVARIANCE_STATUS:
  accept
  accept_covariance_context
  reject
  needs_more_context

Q3_SHAPE_VECTOR_STATUS:
  accept
  accept_as_caveat_reducing_source_support
  reject
  needs_more_context

Q4_NEXT_GATE:
  accept_source_context_only
  needs_separate_promotion_review
  needs_more_context
```

Return instruction:

Fill `data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_template_v1.csv`,
set `review_completed=true` on all rows, keep every replay/validation flag
false, and return the filled CSV in a ZIP. Do not rename the CSV unless the
returned name is
`paper10_desi_shape_row2_source_native_shape_support_review_response_v1.csv`.

Forbidden inputs:

- endpoint residuals,
- endpoint scores,
- fit statistics,
- posterior chains,
- post-hoc kernel performance,
- any instruction to promote the row to endpoint-ready status.

Claim boundary:

```text
paper10_desi_shape_row2_source_native_shape_support_review_not_validation
```

# Paper10 DESI Shape Row2 Replay Authorization Review v1

**Doc class:** external reviewer handoff
**Reader role:** external reviewer without repository access
**Status:** authorization review only; not endpoint validation
**Canonical parent:** Paper10 DESI shape-route Row2 gate ledger

This package asks a narrow question:

```text
May the frozen Row2 DESI shape-route candidate/control setup be replayed once,
as a permission-only diagnostic step, despite Row2 still being non-promotion-ready?
```

It does not ask the reviewer to accept a physical result. It does not contain
endpoint residuals, endpoint scores, fit statistics, or a replay output. A
positive response only authorizes a later Row2 replay run under the frozen
candidate/control setup.

## Current source-side state

The Row2 chain has two caveat-reducing source-side reviews:

- Moresco2012 source attachment: accepted as caveat-reducing context.
- DESI DR2 source-native BAO shape support: accepted as caveat-reducing context.

The completed promotion review then allowed preparing a separate replay
authorization review, but it explicitly did not authorize direct replay or
validation.

The unresolved blocker is also retained:

```text
endpoint_pair_independence_satisfied=false
row2_promotion_ready=false
shape_route_promotion_allowed=false
```

## Reviewer task

Fill the response template:

```text
data/derived/paper10_desi_shape_row2_replay_authorization_review_response_template_v1.csv
```

Use only the source-side artifacts in this package. Do not use endpoint
residuals, endpoint scores, fit statistics, or post-hoc route performance.

## Allowed positive outcome

The strongest allowed positive outcome is:

```text
authorize_row2_permission_only_replay
```

This means only:

```text
one narrow Row2 replay may be run later under the frozen candidate/control setup
```

It still means:

```text
endpoint_validation_claimed=false
physical_validation_claimed=false
route_success_claimed=false
```

## Claim boundary

```text
paper10_desi_shape_row2_replay_authorization_review_not_validation
```

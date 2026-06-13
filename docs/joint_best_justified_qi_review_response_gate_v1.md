# Joint best-justified Q_i review response gate v1

Status: `SOURCE_SIDE_RESPONSE_GATE_NOT_SCORING`

This gate validates a completed external response to the
`joint_best_justified_qi_review_package_v1` handoff. It does not compute a new
joint score, does not authorize endpoint replay, and does not promote the
current best-justified joint kernel to cosmological validation.

## Purpose

The current best-justified joint kernel uses protocol support scores

```text
Q_i = product_a (g_i^a)^(1/7)
```

The response gate asks whether those support factors are source-side defensible
under the already frozen evidence ledgers. It is a review of source discipline,
not a likelihood fit.

## Allowed reviewer responses

Each requirement may be answered with one of:

```text
accept_source_side
accept_with_caveats_source_side
reject
needs_more_context
```

Blank responses are allowed only in the uncompleted template artifact.

## Forbidden inputs

The response remains invalid if it uses endpoint residuals, fit improvements,
posterior chains, or post-score control ranks. Every response row must keep:

```text
forbidden_inputs_used=false
endpoint_scores_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
```

## Claim boundary

A positive completed response can only say that the `Q_i` factors are
source-side accepted or caveated for future gate preparation. It cannot claim a
joint endpoint, a physical cosmological validation, or a dark-energy
explanation. A separate covariance-aware joint likelihood prototype remains the
next validation-facing step.

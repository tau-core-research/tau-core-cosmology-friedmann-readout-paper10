# DESI Shape Route Source-Synthesis Review

**Doc class:** source-side reviewer handoff
**Reader role:** independent reviewer without repository access
**Status:** package template; not completed
**Canonical parent:** Paper10 DESI shape-route source-support chain

## Purpose

This package asks a narrow source-side question: after the Row1 confirmatory
source review and the Row2 caveat-reduction reviews, is the DESI shape route
source-strengthened enough to justify preparing a later, separate
validation-oriented gate?

The package does **not** ask whether the Tau Core candidate is validated.  It
does **not** authorize another replay.  It does **not** claim endpoint
validation, physical validation, or a physical discovery result.

## Source-side state to review

- Rows `1;2` are the core rows identified by the frozen row-sensitivity audit.
- Row1 is the most required row and has confirmatory independent in-interval
  source support externally accepted.
- Row2 is caveat-reduced but not endpoint-ready or promotion-ready.
- The isolated Row2-only permission replay is negative against local controls,
  so Row2 alone is not the full route carrier.
- The allowed route-level interpretation is a multi-row, narrow-margin,
  source-sensitive signal, not Row2-only evidence.

## Forbidden inputs

The reviewer must not use endpoint residuals, endpoint fit statistics,
post-score tuning, or new endpoint scoring information.  The review is limited
to source provenance, row-support logic, caveat status, and claim-boundary
consistency.

## Allowed outcomes

The strongest allowed positive outcome is:

```text
ACCEPT_AS_SOURCE_SYNTHESIS_SUPPORT_FOR_FUTURE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION
```

Even this outcome keeps:

```text
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_validation_claimed=false
shape_route_promotion_allowed=false
```

If the reviewer finds that the source state remains too weak, the response
should list the blockers and keep the route in source-acquisition mode.

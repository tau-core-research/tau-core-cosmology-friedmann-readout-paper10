# Void Channel Remediation Gate v1

## Status

This is a decision gate after the void source-basis audit. It is not endpoint
scoring and does not claim physical validation.

## Parent blocker

The current void source basis is a low-redshift, volume-limited catalogue mapped
onto the full Pantheon distance block:

- parent audit: `VOID_SOURCE_BASIS_AUDIT_V1`
- source-basis limitation:
  `low_z_volume_limited_void_catalog_mapped_to_full_pantheon_distance_block`
- void support proxy: below `z ~= 0.109`
- Pantheon scope: extends above `z = 2`
- void-active fraction: about `0.311`

This explains why the authorized combined void/web endpoint suppressed the void
channel and collapsed to the web-only branch.

## Gate verdict

`ENDPOINT_REOPEN_BLOCKED`

The full-Pantheon void endpoint remains blocked. A new void endpoint may not be
opened from the current source basis.

## Allowed future routes

This gate freezes only the allowed remediation routes:

1. `LOW_Z_PANTHEON_SCOPE_REPLAY_CANDIDATE_NOT_RUN`

   Predeclare a low-redshift Pantheon subset matched to the void catalogue
   support. This would be a new candidate scope and would still require its own
   authorization before endpoint scoring.

2. `FULL_SCOPE_VOID_SOURCE_REBUILD_REQUIRED`

   Acquire and freeze a void/environment source basis whose support matches the
   intended full distance block before any full-Pantheon combined endpoint is
   reopened.

3. `VOID_CHANNEL_QUARANTINE_FROM_FULL_DISTANCE_ENDPOINT`

   Keep the void channel out of the full-distance likelihood until a matched
   support rule exists.

No route is selected by this gate.

## Claim boundary

This artifact records a remediation decision, not a result:

`void_channel_remediation_gate_not_scoring_not_validation`

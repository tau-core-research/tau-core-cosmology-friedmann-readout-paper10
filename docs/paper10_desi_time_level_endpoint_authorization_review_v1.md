# DESI Time-Level Endpoint Authorization Review V1

**Doc class:** endpoint replay authorization handoff.

**Reader role:** external reviewer without repository access.

**Status:** authorization template/package; not completed; not scoring; not validation.

**Canonical parent:** `paper10_time_level_route_external_rd_readiness_gate_v1.md`.

This handoff follows the source-side readiness gate
`PAPER10_TIME_LEVEL_ROUTE_EXTERNAL_RD_READINESS_GATE_V1`. Its purpose is to ask
whether one separate, permission-only DESI/CC five-row time-level replay may
later be prepared.

It does not run the replay, compute endpoint scores, claim endpoint validation,
or claim physical validation.

## Required Precondition

The source-side readiness gate must have:

```text
verdict=desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing
desi_dr2_first_cc_matched_endpoint_rows=5
desi_time_level_control_family_count=7
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_validation_claimed=false
```

The older two-point SDSS-only BAO signal is retained as a diagnostic, not as an
active blocker for this DESI route.

## Proposed Authorization Scope

The proposed authorization scope is limited to:

- the five DESI DR2 radial `DH_over_rs` rows that are matched within frozen
  cosmic-chronometer support;
- the excluded `z=2.33` DESI Ly-alpha row retained only as high-z holdout or
  future independent-clock support;
- the frozen external Planck2018 `r_d` source and the frozen
  `r_d`-marginalization interface;
- the seven frozen control families with deterministic seeds `41001`--`41007`;
- no endpoint residuals, endpoint scores, late-time fitted parameters, posterior
  chains, post-hoc smoothing, post-hoc clock anomaly labels, or post-hoc
  row/control selection in the authorization decision.

## Reviewer Decision

The reviewer is asked only whether a permission-only five-row DESI/CC
time-level replay may be prepared later. Acceptance does not imply validation.

## Claim Boundary

```text
paper10_desi_time_level_endpoint_authorization_review_not_validation
```

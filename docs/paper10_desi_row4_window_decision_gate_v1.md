# Paper10 DESI Row-4 Window Decision Gate v1

**Doc class:** source-side decision gate
**Reader role:** Paper10 DESI time/readout reviewer
**Status:** pending/blocker/source-reopen state machine; not replay; not validation
**Canonical parent:** `README.md`

This gate converts the row-4 source-window review state into a single
machine-readable status.

Inputs:

- the blank row-4 window review package summary;
- an optional completed row-4 window review response summary.

If no completed response summary exists, the gate reports:

`ROW4_WINDOW_REVIEW_PENDING_NOT_REPLAY`

If a completed response exists and keeps the strict window or rejects the source,
the gate reports:

`ROW4_WINDOW_BLOCKER_REMAINS_NOT_REPLAY`

If a completed response accepts Moresco (2015) only as caveated source-side
near-window support, the gate reports one of:

- `ROW4_SOURCE_REOPEN_CAVEATED_NO_REPLAY`
- `ROW4_SOURCE_REOPEN_CAVEATED_REPLAY_REVIEW_REQUIRED_NOT_REPLAY`

The second case still does **not** authorize endpoint replay. It only means a
separate replay-authorization handoff may be prepared.

Current imported state:

`ROW4_SOURCE_REOPEN_CAVEATED_NO_REPLAY`

The completed source-blocker review accepts Moresco (2015) at `z=1.363` only as
caveated near-window source-side context.  The strict `|Delta z| <= 0.10`
window remains the default, and endpoint replay remains disabled.

Claim boundary:

- no endpoint replay,
- no validation claim,
- no physical-validation claim,
- no endpoint residuals,
- no endpoint scores,
- no fit statistics.

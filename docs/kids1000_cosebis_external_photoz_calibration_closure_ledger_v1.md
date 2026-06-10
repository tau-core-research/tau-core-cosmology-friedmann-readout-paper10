# KiDS-1000 COSEBIs External Photo-z Calibration Closure Ledger V1

**Doc class:** source-side closure ledger
**Reader role:** records the post-reviewer H1/R4 status without authorizing endpoint replay
**Status:** source-side closed; endpoint replay still forbidden
**Canonical parent:** `README.md`

## Purpose

This ledger records the direct consequence of the completed reviewer response:
the external photo-z calibration route is closed at source-side H1/R4 level.

It does not rewrite earlier acquisition, manifest, preflight, or handoff
artifacts. Those remain historical prerequisite states. This ledger is the
current post-reviewer closure state.

## Boundary

The ledger computes no scores, contains no endpoint data, does not authorize
endpoint replay, and does not claim endpoint validation. Any endpoint replay
requires a separate explicit human authorization gate.

## Verdict

`external_photoz_calibration_source_side_closed_endpoint_replay_still_forbidden`

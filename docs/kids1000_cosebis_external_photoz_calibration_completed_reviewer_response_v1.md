# KiDS-1000 COSEBIs External Photo-z Calibration Completed Reviewer Response V1

**Doc class:** independent reviewer response validator
**Reader role:** source-side acceptance gate for a returned reviewer CSV
**Status:** validator available; no completed response bundled
**Canonical parent:** `README.md`

## Purpose

This validator is the import gate for a completed independent reviewer
attestation produced from the reviewer handoff package. It is intentionally
narrow: it checks whether the returned CSV answers the four source-side
questions, keeps forbidden endpoint inputs out of the review, and preserves the
no-replay/no-validation boundary.

## Acceptance Boundary

An accepted response may close the source-side reviewer attestation for the
external photo-z calibration route. It does not compute new scores, does not
inspect endpoint residuals, does not authorize endpoint replay, and does not
claim endpoint validation.

The accepted verdict is:

`completed_reviewer_response_accepted_source_side_only_endpoint_replay_still_forbidden`

## Usage

```bash
python scripts/validate_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.py \
  path/to/completed_reviewer_response.csv \
  --summary-out data/derived/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1_summary.csv
```

The completed reviewer response itself is not bundled in this repository until
an actual independent response exists.

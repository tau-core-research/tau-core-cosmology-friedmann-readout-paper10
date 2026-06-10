# KiDS-1000 COSEBIs External Photo-z Calibration Leakage Review Preflight V1

**Doc class:** source-side leakage review preflight
**Reader role:** reviewer-facing bridge between cached calibration sources and independent review
**Status:** automated leakage preflight passed; independent reviewer attestation open
**Canonical parent:** `README.md`

## Purpose

The external photo-z/tomographic calibration source manifest attaches cached
public sources for the first three H1 routes. This preflight checks that those
artifacts remain source-side and do not use endpoint residuals, scores,
post-score ranks, or fit statistics.

## What this closes

The automated part of the leakage review passes:

- source-manifest rows keep forbidden inputs, endpoint replay, and validation
  flags false;
- cached public sources exist and expose the required source-side markers;
- the source-manifest builder does not depend on endpoint scoring or residual
  artifacts.

## What remains open

This is not an independent reviewer attestation. The full R4 leakage review
remains open, H1 remains incomplete, and endpoint replay remains forbidden.

## Verdict

`automated_leakage_preflight_passed_independent_reviewer_still_open`

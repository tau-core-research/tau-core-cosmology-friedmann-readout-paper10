# KiDS-1000 COSEBIs External Photo-z Calibration Source Manifest V1

**Doc class:** source-side calibration source manifest
**Reader role:** reviewer-facing source attachment for H1, before leakage review
**Status:** R1--R3 source artifacts attached; R4 leakage review open
**Canonical parent:** `README.md`

## Purpose

The H1 acquisition plan requires independent photo-z or tomographic calibration
material before any endpoint replay. This manifest attaches cached public
source artifacts for the calibration reference route, SOM-gold / \(n(z)\)
route, and tomographic-bin quality route. It does not compute a score and does
not authorize endpoint replay.

## Cached sources

- A&A article: `KiDS-1000 catalogue: Redshift distributions and their
  calibration`.
- arXiv metadata page for `arXiv:2007.15635`.
- Official KiDS DR4 weak-lensing SOM-gold catalogue page.

The cached source checks look for source-side markers only: SOM calibration,
five tomographic redshift bins, gold selection, residual mean-redshift
bias/uncertainty statements, clustering-redshift cross-checks, and official
KiDS \(n(z)\) product route text.

## Claim boundary

This manifest attaches external calibration sources, but it does not complete
H1. The leakage/reviewer review route remains open. Endpoint replay and
validation claims remain forbidden until that review is complete.

## Verdict

`external_photoz_calibration_sources_attached_pending_leakage_review`

# KiDS-1000 COSEBIs Photo-z / Tomographic Calibration Evidence V1

**Doc class:** source-side calibration evidence ledger  
**Reader role:** reviewer-facing status of H1 before any tomographic replay  
**Status:** partial evidence available; independent external calibration still open  
**Canonical parent:** `README.md`

## Purpose

The tomographic holdout gate requires independent photo-z or tomographic
calibration evidence before endpoint replay. This ledger records what the
current repository can support without using endpoint residuals or fit
statistics.

## Accepted source-side evidence

- The KiDS-1000 cosmic-shear tarball is checksum-frozen.
- The cached KiDS DR4 lensing page contains the weak-lensing SOM-gold catalogue
  route and the public photometric-redshift citation markers.
- The committed `NZ_SOURCE` inventory provides five source-bin redshift kernels
  with 119 rows each.

## Remaining blocker

The ledger does not attach an independent external photo-z or tomographic
calibration manifest. Therefore H1 is not complete and endpoint replay remains
forbidden.

## Verdict

`partial_photoz_tomographic_evidence_available_but_h1_external_calibration_open`

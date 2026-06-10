# KiDS-1000 COSEBIs External Photo-z Calibration Acquisition Plan V1

**Doc class:** source-side acquisition plan  
**Reader role:** reviewer-facing H1 blocker resolution checklist  
**Status:** acquisition plan frozen; external calibration not yet attached  
**Canonical parent:** `README.md`

## Purpose

The photo-z/tomographic evidence ledger records partial source-side evidence,
but H1 remains open because no independent external calibration manifest is
attached. This plan freezes the next required source-side acquisition routes
without using endpoint residuals, fit statistics, null ranks, or post-score
shape information.

## Required routes

- `R1`: attach a source-frozen photo-z calibration reference or product
  manifest from official KiDS/DR4/KiDS-1000 calibration material.
- `R2`: attach an independent SOM-gold or redshift-distribution validation
  manifest.
- `R3`: attach tomographic-bin quality, \(\Delta z\) prior, or equivalent
  source-side calibration-quality evidence.
- `R4`: after `R1`--`R3` are attached, complete a leakage review showing that
  endpoint residuals, endpoint scores, null-control ranks, and post-score
  residual shapes were not used.

## Current status

No route is attached by this plan. It is a frozen acquisition checklist only.
Endpoint replay and validation claims remain forbidden.

## Verdict

`external_photoz_calibration_acquisition_plan_frozen_h1_still_open`

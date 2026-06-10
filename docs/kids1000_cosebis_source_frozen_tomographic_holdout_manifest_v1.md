# KiDS-1000 COSEBIs Source-Frozen Tomographic Holdout Manifest V1

**Doc class:** source-freeze / holdout partition manifest  
**Reader role:** reviewer-facing protocol for the next tomographic replay gate  
**Status:** holdout partition frozen; independent external calibration still open  
**Canonical parent:** `README.md`

## Purpose

The tomographic holdout/calibration gate requires a source-side holdout
partition before any endpoint replay can be treated as validation-facing. This
manifest freezes that partition without using endpoint residuals, fit
statistics, null-control ranks, or observed COSEBIs values.

## Rule

The partition is a deterministic five-fold leave-one-source-bin schedule. In
fold \(k\), all tomographic pairs that touch source bin \(k\) are held out, and
all remaining tomographic pairs are calibration pairs.

This is deliberately not a best-looking split. It is a source-index rule built
from the KiDS tomographic-bin structure and the committed source-native
redshift-kernel inventory.

## Current status

The holdout partition is frozen, but the independent external
photometric-redshift or tomographic-calibration evidence required by the parent
gate is not yet attached. Therefore this manifest does not authorize endpoint
replay and does not claim validation.

## Verdict

`holdout_partition_frozen_but_independent_photoz_calibration_still_open`

# KiDS-1000 COSEBIs Tomographic / Photo-z Closure Status v1

Document class: reproducibility ledger.

Status: `TOMOGRAPHIC_PHOTOZ_CLOSURE_STATUS_BUILT_NOT_VALIDATION`.

This ledger summarizes the narrow post-reviewer state of the KiDS-1000 COSEBIs
tomographic/photo-z branch. It computes no new score, uses no endpoint residual
shape for source selection, and makes no endpoint-validation or physical-
validation claim.

## Inputs

- External photo-z calibration closure ledger:
  `data/derived/kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv`
- Source-frozen tomographic holdout replay:
  `data/derived/kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv`
- Best holdout-beating tomographic-control source-evidence gate:
  `data/derived/kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1_summary.csv`
- Validation-readiness ledger:
  `data/derived/kids1000_cosebis_validation_readiness_ledger_v1_summary.csv`

## Result

The external photo-z/tomographic calibration route is source-side closed:

- `h1_independent_evidence_complete=true`
- `r4_leakage_review_complete=true`

The source-bin holdout replay remains diagnostic-positive:

- `candidate_holdout_improved_fold_count=4/5`
- `source_bin_holdout_signal_survives=true`

The best holdout-beating tomographic control remains control-only:

- `best_holdout_control_physical_alternative=false`

However, this does not make the KiDS branch validation-ready:

- `tomographic_caveat_active=true`
- `physical_promotion_ready=false`
- `validation_ready=false`

## Allowed Current Claim

`source_side_photoz_closed_and_holdout_signal_survives_but_validation_blocked`

In plain language: the independent photo-z/source-side concern has been reduced,
and the KiDS low-tail signal survives the current diagnostic holdout checks, but
the branch is still not a KiDS validation because physical-promotion blockers
remain open.

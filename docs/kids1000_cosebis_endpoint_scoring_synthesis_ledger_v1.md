# KiDS-1000 COSEBIs Endpoint Scoring Synthesis Ledger V1

**Doc class:** endpoint scoring synthesis ledger  
**Reader role:** reviewer-facing diagnostic summary  
**Status:** built from existing endpoint score and robustness artifacts; not validation  
**Canonical parent:** `README.md`

## Purpose

This ledger aggregates the existing KiDS-1000 COSEBIs endpoint score and its
follow-up diagnostics into one claim-safe decision surface. It does not compute
new scores, select new kernels, retune amplitudes, or promote the diagnostic
endpoint into a physical prediction.

## Inputs

The ledger reads only existing committed summaries:

- `kids1000_cosebis_endpoint_scoring_v1_summary.csv`
- `kids1000_cosebis_endpoint_scoring_diagnostics_v1_summary.csv`
- `kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv`
- `kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv`
- `kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv`
- `kids1000_cosebis_endpoint_mode_localization_v1_summary.csv`
- `kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv`
- `kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv`

## Claim-safe synthesis

The current endpoint result is a low-tail diagnostic signal: the source-frozen
candidate improves the zero baseline and ranks in the low tail against
predeclared controls. It is not an absolute winner because tomographic
shuffle/control variants still outperform it. The plausibility audit classifies
the better controls as control-only or conditional source-systematic candidates,
not accepted physical alternatives in the current source state.

The jackknife/localization audits support that the signal is not carried by one
source bin or one tomographic pair. The mode audits sharpen the caveat: the
signal is strongly low-mode localized and carrier-sensitive, although it is not
produced solely by the exact candidate carrier.

The physical-promotion blocker ledger remains decisive: even with a diagnostic
endpoint signal, physical promotion is blocked by open requirements for the
survey-native operator theorem, leakage theorem, gauge/quotient descent,
response-unit normalization, and the standard-lensing/no-Tau-source
null-amplitude theorem.

## Verdict

`endpoint_signal_low_tail_caveated_by_tomographic_controls_and_physical_promotion_blockers`

The next scoring-facing action should be a predeclared tomographic-structure
holdout or an independent lensing-probe replay before any stronger physical
claim.

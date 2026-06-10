# KiDS-1000 COSEBIs Physical Promotion Dependency Order v1

Document class: blocker-dependency ledger.

Status: `PHYSICAL_PROMOTION_DEPENDENCY_ORDER_BUILT_NOT_PROOF`.

This ledger orders the five remaining physical-promotion blockers after the
diagnostic KiDS/COSEBIs pipeline and the source-side photo-z closure have been
recorded. It computes no new score, contains no endpoint residuals, and makes
no endpoint-validation or physical-validation claim.

## Dependency Order

1. `B2_operator_leakage_theorem_open`
   - next primary proof gate
   - reason: a survey-native operator cannot be physical if non-uniform
     mask/leakage directions can mimic the low-mode response

2. `B3_gauge_quotient_descent_open`
   - next parallel proof gate
   - reason: a physical response must be independent of representative or
     gauge choice

3. `B4_response_unit_normalization_open`
   - waits for leakage and quotient control
   - reason: the dimensionless source kernel needs a response-unit map before
     it can become a physical COSEBIs prediction

4. `B5_standard_lensing_null_amplitude_theorem_open`
   - waits for leakage, quotient, and units
   - reason: the Tau-absent limit must recover standard lensing or an
     equivalent null response

5. `B1_survey_native_operator_theorem_open`
   - final synthesis proof gate
   - reason: the operator skeleton exists, but the full physical operator
     theorem requires leakage, quotient, units, and null-limit closure

## Current Verdict

`physical_promotion_ordered_leakage_and_gauge_are_next_not_validation`

In plain language: the data-side KiDS signal can stay as a diagnostic signal,
but the next theory-side work is not another endpoint score. The next narrow
proof work is leakage control and gauge/quotient descent. Only after those can
response units, the standard-lensing null limit, and the full survey-native
operator theorem be promoted.

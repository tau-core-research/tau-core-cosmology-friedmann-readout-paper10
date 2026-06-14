# Joint KiDS caveated-block resolution plan v1

**Doc class:** post-replay blocker-resolution plan
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_kids_caveated_block_resolution_plan_not_validation`

The joint guarded replay keeps the KiDS/COSEBIs low-mode block as a
caveated support block. The reason is not lack of a numerical low-tail
signal; the blocker is physical promotion. This plan freezes the proof
order required before the KiDS block can be promoted from caveated
support to clean joint support.

Frozen proof order:

1. operator leakage theorem
2. gauge quotient descent
3. response unit normalization
4. standard-lensing null-amplitude theorem
5. survey-native operator theorem

Summary:

- KiDS block status: `caveated`
- candidate delta chi2: `-1.836152665217e+02`
- tail fraction: `2.973240832507e-03`
- open resolution steps: `5`
- next primary proof gate: `B2_operator_leakage_theorem_open`
- next parallel proof gate: `B3_gauge_quotient_descent_open`
- verdict: `KIDS_JOINT_BLOCK_HAS_SIGNAL_BUT_CAVEAT_RESOLUTION_REQUIRES_PHYSICAL_PROMOTION_PROOFS`

Interpretation: the KiDS block can motivate further work, but it cannot
be used as clean validation support until the physical-promotion proof
chain is closed without endpoint leakage.

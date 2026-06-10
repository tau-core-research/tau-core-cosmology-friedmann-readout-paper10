**Doc class:** validation-readiness synthesis ledger
**Reader role:** reviewer checking the current KiDS/COSEBIs claim boundary after the tomographic-control follow-up gates
**Status:** diagnostic readiness summary; not validation
**Canonical parent:** README.md

# KiDS-1000 COSEBIs Validation-Readiness Ledger

This ledger summarizes the current KiDS/COSEBIs endpoint state after the
authorized replay, tomographic-control disambiguation, source-bin holdout
replay, best-control source-evidence gate, and physical-promotion blocker
ledger.

It computes no new score and does not change the endpoint result.

Current status:

- low-tail endpoint signal is present,
- tomographic controls do not refute the endpoint signal,
- source-bin holdout replay preserves the signal in 4/5 folds,
- the best holdout-beating control remains control-only rather than a physical
  alternative,
- the tomographic caveat remains active,
- physical promotion remains blocked by open operator/amplitude/normalization
  requirements,
- endpoint validation is not claimed.

Allowed current claim:

```text
diagnostic_low_tail_signal_with_reduced_tomographic_control_concern_not_validation
```

Required next gate:

```text
independent_tomographic_or_photoz_holdout_and_physical_promotion_blocker_resolution
```

In plain language, the KiDS signal has survived the narrow follow-up checks
performed so far, and the most dangerous tomographic control has not become a
source-side physical alternative. This strengthens the diagnostic status, but
it is still not KiDS validation.

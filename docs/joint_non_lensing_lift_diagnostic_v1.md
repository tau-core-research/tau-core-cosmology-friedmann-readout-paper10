# Joint non-lensing lift diagnostic v1

**Doc class:** fragility-remediation diagnostic
**Status:** not endpoint scoring; not validation

This diagnostic asks how much non-lensing support is needed for the
joint multichannel score to remain positive when the KiDS/COSEBIs
lensing block is removed. It uses only the already frozen joint
candidate channel ledger.

Summary:

- non-lensing weighted sum: `-0.363118958`
- required lift to zero: `0.363118958`
- required lift to protocol margin 0.25: `1.113118958`
- highest lift-priority channel: `observer_path_basis_low_z`
- verdict: `NON_LENSING_FRAGILITY_REMEDIATION_HAS_SINGLE_CHANNEL_ROUTES_NOT_VALIDATION`

Interpretation: this identifies where additional source-frozen work
would reduce KiDS/lensing dominance. It is not an invitation to tune
a channel after looking at residuals.

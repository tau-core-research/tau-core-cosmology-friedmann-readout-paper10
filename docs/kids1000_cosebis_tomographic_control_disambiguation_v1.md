**Doc class:** endpoint caveat audit ledger
**Reader role:** reviewer checking why tomographic controls do or do not refute the KiDS/COSEBIs replay signal
**Status:** diagnostic disambiguation; not validation
**Canonical parent:** README.md

# KiDS-1000 COSEBIs Tomographic Control Disambiguation

This ledger separates the authorized endpoint replay signal from the
tomographic-control caveat.

The authorized replay remains a low-tail endpoint signal. The open question is
whether the few tomographic controls that beat the candidate are physical
alternatives, source-systematic candidates, or control-only relabelings.

The disambiguation uses the already-built tomographic robustness and
plausibility audit artifacts. It computes no new score and does not inspect
endpoint residual shape for source selection.

Current result:

- candidate-beating tomographic controls: 3,
- control-only: 2,
- conditional source-systematic candidate: 1,
- accepted physical alternatives: 0.

Thus the tomographic controls do not refute the endpoint signal, but they still
block validation. The next required step is an independent photo-z/tomographic
holdout replay before promoting any tomographic alternative.


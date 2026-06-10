**Doc class:** endpoint caveat replay ledger
**Reader role:** reviewer checking whether the KiDS/COSEBIs signal survives source-bin holdout structure
**Status:** diagnostic holdout replay; not validation
**Canonical parent:** README.md

# KiDS-1000 COSEBIs Tomographic Holdout Replay

This replay uses the source-frozen five-fold tomographic holdout manifest. For
each fold, all tomographic pairs touching one held-out source bin are scored as
the holdout set, while the non-touching pairs are used only to freeze the
nonnegative amplitude.

The replay compares the source-frozen candidate against the three
candidate-beating tomographic controls already identified by the stricter
tomographic robustness/disambiguation chain. It creates no new labels and does
not use holdout scores for source-side selection.

Current result:

- candidate improves over the zero baseline in 4/5 held-out source-bin folds,
- aggregate candidate holdout \(\Delta\chi^2=-521.8035067179\),
- one candidate-beating tomographic control remains slightly better in the
  same holdout replay,
- candidate rank among the four compared branches is 2/4,
- endpoint validation is not claimed.

Thus the holdout replay preserves the low-tail signal in a useful diagnostic
sense, but the tomographic-control caveat remains active. The next narrow step
is still independent photo-z/tomographic evidence or a stronger source-frozen
tomographic holdout replay before any validation-facing claim.

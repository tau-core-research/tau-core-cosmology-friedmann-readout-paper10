# KiDS-1000 COSEBIs `F_overlap` Batch Promotion Review v1

This gate defines the source-side checklist for promoting a manually fetched
full-mask batch into a reviewable source-freeze artifact.

The public package currently has no committed fetched-batch review artifact.
Therefore the gate is expected to remain `promotion_ready=false`.

The first blockers are:

- a committed execution-review artifact, not a machine-local `data/local/` log,
- a checksum manifest for the fetched FITS products,
- an accounting check that every product in the declared batch is present,
- a forbidden-input audit showing no KiDS data-vector, posterior, residual, fit
  statistic, or post-hoc tile selection was used.

Passing this gate would still not compute an overlap rule. It would only allow a
later, separate source-native overlap derivation gate to consume the frozen
batch artifact.

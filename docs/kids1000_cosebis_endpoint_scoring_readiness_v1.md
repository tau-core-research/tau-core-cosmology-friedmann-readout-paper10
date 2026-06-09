# KiDS-1000 COSEBIs Endpoint Scoring Readiness v1

This gate summarizes the current distance from a KiDS-1000 COSEBIs endpoint
score.

It is not a scoring script and not a validation result. It only collects the
source-side readiness state of the components that would be required before an
endpoint can be attempted.

Current result:

- ready source-side components: data-vector structure, covariance matrix,
  covariance solve policy, the theory-vector row-interface template, and the
  mapping-to-template join contract, plus the F-overlap resolution/control
  decision;
- blocking components: theory vector, web/path mapping, source preflight,
  blocker-resolution order, and null controls;
- first blocker: `F_overlap`;
- endpoint scoring remains disabled.

The ledger forbids KiDS data-vector values for source selection, posterior
chains, fit-improvement flags, lensing residuals, post-hoc channel activation,
post-hoc mode cuts, post-hoc tomographic selection, post-hoc sky-direction
selection, post-hoc web/path labels, and post-hoc weight selection.

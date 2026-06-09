# KiDS-1000 COSEBIs Endpoint Scoring Readiness v1

This gate summarizes the current distance from a KiDS-1000 COSEBIs endpoint
score.

It is not a scoring script and not a validation result. It only collects the
source-side readiness state of the components that would be required before an
endpoint can be attempted.

Current result:

- ready source-side components: data-vector structure, covariance matrix,
  covariance solve policy, the theory-vector row-interface template, the
  mapping-to-template join contract, the blocker-resolution ledger, and the
  F-overlap resolution/control decision;
- `F_overlap` and a caveated full-route `D_path` mask-load proxy are
  source-supported, and `E_web` is source-supported only as a uniform null-web
  control;
- `C_norm` is source-side resolved by unit-mean normalization of the frozen
  source factors;
- blocking components: source preflight/mapping vector, theory vector, web/path
  mapping, null controls, and the partial-control degeneracy audit;
- first blocker: `mapping_vector`;
- endpoint scoring remains disabled.

The ledger forbids KiDS data-vector values for source selection, posterior
chains, fit-improvement flags, lensing residuals, post-hoc channel activation,
post-hoc mode cuts, post-hoc tomographic selection, post-hoc sky-direction
selection, post-hoc web/path labels, and post-hoc weight selection.

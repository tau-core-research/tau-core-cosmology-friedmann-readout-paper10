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
- the web/path mapping and source-preflight ledgers now expose a source-frozen
  300-row mapping basis;
- a source-frozen unit-amplitude theory-vector shell is now built from the
  frozen mapping basis and a predeclared unit-mean mode-shape rule;
- predeclared null controls have been replayed as source-frozen control
  theory-vector digests, without scores;
- the endpoint-family geometry audit passes on the source-frozen candidate plus
  predeclared null-control vector family;
- ready components: 12;
- blocking components: 0;
- first endpoint blocker: `none`;
- endpoint scoring remains disabled until an explicit scoring run is opened
  under the frozen protocol.

The ledger forbids KiDS data-vector values for source selection, posterior
chains, fit-improvement flags, lensing residuals, post-hoc channel activation,
post-hoc mode cuts, post-hoc tomographic selection, post-hoc sky-direction
selection, post-hoc web/path labels, and post-hoc weight selection.

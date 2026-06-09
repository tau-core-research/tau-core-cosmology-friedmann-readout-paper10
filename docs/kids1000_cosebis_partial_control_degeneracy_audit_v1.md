# KiDS-1000 COSEBIs Partial-Control Degeneracy Audit V1

This artifact audits the branch geometry of the caveated three-mask
partial-control diagnostic score before any endpoint claim is allowed.

It uses:

- the frozen partial-control design matrix,
- the KiDS COSEBIs `COVMAT` covariance as a branch-geometry metric only.

It does not use:

- KiDS `En` data-vector values,
- residuals,
- posterior chains,
- fit-improvement flags,
- post-hoc mask, channel, mode, sky, web, or path labels.

Main result:

- the positive partial-control branches are effectively rank one;
- their covariance-metric absolute cosine is numerically unity;
- the sign-flip branch is the same shape with opposite sign;
- therefore the previous diagnostic score and null replay remain useful smoke
  tests, but they do not yet provide a non-degenerate endpoint theory-vector
  route.

Claim boundary:

`partial_control_degeneracy_audit_not_endpoint_not_validation`

Recommended next action:

replace the three-mask partial-control branch family with a non-degenerate,
source-frozen full-route or official-geometry mapping before endpoint scoring.

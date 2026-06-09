# KiDS-1000 COSEBIs Endpoint-Family Geometry Audit v1

This audit checks whether the source-frozen endpoint comparison family is
geometrically non-degenerate before endpoint scoring is allowed.

It deliberately does not use the KiDS COSEBIs `En` data vector. It uses:

- the source-frozen unit-amplitude candidate theory shell;
- the source-frozen null-control theory replay;
- the KiDS covariance matrix only as a geometry metric.

This audit supersedes the earlier three-mask partial-control degeneracy blocker
as an endpoint-readiness geometry test. The earlier partial-control audit remains
preserved as a negative result: that diagnostic branch family is effectively
rank one. The source-frozen endpoint family is different because it includes the
full-route source-frozen candidate and the predeclared null-control vectors.

Current result:

- endpoint-family vector count: 1009;
- retained COSEBIs rows: 300;
- raw Euclidean effective rank at tolerance `1e-8`: 15;
- covariance-metric effective rank at tolerance `1e-8`: 15;
- endpoint-family geometry passed: true;
- endpoint scoring executed: false.

The covariance matrix is used only to define the geometry metric. No residual,
likelihood, AIC value, null-control score, endpoint score, or validation result
is computed by this audit.

Claim boundary:

```text
kids1000_cosebis_endpoint_family_geometry_audit_not_scoring_not_validation
```

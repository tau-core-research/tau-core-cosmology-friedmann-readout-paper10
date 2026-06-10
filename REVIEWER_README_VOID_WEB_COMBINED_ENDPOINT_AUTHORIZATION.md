# Void/Web Combined Endpoint Authorization Review

This package is a permission-only reviewer handoff for a future combined
void/web multiblock endpoint run. It is not an endpoint run and it is not a
validation claim.

## First Checks

If you received the ZIP and `.zip.sha256` sidecar together, place both files in
the same directory and run:

```bash
shasum -a 256 -c void_web_combined_multiblock_endpoint_authorization_review_package_v1.zip.sha256
```

Expected result:

```text
void_web_combined_multiblock_endpoint_authorization_review_package_v1.zip: OK
```

## Start Here

Read:

```text
docs/void_web_combined_multiblock_endpoint_authorization_review_v1.md
docs/void_web_combined_multiblock_endpoint_protocol_v1.md
docs/void_web_endpoint_readiness_after_flrw_audit_v1.md
```

Complete:

```text
data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv
```

## Boundary

Do not inspect or use endpoint residuals, endpoint scores, fit statistics,
post-hoc block weights, post-hoc covariance reweighting, or post-hoc channel
promotion. A completed review can only authorize or reject one future,
predeclared combined void/web endpoint run. It cannot validate Tau Core
cosmology or promote the existing isolated pilots.

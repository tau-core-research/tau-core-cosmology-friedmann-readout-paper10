# Void/Web Combined Multiblock Endpoint Authorization Review v1

**Doc class:** authorization-review template  
**Reader role:** Paper 10 endpoint-governance / leakage prevention  
**Status:** template ready, not completed, no endpoint run authorized  
**Canonical parent:** README.md

This review layer sits after the combined void/web multiblock endpoint protocol.
It does not run scoring. It asks whether a separate, single, predeclared
combined void/web endpoint run may be authorized while keeping
`physical_validation_claimed=false`.

The template is written to:

```text
data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv
```

The template defaults to:

```text
review_completed = false
endpoint_run_allowed = false
physical_validation_claimed = false
```

The authorization reviewer must not use distance residuals, growth residuals,
lensing residuals, endpoint scores, fit statistics, or post-hoc block/channel
choices. Until a completed response is accepted, the combined void/web endpoint
run remains forbidden.

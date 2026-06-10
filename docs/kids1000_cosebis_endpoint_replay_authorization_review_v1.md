**Doc class:** reviewer handoff note
**Reader role:** independent reviewer without repository access
**Status:** blank authorization package; not completed
**Canonical parent:** README.md

# KiDS-1000 COSEBIs Endpoint Replay Authorization Review

This review package is the next narrow gate after the completed source-side
H1/R4 closure ledger. It asks only whether a separate endpoint replay may be
authorized under the frozen source-side state.

It does not authorize endpoint validation. It does not contain endpoint scores,
endpoint residuals, fit statistics, null-control ranks, post-score residual
shapes, or observed COSEBIs values.

The reviewer should fill:

```text
kids1000_cosebis_endpoint_replay_authorization_review_response_template_v1.csv
```

Allowed decisions are:

- `GO_SOURCE_SIDE_REPLAY_PERMISSION_ONLY`
- `NO_GO_NEEDS_MORE_SOURCE_SIDE_EVIDENCE`
- `NO_GO_LEAKAGE_OR_SCOPE_RISK`

If the reviewer chooses a go decision, the scope is a single separate
predeclared endpoint replay only, with `endpoint_validation_claimed=false`.


# KiDS-1000 COSEBIs Endpoint Replay Authorization Review

This package is for an external reviewer who does not have access to the
repository.

## Review purpose

Please decide whether the already completed source-side H1/R4 closure is
sufficient to authorize a separate endpoint replay for the predeclared
KiDS-1000 COSEBIs endpoint.

This is a replay-permission review only. It is not a request to validate Tau
Core, KiDS, COSEBIs, or any endpoint result.

## What you may use

Use only the files in this ZIP package:

- the completed source-side reviewer response,
- the source-side closure ledger,
- the source manifest and leakage preflight summaries,
- the tomographic holdout/calibration gate summaries,
- the package manifest and SHA256 checksums,
- the blank authorization response CSV.

## Forbidden inputs

Do not use or request:

- observed COSEBIs data-vector values,
- endpoint residuals,
- endpoint scores,
- fit statistics,
- null-control ranks,
- post-score residual shapes,
- any unpublished endpoint replay output.

If any forbidden endpoint information is needed to make the decision, answer
`NO_GO_NEEDS_MORE_SOURCE_SIDE_EVIDENCE`.

## What to fill

Fill this file:

```text
kids1000_cosebis_endpoint_replay_authorization_review_response_template_v1.csv
```

Return the completed CSV only. Keep `endpoint_validation_claimed=false`.

## Allowed decisions

- `GO_SOURCE_SIDE_REPLAY_PERMISSION_ONLY`
- `NO_GO_NEEDS_MORE_SOURCE_SIDE_EVIDENCE`
- `NO_GO_LEAKAGE_OR_SCOPE_RISK`

If you choose `GO_SOURCE_SIDE_REPLAY_PERMISSION_ONLY`, this authorizes only a
single explicitly predeclared endpoint replay under the existing frozen
source-side state. It does not authorize a validation claim.


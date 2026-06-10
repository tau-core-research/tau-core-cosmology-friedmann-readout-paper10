# Void Source-Basis Refinement Endpoint Replay Authorization Review v1

**Doc class:** endpoint replay authorization handoff  
**Status:** authorization template/package; not completed; not scoring; not validation

This gate comes after the R6 source-side leakage review. Its purpose is only to
ask whether one separate, predeclared refined low-z void source-basis replay may
be run under the already frozen R4/R5 source-basis and control rules.

It does not run the replay, compute endpoint scores, or claim physical
validation.

## Required precondition

The completed R6 reviewer response must have:

```text
leakage_review_complete=true
source_unique_ready=true
endpoint_replay_allowed=false
endpoint_validation_claimed=false
```

## Proposed scope

The proposed replay scope is limited to:

- low-z Pantheon rows already used in the void refinement route;
- R4-admitted source-side features;
- R5 frozen controls;
- no post-hoc void catalogue, row, threshold, amplitude, or covariance changes.

## Artifacts

```text
data/source_manifest/void_source_basis_refinement_endpoint_replay_authorization_review_policy_v1.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_response_template_v1.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_template_v1_summary.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.zip
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1.zip.sha256
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1_manifest.csv
data/derived/void_source_basis_refinement_endpoint_replay_authorization_review_package_v1_summary.csv
```

## Claim boundary

```text
void_source_basis_refinement_endpoint_replay_authorization_review_not_validation
```

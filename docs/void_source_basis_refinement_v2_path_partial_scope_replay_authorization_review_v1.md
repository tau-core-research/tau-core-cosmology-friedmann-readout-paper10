# V2 Path Partial-Scope Replay Authorization Review v1

**Doc class:** endpoint replay authorization handoff  
**Status:** authorization template/package; not completed; not scoring; not validation

This gate follows the completed V2 partial path-scope source-side review.  Its
purpose is only to ask whether one separate, permission-only partial replay may
be run for the 12 predeclared `W_path` candidate rows.

It does not run the replay, compute endpoint scores, claim endpoint validation,
enable a full low-z `W_path` channel, or promote the tile-proximity value as a
calibrated physical lensing-path weight.

## Required precondition

The completed V2 partial path review must have:

```text
review_completed=true
final_verdict=ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
future_action_allowed=prepare_separate_partial_scope_replay_authorization_package_only
```

## Proposed replay scope

The proposed authorization scope is limited to:

- the 12 predeclared partial path-scope rows;
- 5 strict path-scope candidates and 7 caveated candidates;
- the frozen source-side tile-proximity control values;
- no KiDS data-vector values, posterior chains, endpoint residuals, endpoint
  scores, fit statistics, post-hoc sky selection, or post-hoc path-weight
  tuning;
- no full low-z `W_path` channel for the remaining 412 rows.

## Artifacts

```text
data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_policy_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_template_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1_summary.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.zip
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1.zip.sha256
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_manifest.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_summary.csv
```

## Claim Boundary

```text
v2_path_partial_scope_replay_authorization_review_not_validation
```

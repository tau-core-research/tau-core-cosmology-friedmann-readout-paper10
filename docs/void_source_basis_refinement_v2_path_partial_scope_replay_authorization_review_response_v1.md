# V2 Path Partial-Scope Replay Authorization Review Notes v1

## Decision

```text
GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY
```

## Scope authorized

This review authorizes only one separate, explicitly predeclared partial `W_path` replay over the frozen 12-row partial path-scope source-side labels and tile-proximity control values.

Authorization scope:

```text
single_permission_only_12_row_partial_W_path_replay_not_validation
```

## Preconditions checked from the package

- Completed partial path-scope review: `review_completed=true`.
- Completed partial path-scope verdict: `ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE`.
- Prior source-side review kept `endpoint_replay_allowed=false`.
- Prior source-side review kept `endpoint_validation_claimed=false`.
- Prior source-side review kept `physical_lensing_path_weight_claimed=false`.
- Future action from prior review was only `prepare_separate_partial_scope_replay_authorization_package_only`.

## Source-side scope facts checked

- Low-z rows in scope ledger: `424`.
- Strict path-scope candidates: `5`.
- Caveated path-scope candidates: `7`.
- Total partial path-scope candidates: `12`.
- Remaining low-z rows with full `W_path` channel disabled: `412`.
- Partial path values computed: `true`.
- Full low-z path values computed: `false`.
- Nonzero partial `W_path` values: `12`.
- Candidate `W_path_source_value` range: `6.129006671360e-02` to `4.420864334176e-01`.
- Path rule: `P_tile=max(0,(2deg-sep)/2deg); W_path=P_tile/(1+abs(P_tile))`.
- Rule status: `SOURCE_ONLY_TILE_PROXIMITY_CONTROL_NOT_PHYSICAL_LENSING_WEIGHT`.

## Review item responses

```text
Q1_source_side_review_closure = yes
Q2_partial_scope_replay_scope = caveated_yes
Q3_no_leakage = yes
Q4_authorization = GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY
```

## Boundary preserved

```text
forbidden_inputs_used=false
endpoint_replay_allowed=true
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
claim_boundary=v2_path_partial_scope_replay_authorization_review_not_validation
```

This is permission-only authorization. It does not run the replay, compute endpoint scores, claim endpoint validation, enable a full low-z `W_path` channel, tune path weights post hoc, use KiDS data-vector values, or promote `W_path` to a calibrated physical lensing-path weight.

## Package checks

```text
input_zip_sha256=03f4a7d801e0987df6797fa4a8d321d8af1d6ee7b04201bb6cbe81cca2b08b4a
manifest_hash_check=pass
package_forbidden_endpoint_flags_check=pass
template_validator_precompletion_check=pass
precondition_check=pass
completed_response_check=pass
```

## Output files

```text
void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_template_v1.csv
void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_completed_summary_v1.csv
void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_notes_v1.md
void_source_basis_refinement_v2_path_partial_scope_replay_authorization_validation_log_v1.txt
void_source_basis_refinement_v2_path_partial_scope_replay_authorization_completed_review_response_v1.zip
void_source_basis_refinement_v2_path_partial_scope_replay_authorization_completed_review_response_v1.zip.sha256
```

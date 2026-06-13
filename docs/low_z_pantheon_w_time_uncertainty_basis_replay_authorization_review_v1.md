# Low-z Pantheon+ W-time uncertainty-basis replay authorization review v1

**Doc class:** endpoint replay authorization handoff
**Status:** authorization template/package; not completed; not scoring; not validation

This gate follows the frozen source-side `W_time` uncertainty-basis candidate.
Its purpose is only to ask whether one separate, permission-only replay may be
run using that frozen basis.

It does not run the replay, compute endpoint scores, claim endpoint validation,
or promote the uncertainty basis into a physical clock-drift measurement.

## Required precondition

The source-side basis candidate must have:

```text
status=W_TIME_UNCERTAINTY_BASIS_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING
W_time_values_status=SOURCE_SIDE_BASIS_CANDIDATE_ONLY_NOT_ENDPOINT
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
```

## Proposed replay scope

The proposed authorization scope is limited to:

- the 424 frozen low-z Pantheon+ source rows;
- the frozen CC redshift-bin policy;
- the frozen `Delta_clock_uncertainty_candidate`;
- the frozen source-normalized `W_time_uncertainty_basis_candidate`;
- no changes to labels, bins, normalization, or row selection;
- no Pantheon distance residuals, endpoint scores, fit statistics, late-time
  fitted parameters, posterior chains, post-hoc `H(z)` smoothing, or post-hoc
  clock anomaly labels in the authorization decision.

## Artifacts

```text
data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_policy_v1.csv
data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_template_v1.csv
data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1_summary.csv
data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.zip
data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.zip.sha256
data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_manifest.csv
data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_summary.csv
scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1.py
```

## Completed response validation

When a reviewer returns a completed CSV, validate it with:

```bash
python scripts/validate_low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1.py \
  data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1.csv
```

The validator only accepts a permission-only replay decision.  It writes a
summary with `endpoint_replay_allowed=true` only if all four review rows are
completed, forbidden inputs are false, endpoint validation remains false, and
the reviewed package checksum matches the frozen package.

## Claim boundary

```text
w_time_uncertainty_basis_replay_authorization_review_not_validation
```

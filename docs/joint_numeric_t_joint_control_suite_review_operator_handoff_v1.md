# Joint numeric T_joint control-suite review operator handoff v1

**Doc class:** operator handoff.
**Status:** waiting for external reviewer response.
**Claim boundary:** `joint_numeric_t_joint_control_suite_review_not_endpoint_scoring_not_validation`.

## What to send

Send this file to the external reviewer:

```text
data/derived/joint_numeric_t_joint_control_suite_review_package_v1.zip
```

The reviewer does not need repository access.

Expected checksum:

```text
70de8881d432a1ec7ae69825462821fee45afe13b539afb88cb6a659e025abba
```

The same zip has also been copied locally to:

```text
/Users/jolcsak/Downloads/joint_numeric_t_joint_control_suite_review_package_v1.zip
```

## What the reviewer is asked

The reviewer is not asked to approve endpoint scoring.

The narrow question is whether the already-built same-statistic control suite,
where `0/26` numeric controls beat or equal the candidate, is sufficient to
prepare a separate endpoint-scoring authorization package.

This is only a package-preparation permission gate. It is not endpoint scoring,
not a p-value, not a likelihood ratio, and not cosmological or physical
validation.

## Required accepted response fields

If the reviewer accepts all four rows, the completed CSV must set:

```text
endpoint_scoring_authorization_package_preparation_allowed=true
endpoint_scoring_allowed=false
endpoint_validation_claimed=false
cosmological_validation_claimed=false
physical_validation_claimed=false
forbidden_inputs_used=false
review_completed=true
```

Accepted response tokens are:

```text
ACCEPT_CONTROL_SUITE_REVIEW_SCOPE_NOT_ENDPOINT_SCORING
ACCEPT_SAME_STATISTIC_CONTROLS_NO_RETUNING
ACCEPT_PREPARE_SEPARATE_ENDPOINT_AUTHORIZATION_PACKAGE
ACCEPT_CAVEAT_PRESERVATION
```

Any direct scoring permission, validation claim, forbidden input use, or
missing rationale should be treated as a rejection or incomplete response.

## What to import

After the reviewer returns the completed CSV or a zip containing exactly one
matching response CSV, run:

```bash
python scripts/import_joint_numeric_t_joint_control_suite_review_response_v1.py \
  /path/to/completed_reviewer_response.csv
python scripts/build_joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.py
python scripts/validate_joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.py
python scripts/audit_joint_numeric_t_joint_endpoint_readiness_v1.py
```

The last command currently exits with code `2` while blocked. After a valid
accepted reviewer response, it should report:

```text
READY_TO_BUILD_ENDPOINT_AUTHORIZATION_PACKAGE_NOT_SCORING
```

Only then may the next authorization package be built. This handoff does not
authorize endpoint scoring.

# Joint Numeric T_joint Authorization Reviewer Instructions v1

This package asks only whether the already built channel-level numeric `z_i`
ledger may be combined once under the frozen symbolic shell:

```text
T_joint = sum_i q_i z_i
```

It does not authorize new endpoint scores, new fitting, endpoint validation,
cosmological validation, physical validation, retuning, channel selection, or
claim-strengthening.

## What to review

Use the package:

```text
data/derived/joint_numeric_t_joint_authorization_package_v1.zip
```

The same zip is also intended for handoff outside the repository.

Inside it, review at least:

- `docs/joint_numeric_t_joint_authorization_package_v1.md`
- `data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv`
- `data/derived/joint_numeric_zi_distribution_ledger_v1.csv`
- `data/derived/joint_single_statistic_protocol_shell_v1.csv`
- `data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv`
- `data/derived/joint_numeric_t_joint_authorization_response_template_v1.csv`

## How to fill the response

Fill:

```text
data/derived/joint_numeric_t_joint_authorization_response_template_v1.csv
```

If you authorize a numeric `T_joint` ledger, use these exact decisions:

- `NTJ_Q1_SCOPE`: `AUTHORIZE_NUMERIC_T_JOINT_LEDGER_ONLY_NOT_ENDPOINT_SCORING`
- `NTJ_Q2_FROZEN_INPUTS`: `ACCEPT_FROZEN_QI_ZI_INPUTS_NO_RETUNING`
- `NTJ_Q3_CAVEATED_COVARIANCE`: `ACCEPT_CAVEATED_COVARIANCE_BOUNDARY`
- `NTJ_Q4_NO_VALIDATION`: `ACCEPT_NUMERIC_TJOINT_NO_VALIDATION`

For every accepted row, keep:

- `forbidden_inputs_used=false`
- `numeric_t_joint_allowed=true`
- `endpoint_scoring_allowed=false`
- `endpoint_validation_claimed=false`
- `cosmological_validation_claimed=false`
- `physical_validation_claimed=false`

If any row cannot be accepted, set `reviewer_response=reject`, explain the
reason in `reviewer_rationale`, and do not authorize the numeric `T_joint`
ledger.

## Return

Return the completed CSV, or a ZIP containing the completed CSV.

The expected canonical import target is:

```text
data/derived/joint_numeric_t_joint_authorization_response_v1.csv
```

The expected accepted summary decision is:

```text
AUTHORIZE_NUMERIC_T_JOINT_LEDGER_NOT_ENDPOINT_SCORING_NOT_VALIDATION
```

## Claim Boundary

This review is only a permission gate for computing a numeric joint ledger
from already frozen inputs. It is not an endpoint scoring gate, not a
cosmological validation gate, and not a physical validation gate.

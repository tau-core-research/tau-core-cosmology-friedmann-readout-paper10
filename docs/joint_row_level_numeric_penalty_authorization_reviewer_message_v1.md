# Reviewer handoff: joint row-level numeric penalty authorization v1

Dear Reviewer,

Please review the attached package:

`joint_row_level_numeric_penalty_authorization_review_package_v1.zip`

This package asks only whether the already frozen symbolic row-level source-feature penalty may be promoted to a later numeric penalty-value computation package. It does not ask you to approve endpoint scoring, cosmological validation, or any change to `T_joint`.

## What is being reviewed

The symbolic formula already frozen in the package is:

```text
P_i(a) = omega_i * mean_{r,f}(z_{i,a,r,f}^2)
P_row(a) = sum_i P_i(a)
T_joint_penalized(a) = T_joint(a) + lambda_row * P_row(a)
```

Here `z_{i,a,r,f}` is a previously frozen normalized source feature for channel `i`, candidate/control alternative `a`, row `r`, and feature `f`.

## What is not being reviewed

Please do not treat this as authorization for any of the following:

- endpoint replay,
- endpoint validation,
- cosmological validation,
- `T_joint` rescoring,
- choosing a numeric `lambda_row`,
- using endpoint residuals or fit improvements,
- accepting Tau Core as a validated physical theory.

The package should remain source-side and protocol-side only.

## Requested task

Open the zip and fill:

```text
data/derived/joint_row_level_numeric_penalty_authorization_review_response_template_v1.csv
```

For each question, provide:

- `review_completed=true`
- a reviewer role or identifier,
- `reviewer_response`
- `reviewer_rationale`
- whether any forbidden inputs were used.

The expected safe path, if you agree, is to authorize only a later package that computes `P_i(a)` and `P_row(a)` values from frozen source features, while keeping `lambda_row` unset or separately predeclared and keeping `T_joint` rescoring forbidden.

## Integrity check

The package SHA256 should be:

```text
ea2f749634a05da53f3984f554bd9d1cf47d5cb7f93a5e0f97e6ba34671da163
```

Claim boundary:

```text
joint_row_level_numeric_penalty_authorization_review_not_scoring_not_validation
```


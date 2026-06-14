# External Reviewer Message: Numeric T_joint Authorization v1

Dear Reviewer,

You do not need repository access for this review. Please use the attached ZIP:

```text
joint_numeric_t_joint_authorization_package_v1.zip
```

This is a narrow authorization review. It asks only whether the already frozen
channel-level numeric `z_i` values may be combined once using the already
frozen symbolic shell:

```text
T_joint = sum_i q_i z_i
```

This review does **not** authorize:

- new endpoint scores,
- new fitting,
- endpoint validation,
- cosmological validation,
- physical validation,
- retuning of `q_i`,
- retuning of signs, centers, scales, or channels.

Inside the ZIP, please read:

- `docs/joint_numeric_t_joint_authorization_reviewer_instructions_v1.md`
- `docs/joint_numeric_t_joint_authorization_package_v1.md`
- `data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv`
- `data/derived/joint_single_statistic_protocol_shell_v1.csv`
- `data/derived/joint_numeric_t_joint_authorization_response_template_v1.csv`

If you authorize the numeric joint ledger, fill the response template using:

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

Please return only the completed CSV, or a ZIP containing the completed CSV.

Claim boundary: this is only permission to compute a numeric joint ledger from
already frozen inputs. It is not evidence for cosmological or physical
validation.

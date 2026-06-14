# Joint Numeric T_joint Control-Suite Review Instructions v1

You do not need repository access. Review only the zip contents.

If accepted, use these exact response tokens:

- `ACCEPT_CONTROL_SUITE_REVIEW_SCOPE_NOT_ENDPOINT_SCORING`
- `ACCEPT_SAME_STATISTIC_CONTROLS_NO_RETUNING`
- `ACCEPT_PREPARE_SEPARATE_ENDPOINT_AUTHORIZATION_PACKAGE`
- `ACCEPT_CAVEAT_PRESERVATION`

If and only if all four rows are accepted, set
`endpoint_scoring_authorization_package_preparation_allowed=true`
on every row. This authorizes preparation of a later package only.

Keep all direct scoring and validation fields false:
`endpoint_scoring_allowed=false`,
`endpoint_validation_claimed=false`,
`cosmological_validation_claimed=false`, and
`physical_validation_claimed=false`.

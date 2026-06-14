# Joint numeric z_i distribution ledger v1

**Doc class:** numeric channel-level distribution ledger
**Status:** z_i distribution built; not T_joint; not scoring; not validation
**Claim boundary:** `joint_numeric_zi_distribution_ledger_not_tjoint_not_scoring_not_validation`

This artifact applies the frozen signed median/MAD rule to each active
channel independently. Centers and scales are computed only from matched
controls. Candidate values do not define center or scale.

The output is a channel-level `z_i` ledger only. It does not compute
`T_joint`, endpoint scores, cosmological validation, or physical
validation.

Channel-level candidate `z_i` values are recorded in:

- `data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv`
- `data/derived/joint_numeric_zi_distribution_ledger_v1.csv`

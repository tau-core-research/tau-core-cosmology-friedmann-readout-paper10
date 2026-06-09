# KiDS-1000 COSEBIs Mapping-To-Template Join Contract V1

This artifact freezes the row-level join contract between a future source-frozen
`W_web/W_path` mapping and the already materialized 300-row COSEBIs
theory-vector template.

It is not a mapping vector, not a theory vector, not a prediction, and not an
endpoint score. The only accepted join key is `row_index_zero_based`, inherited
from the COSEBIs tomographic-pair/mode template. Future source-side mapping
columns must be supplied as source-frozen values before endpoint scoring can be
enabled.

Recorded artifacts:

```text
data/source_manifest/kids1000_cosebis_mapping_template_join_contract_policy_v1.csv
data/derived/kids1000_cosebis_mapping_template_join_contract_v1.csv
data/derived/kids1000_cosebis_mapping_template_join_contract_v1_summary.csv
scripts/build_kids1000_cosebis_mapping_template_join_contract_v1.py
scripts/validate_kids1000_cosebis_mapping_template_join_contract_v1.py
```

Leakage controls: the policy forbids KiDS data-vector values, posterior chains,
lensing residuals, fit-improvement flags, post-hoc theory-vector choice,
post-hoc mapping-row selection, post-hoc channel activation, post-hoc sky
direction selection, post-hoc web-environment labels, and post-hoc path
projection labels.

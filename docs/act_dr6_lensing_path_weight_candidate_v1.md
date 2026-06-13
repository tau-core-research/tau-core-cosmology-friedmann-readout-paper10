# ACT DR6 lensing path-weight candidate v1

This artifact freezes a source-side, unitless observer/path lensing
candidate from ACT DR6 low-resolution kappa sampling. It uses only
mask-positive ACT rows for robust median/MAD normalization and assigns
zero weight outside the ACT baseline mask.

The baseline channel is the science candidate. Curl and f150-f090
difference channels are retained as null controls. The artifact is not
endpoint replay, not validation, and not a physical metric/lensing
path-weight derivation.

- source rows: 424
- mask-positive rows: 168
- corr baseline/curl: -0.0415435390521
- corr baseline/diff_f150_f090: -0.230185832443
- claim boundary: act_dr6_lensing_path_weight_candidate_source_side_not_endpoint_not_validation

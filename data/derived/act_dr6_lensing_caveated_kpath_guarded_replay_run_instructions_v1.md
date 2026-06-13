# ACT DR6 caveated K_path guarded replay package v1

This package is a prepared run bundle, not a replay execution.

The allowed next action is to run the guarded replay only as a
permission-only endpoint diagnostic with all controls retained.

Required controls:

- off
- baseline_only
- curl_null
- diff_f150_f090_null
- wrong_sign
- deterministic_shuffle
- rank_reverse
- source_basis_recenter_stress, if implemented as a frozen stress

Forbidden claims:

- validation
- physical K_path promotion
- dark-sector inference
- family verdict

Claim boundary: `act_dr6_lensing_caveated_kpath_guarded_replay_package_not_scoring`.

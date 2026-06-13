# V2 Observer-Basis Candidate Review Notes v1

## Decision

```text
ACCEPT_OBSERVER_BASIS_CANDIDATE_FOR_SEPARATE_PERMISSION_ONLY_REPLAY_AUTHORIZATION_PACKAGE
```

## Candidate

```text
W_path_x_sky_x_x_zcenter
```

## Scope boundary

This review is a candidate-eligibility review only. It does not authorize endpoint replay and does not claim endpoint validation or a physical lensing-path weight.

Required flags in the completed response remain:

```text
forbidden_inputs_used=false
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
claim_boundary=v2_observer_basis_candidate_review_not_validation
```

## Source-side review findings

- The candidate family is predeclared in the supplied fast-screen family summary and is named as the policy candidate.
- The screen summary identifies it as `best_candidate_family` over 19 families and 9416 grid rows.
- The candidate uses the stated source-side components only: `W_path`, `sky_x`, and centered `zHD`.
- The package scope excludes endpoint replay, endpoint validation, and physical lensing-path-weight claims.
- The diagnostic screen result is caveated source-side evidence only.

## Diagnostic screen values used from the supplied package

```text
n_rows=12
source_row_indices=344;350;374;375;384;448;554;595;603;606;635;701
baseline_best_chi2=5.13167342672
best_candidate_family=W_path_x_sky_x_x_zcenter
best_candidate_chi2=4.55094910859
best_candidate_delta_chi2_minus_baseline=-0.58072431813
best_global_control_family=W_path_x_sky_y_x_zcenter
best_global_control_branch=rank_reverse
best_global_control_chi2=4.5739786714
best_candidate_delta_chi2_minus_best_global_control=-0.02302956281
surviving_family_count=4
surviving_families=W_path_x_centered_sky_yz_plus;W_path_x_sky_x_x_zcenter;W_path_x_sky_yz_plus;W_path_x_sky_z
```

Candidate local family-control row:

```text
family_id=W_path_x_sky_x_x_zcenter
candidate_best_chi2_screen=4.55094910859
best_control_branch=rank_reverse
best_control_chi2_screen=4.63878177658
delta_chi2_candidate_minus_baseline=-0.58072431813
delta_chi2_candidate_minus_best_control=-0.08783266799
controls_better_than_candidate_chi2=0
survives_family_controls=true
```

## Caveats

- This is not endpoint validation.
- This is not population evidence.
- This is not a physical lensing-path proof.
- This is not an authorization to run endpoint replay inside this review packet.
- Any replay must be handled by a separate permission-only replay authorization package.

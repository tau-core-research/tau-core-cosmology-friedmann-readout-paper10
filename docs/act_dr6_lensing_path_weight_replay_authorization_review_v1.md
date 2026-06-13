# ACT DR6 lensing path-weight replay authorization review v1

This package is for an external reviewer who does not have repository access.
The reviewer should decide whether the ACT DR6 source-side path-weight
candidate may proceed to a separate guarded replay.

Review boundaries:

- The package is not endpoint replay.
- The package is not empirical validation.
- The candidate is unitless and source-side; it is not a physical metric/lensing path-weight derivation.
- Curl and f150-f090 difference channels must remain null controls in any later replay.
- Endpoint residuals, endpoint scores, and fit statistics are forbidden inputs for this review.

Claim boundary: `act_dr6_lensing_path_weight_replay_authorization_review_not_validation`.

The reviewer should fill only the `reviewer_answer` and `reviewer_notes` columns
in the response template, then return the completed CSV.

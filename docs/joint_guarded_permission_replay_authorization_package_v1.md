# Joint guarded permission replay authorization package v1

**Doc class:** reviewer handoff package.
**Status:** prepared, not completed.
**Claim boundary:** `joint_guarded_permission_replay_authorization_not_scoring_not_validation`.

This package asks whether a guarded permission-only joint replay package may be prepared.
It is not scoring, not endpoint validation, and not cosmological validation.

The upstream scoring-authorization review allows only a separate guarded package.
Candidate and controls must use the same block-diagonal statistic and covariance blocks.

Mandatory caveats carried forward:
- no source-native cross-probe covariance product is available;
- block-diagonal independence is caveated;
- shared sky/mask, redshift-kernel, cosmology/nuisance, calibration, and population covariance caveats remain active;
- direct execution remains forbidden until a separate run-template gate is built and validated.

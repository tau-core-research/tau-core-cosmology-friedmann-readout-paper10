# Joint cross-probe covariance closure review package v1

**Doc class:** external source-side review handoff
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_cross_probe_covariance_closure_review_not_scoring_not_validation`

This package addresses the blocker left open by the block-diagonal
independence review. It asks whether the joint Paper10 route can close
the cross-probe covariance/independence condition without using endpoint
residuals, endpoint scores, fit improvements, posterior chains, or
post-score control ranks.

Current machine state:

- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- covariance gate verdict: `JOINT_COVARIANCE_MODEL_REQUIREMENTS_PARTIAL_BLOCKS_READY_CROSS_PROBE_BLOCKED`
- block-diagonal review decision: `JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_ALLOWED_CROSS_PROBE_OPEN_NOT_SCORING`
- block-diagonal shell verdict: `JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_FROZEN_COVARIANCE_STILL_OPEN_NOT_SCORING`
- cross-probe covariance defined: `false`
- block-diagonal shell executable: `false`
- endpoint scoring allowed: `false`

Allowed closure routes:

1. **Covariance-product route:** identify a source-native or source-frozen
   cross-probe covariance product with dimensional scope and provenance.
2. **Independence-rationale route:** justify a caveated block-diagonal
   approximation from source-side probe design, redshift/sky/nuisance
   separation, and known calibration overlap limits.

Neither route authorizes scoring by itself. A separate scoring/replay
authorization must be created after source-side closure, if closure is accepted.

Reviewer instruction:

- Fill `data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv`.
- Do not use endpoint residuals, new endpoint scores, fit improvements,
  posterior chains, or post-score control ranks.
- If keeping the blocker open, state the missing source-side evidence.

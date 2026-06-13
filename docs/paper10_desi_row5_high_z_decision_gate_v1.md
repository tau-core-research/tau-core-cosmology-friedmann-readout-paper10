# Paper10 DESI Row5 High-z Decision Gate v1

This gate converts the external row-5 high-z source review into a machine-readable route state.

It is deliberately not an endpoint replay gate. A completed positive review can at most reopen source-side work or request a separate replay-authorization package. The gate never permits endpoint scoring, endpoint validation, or physical validation.

Inputs:

- `data/source_manifest/paper10_desi_row5_high_z_decision_gate_policy_v1.csv`
- `data/derived/paper10_desi_row5_high_z_review_package_v1_summary.csv`
- optional `data/derived/paper10_desi_row5_high_z_review_response_v1_summary.csv`

Outputs:

- `data/derived/paper10_desi_row5_high_z_decision_gate_v1.csv`
- `data/derived/paper10_desi_row5_high_z_decision_gate_v1_summary.csv`

Allowed states:

- `ROW5_HIGH_Z_REVIEW_PENDING_NOT_REPLAY`
- `ROW5_HIGH_Z_BLOCKER_REMAINS_NOT_REPLAY`
- `ROW5_SOURCE_REOPEN_NO_REPLAY`
- `ROW5_SOURCE_REOPEN_REPLAY_REVIEW_REQUIRED_NOT_REPLAY`

Current imported state:

`ROW5_HIGH_Z_BLOCKER_REMAINS_NOT_REPLAY`

The completed source-blocker review identifies no independent high-z clock
source and no source-native time/readout observable covering `z=2.33`.
Ly-alpha BAO remains cross-probe context only, not clock support.

Claim boundary:

`paper10_desi_row5_high_z_decision_gate_not_validation`.

No residuals, scores, fit statistics, or endpoint results are read by this gate.

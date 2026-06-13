# DESI Shape Validation-Oriented Permission Replay Authorization Review V1

**Doc class:** final permission-only replay authorization handoff.

**Reader role:** external reviewer without repository access.

**Status:** blank authorization package; not completed; not replay; not
validation.

**Canonical parent:** `paper10_desi_shape_validation_oriented_gate_review_v1.md`.

The DESI shape route has passed a staged source-side and gate-preparation chain,
but it has not been promoted to validation. The current state is:

```text
route_candidate_score = 5.52425578108
route_best_control_score = 5.50939872844
route_margin = 0.01485705264
robustness_verdict = positive_but_narrow_margin_and_row_sensitive_not_validation
source_synthesis_decision =
  ACCEPT_AS_SOURCE_SYNTHESIS_SUPPORT_FOR_FUTURE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION
post_synthesis_decision =
  ACCEPT_PREPARE_SEPARATE_VALIDATION_ORIENTED_GATE_PACKAGE_NOT_REPLAY_NOT_VALIDATION
validation_oriented_gate_decision =
  GO_DESI_SHAPE_VALIDATION_ORIENTED_PERMISSION_REPLAY_ONLY
endpoint_replay_allowed = false
endpoint_validation_claimed = false
physical_validation_claimed = false
```

This handoff asks the reviewer one narrow question: may one frozen
permission-only diagnostic replay be run under the validation-oriented DESI
shape-route scope?

## Proposed Replay Scope

The proposed scope is limited to:

- the already frozen DESI shape-route candidate and controls;
- the already imported source-synthesis and post-synthesis gate responses;
- the validation-oriented gate response, including all retained caveats;
- one future permission-only diagnostic replay, if separately authorized by the
  completed response to this package.

The package does not contain endpoint residuals, new endpoint scores, posterior
chains, late-time fitted parameters, or any post-hoc shape/control choices. It
also does not authorize validation language.

## Caveats That Must Remain Active

The completed validation-oriented gate response explicitly retained:

- narrow-margin caveat;
- row-sensitive robustness caveat;
- Row2 negative-diagnostic caveat.

Any positive response to this package must keep those caveats active. A replay
authorized here would be permission-only diagnostic evidence, not endpoint
validation and not physical validation.

## Claim Boundary

```text
paper10_desi_shape_validation_permission_replay_authorization_not_validation
```

# Joint guarded replay execution authorization package v1

This package asks whether the prepared runner may be executed once as a
permission-only replay.  It does not itself execute the runner.

Any accepted result must remain permission-only, not endpoint validation,
not cosmological validation, and not physical proof.

Claim boundary: `joint_guarded_replay_execution_authorization_not_validation`.

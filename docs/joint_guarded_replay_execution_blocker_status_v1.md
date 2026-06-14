# Joint guarded replay execution blocker status v1

This ledger records the current execution blocker for the joint guarded replay path.
It is not a replay, not endpoint scoring, and not cosmological validation.

Current blocker: `permission_only_replay_completed_not_validation`.
Next required action: `preserve_outputs_and_do_not_promote_to_validation_without_new_protocol`.

This ledger remains non-validation even after a permission-only replay.
Endpoint scoring and cosmological validation require a separate protocol.

Claim boundary: `joint_guarded_replay_execution_blocker_status_not_execution_not_scoring_not_validation`.

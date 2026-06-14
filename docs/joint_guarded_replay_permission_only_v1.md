# Joint guarded replay permission-only v1

This artifact records a permission-only guarded replay, not endpoint validation
and not cosmological validation.

The replay is allowed only when the separate execution authorization response
is imported and validates `permission_only_execution_allowed=true`.

Claim boundary: `joint_guarded_replay_permission_only_not_validation`.

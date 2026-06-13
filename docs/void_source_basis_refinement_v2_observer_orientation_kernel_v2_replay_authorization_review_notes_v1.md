# Observer-orientation kernel v2 replay authorization review notes

## Decision

```text
GO_OBSERVER_ORIENTATION_V2_REPLAY_PERMISSION_ONLY
```

## Scope

This review authorizes exactly one later, predeclared replay of:

```text
K_v2 = W_path * (sky_z - mean_sky_z_scope)
```

on the frozen 12-row partial path scope only.

## Accepted source-side conditions

- The V2 kernel is frozen source-side as `W_path_times_centered_sky_z`.
- Inputs remain limited to RA, DEC, the frozen `W_path` source value, and the predeclared 12-row scope.
- The centering rule is source-side monopole removal over the same 12 rows, not a residual- or score-fitted rule.
- Required controls are preserved: `off`, `wrong_sign`, `deterministic_shuffle`, `rank_reverse`, `axis_x_reference`, `axis_y_reference`.
- `axis_x_reference` and `axis_y_reference` remain controls only, not post-hoc replacements.

## Boundary flags

```text
review_completed=true
forbidden_inputs_used=false
endpoint_replay_allowed=true
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
authorization_scope=single_permission_only_12_row_observer_orientation_kernel_v2_replay_not_validation
claim_boundary=v2_observer_orientation_kernel_v2_replay_authorization_not_validation
```

## Non-claims

This is not endpoint validation, not endpoint scoring, not population evidence, not a physical lensing-path proof, not new gravitational-law evidence, and not post-hoc sky-direction tuning.

## Checks performed on local package copy

- Inner ZIP sidecar SHA-256 matched.
- Package manifest byte counts and SHA-256 values matched all listed files.
- Manifest forbidden endpoint/validation flags remained false.
- Packaged template validator accepted the uncompleted template state.
- Source-side kernel consistency was checked for 12 rows, `mean_sky_z_scope`, primary/reference sign counts, and the relation `K_primary_raw = W_path * centered_sky_z`.
- Completed response check passed.

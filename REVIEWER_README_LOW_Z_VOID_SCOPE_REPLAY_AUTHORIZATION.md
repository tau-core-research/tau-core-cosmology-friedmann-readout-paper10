# Low-z Pantheon Void Replay Authorization Review

This package is a permission-only reviewer handoff for a possible future
low-redshift Pantheon void replay. It is not an endpoint run and it is not a
validation claim.

## First Checks

If you received the ZIP and `.zip.sha256` sidecar together, place both files in
the same directory and run:

```bash
shasum -a 256 -c low_z_pantheon_void_scope_replay_authorization_review_package_v1.zip.sha256
```

Expected result:

```text
low_z_pantheon_void_scope_replay_authorization_review_package_v1.zip: OK
```

## Start Here

Read:

```text
docs/low_z_pantheon_void_scope_candidate_v1.md
docs/void_channel_remediation_gate_v1.md
docs/void_source_basis_audit_v1.md
```

Complete:

```text
data/derived/low_z_pantheon_void_scope_replay_authorization_review_response_template_v1.csv
```

## Boundary

Do not inspect or use endpoint residuals, endpoint scores, fit statistics,
post-hoc row selection, post-hoc amplitude tuning, or post-hoc channel
promotion. A completed review can only authorize or reject one future,
predeclared low-z Pantheon void replay. It cannot validate Tau Core cosmology,
the void channel, or the previous full-Pantheon combined endpoint.

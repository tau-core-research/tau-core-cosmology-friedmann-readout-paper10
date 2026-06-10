# Low-z Pantheon Void Scope Candidate v1

## Status

This is a scope-candidate artifact for the low-redshift route allowed by the
void-channel remediation gate. It is not endpoint scoring and does not claim
physical validation.

## Why this exists

The current void source basis is low-redshift and volume-limited. The full
Pantheon distance block extends far beyond that support, so the full-Pantheon
void endpoint remains blocked. A claim-safe next step is to freeze which
Pantheon rows would be eligible for a future low-z void replay before any
endpoint score is run.

## Row rule

Rows are included only when both conditions hold:

1. `zHD <= void_catalog_z_support_max_proxy`
2. `W_void_source_native_basis > 0`

The current support cap is inherited from `VOID_CHANNEL_REMEDIATION_GATE_V1`.

## Outputs

```text
data/source_manifest/low_z_pantheon_void_scope_candidate_policy_v1.csv
data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv
data/derived/low_z_pantheon_void_scope_candidate_v1_summary.csv
scripts/build_low_z_pantheon_void_scope_candidate_v1.py
scripts/validate_low_z_pantheon_void_scope_candidate_v1.py
```

## Claim boundary

This artifact freezes an eligible low-z scope candidate only:

`low_z_void_scope_candidate_not_scoring_not_validation`

It does not select amplitudes, does not compare branches, does not score
residuals, and does not authorize an endpoint run.

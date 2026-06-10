# Void/Web Combined Endpoint Diagnostics v1

## Status

This is a diagnostic artifact for the authorized combined void/web endpoint run.
It is not a validation result and does not promote the void/web branch.

## Diagnostic Result

The combined source-native void/web candidate improves chi-square only weakly,
loses under AIC/BIC, and does not beat the deterministic shuffled void/web
control.

The more specific diagnostic is:

`void_channel_inactive_and_shuffled_control_marginally_better`

At the best candidate point:

- `omega_void = 0`
- `mu_web = -0.1`
- `candidate_equals_web_only_chi2 = true`
- `candidate_delta_chi2_vs_baseline = -0.32825117`
- `candidate_delta_aic_vs_baseline = 3.67174883`
- `shuffled_minus_candidate_chi2 = -0.0112178400002`

## Interpretation

The combined endpoint does not currently demonstrate a robust void/web signal.
Its best candidate effectively collapses to a web-only branch, while the
deterministic shuffled branch remains marginally better. Therefore the failure
mode is not simply "the branch is zero"; rather, the present void source basis
and shared-amplitude grammar are not yet strong enough to distinguish the
source-native void/web family from a shuffled control.

## Next Claim-Safe Action

Do not promote the endpoint result. The next step is to diagnose the void source
basis and the shared void/web amplitude grammar before any new endpoint claim.
Possible follow-up checks are:

- whether the current void source-native basis is too weak after the FLRW
  consistency audit;
- whether the shared-amplitude grammar suppresses the void channel;
- whether distance-only improvement is being diluted by growth/BAO blocks;
- whether path/time channels are genuinely required before a combined
  cosmological endpoint can be expected to pass.

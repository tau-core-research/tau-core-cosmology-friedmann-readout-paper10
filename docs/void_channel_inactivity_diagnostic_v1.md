# Void Channel Inactivity Diagnostic v1

## Status

This diagnostic follows the weak/negative combined void/web endpoint result. It
does not reopen endpoint scoring and does not claim physical validation.

## Result

The void channel is inactive at the best combined candidate point. The combined
candidate collapses to the web-only branch:

- `combined_candidate_void_channel_active_at_best = false`
- `combined_candidate_equals_web_only_chi2 = true`

The source-native void basis also has much narrower support than the web basis
in the Pantheon design matrix:

- `void_nonzero_fraction = 0.310722100656`
- `web_nonzero_fraction = 0.972283005106`

Under the frozen void-only profiles, every non-zero `omega_void` value worsens
relative to `omega_void=0`. The least bad non-zero combined-profile case is:

- `omega_void = 0.1`
- `delta_chi2_vs_omega_void_zero = 0.16283019`

## Diagnostic Verdict

`void_basis_has_limited_support_and_nonzero_void_amplitudes_do_not_improve_frozen_profiles`

## Interpretation

The combined endpoint did not fail merely because the effect is numerically
zero. It failed because the currently frozen source-native void mapping is too
weak or misaligned to survive the endpoint grammar: the best model suppresses
the void channel, and non-zero void amplitudes are disfavored in both the
distance-only and combined profiles.

The claim-safe next step is to audit the void mapping rule and void source basis
before reopening endpoint scoring. In particular, the current low-redshift
comoving-distance bin proxy and cumulative void-load rule may be too coarse for
the multi-block endpoint.

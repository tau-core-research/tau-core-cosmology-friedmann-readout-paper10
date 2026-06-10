# Low-z Pantheon Void Scope Replay Authorization Review v1

## Purpose

This review asks whether the frozen low-z Pantheon void-scope candidate is
sufficiently source-side and leakage-safe to authorize one future replay.

It does not run the replay and does not claim validation.

## Required reviewer checks

The reviewer must confirm:

1. the low-z row mask is frozen before scoring;
2. the route is justified by the low-z void catalogue support limitation;
3. the authorization can be made without endpoint residuals, scores, fit
   statistics, post-hoc row selection, or post-hoc amplitude tuning;
4. any approval is permission for one replay only, with
   `physical_validation_claimed=false`.

## Claim boundary

`low_z_void_scope_replay_authorization_review_not_validation`

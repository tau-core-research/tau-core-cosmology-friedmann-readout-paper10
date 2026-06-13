# DESI clock-support blocker external review notes v1

## Decision

`PARTIAL_SOURCE_ACQUISITION_REOPEN_ROW4_KEEP_ROW5_BLOCKED_NO_REPLAY`

## Scope

This review is source-side only. It does not authorize endpoint replay, endpoint validation, physical validation, residual scoring, late-time parameter fitting, or post-hoc clock smoothing.

Claim boundary:

`paper10_desi_clock_support_blocker_external_review_not_validation`

## Findings

### Q1 / radial row 4, z_eff = 1.484

Decision:

`CAVEATED_YES_ROW4_SOURCE_ACQUISITION_GATE_CAN_REOPEN`

Rationale: the checked cosmic-chronometer table contains direct CC H(z) entries at `z=1.43` and `z=1.53`, bracketing the row-4 target `z_eff=1.484`. This is enough to reopen source acquisition for row 4, but not enough to authorize replay or claim validation.

### Q2 / radial row 5, z_eff = 2.33

Decision:

`NO_ROW5_REMAINS_BLOCKED_CLOCK_SUPPORT_NOT_FROZEN`

Rationale: DESI Ly-alpha BAO provides high-redshift BAO context above redshift two, but it is not itself an independent clock/chronometer or source-native time-readout source. The checked CC/source-native clock material does not cover or bracket `z=2.33` without extrapolation. Row 5 therefore remains blocked.

### Q3 / BAO-RSD-Ly-alpha control status

Decision:

`YES_KEEP_BAO_RSD_LYA_AS_CONTEXT_CONTROLS_UNLESS_CLOCK_ATTACHED`

BAO/RSD/Ly-alpha BAO material may remain useful as cross-probe context/control evidence, but it should not be promoted to clock-support evidence unless independent chronometer/source-native time-readout evidence is attached.

### Q4 / source-side boundary

Decision:

`YES_SOURCE_SIDE_ONLY_NO_ENDPOINT_REPLAY_AUTHORIZED`

Forbidden-input and validation flags remain false.

## Boundary flags

```text
forbidden_inputs_used=false
endpoint_replay_authorized=false
endpoint_validation_claimed=false
physical_validation_claimed=false
```

## External source notes used for source-side context

- Moresco 2023 cosmic chronometer review/table: CC method derives H(z) from differential age-redshift information; table includes nearby entries at z=1.43 and z=1.53.
- DESI DR2 guide/papers: Ly-alpha BAO is high-redshift BAO context above z>2, not source-native clock evidence by itself.

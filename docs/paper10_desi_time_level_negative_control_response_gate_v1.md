# DESI Time-Level Negative-Control Response Gate V1

**Doc class:** negative-control response gate; source-side next-action ledger.

**Reader role:** Paper 10 endpoint auditor.

**Status:** route blocked pending richer source-side clock/readout support; not
endpoint replay; not validation.

**Canonical parent:** `paper10_desi_time_level_negative_control_diagnostic_v1.md`.

This gate records the consequence of the DESI/chronometer five-row negative
control diagnostic. It deliberately does not tune the candidate, change the row
set, smooth the chronometer table, or open a new endpoint replay.

## Preserved Failure Mode

```text
five_row_time_level_constant_beta_endpoint_is_ordering_fragile
```

The diagnostic shows that the candidate constant-level fit is not distinctive:
four frozen controls beat the candidate in chi-square, and the best branch is
the deterministic redshift-order shuffle control.

## Exit Conditions Before Any Future DESI Time-Level Replay

Any future replay attempt must satisfy all of the following before a separate
permission-only authorization is even considered:

```text
preserve_negative_control
no_posthoc_beta_or_row_tuning
independent_clock_support_beyond_nearest_neighbor_5row_scope
source_frozen_time_readout_observable_beyond_constant_beta_level
predeclared_ordering_and_leave_row_controls
separate_permission_only_authorization_before_any_replay
```

## Forbidden Inputs

```text
endpoint_residuals
endpoint_scores
late_time_fit_parameters
posthoc_row_selection
posthoc_control_selection
posthoc_beta_retuning
posthoc_cc_smoothing
validation_language
```

## Next Allowed Action

```text
build_source_side_time_readout_expansion_manifest_only
```

This means the next step is not a replay. The next step is a source-side
manifest that identifies which additional independent clock/readout observables
would be required to reopen the DESI time-level route without leakage.

## Artifacts

```text
data/source_manifest/paper10_desi_time_level_negative_control_response_gate_v1.csv
data/derived/paper10_desi_time_level_negative_control_response_gate_v1.csv
data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv
scripts/build_paper10_desi_time_level_negative_control_response_gate_v1.py
scripts/validate_paper10_desi_time_level_negative_control_response_gate_v1.py
```

## Claim Boundary

```text
paper10_desi_time_level_negative_control_response_gate_not_validation
```

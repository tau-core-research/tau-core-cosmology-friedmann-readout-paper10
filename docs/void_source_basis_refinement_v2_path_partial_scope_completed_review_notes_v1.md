# V2 Path Partial-Scope Review Notes v1

## Decision

```text
ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE
```

## Scope accepted

The supplied `W_path` partial-scope material is acceptable only as a caveated source-side control for the predeclared 12 candidate rows.

Accepted reading:

```text
partial_scope_12_row_W_path_source_side_control_only
```

## Key source-side facts checked

- Low-z scope rows: `424`.
- Strict path-scope candidates: `5`.
- Caveated path-scope candidates: `7`.
- Total partial-scope candidates: `12`.
- Rows not path-scope eligible: `412`.
- Partial path values computed: `true`.
- Full low-z path values computed: `false`.
- Full low-z scope path ready: `false`.
- Nonzero partial `W_path` values: `12`.
- Candidate `W_path_source_value` range: `6.129006671360e-02` to `4.420864334176e-01`.

## Review item responses

```text
Q1_NO_ENDPOINT_LEAKAGE = yes
Q2_SCOPE_LABELS = caveated_yes
Q3_VALUE_RULE = caveated_yes
Q4_FUTURE_REPLAY_PACKAGE = caveated_yes
FINAL_VERDICT = ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE
```

## Caveats preserved

```text
forbidden_inputs_used=false
endpoint_replay_allowed=false
endpoint_validation_claimed=false
physical_lensing_path_weight_claimed=false
full_lowz_W_path_channel_enabled=false
```

The accepted rule is source-only and residual-blind:

```text
P_tile = max(0, (2 deg - nearest_tile_sep_deg) / 2 deg)
W_path = P_tile / (1 + abs(P_tile))
```

This remains a bounded tile-proximity control, not a calibrated physical lensing-path weight.

## What this permits

The authors may prepare a separate partial-scope replay authorization package using the frozen 12-row source-side labels and values.

## What this does not permit

This review does not authorize endpoint replay, endpoint scoring, endpoint validation, post-hoc tuning, a full low-z `W_path` channel, or any physical lensing-path weight claim.

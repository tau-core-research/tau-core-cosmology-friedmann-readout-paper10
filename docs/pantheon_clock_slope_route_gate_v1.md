# Pantheon clock-slope route gate v1

**Doc class:** source-side route gate
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time/readout source audit

This gate records the next focused time/readout route after the wider
CC-support fast screen.

The route does not promote the CC-support fast screen to validation. It only
freezes the following interpretation:

- `clock_slope` is the best candidate family in the CC-support screen;
- `clock_slope` improves over the baseline;
- `clock_slope` survives its own local family controls;
- the route remains endpoint-blocked because a global `rank_reverse/clock_level`
  control is still better.

Tau Core motivation:

`clock_slope` is closer to a time/readout channel than `clock_level`, because it
tracks the local rate of change of the expansion readout,
`d log H / d log(1+z)`, rather than the background clock level itself. The
`clock_phase` product is retained as a useful mixed control but is not selected
as the primary route.

Allowed next step:

```text
reviewer_gated_clock_slope_only_route_candidate
```

Forbidden next step:

```text
endpoint_replay_or_validation_without_global_control_resolution
```

Claim boundary:

```text
clock_slope_route_gate_source_side_not_replay_not_validation
```

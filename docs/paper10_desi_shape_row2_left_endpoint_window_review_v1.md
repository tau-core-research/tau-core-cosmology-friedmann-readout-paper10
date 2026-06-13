# Paper10 DESI shape row2 left-endpoint window review v1

**Doc class:** external source-window review handoff
**Reader role:** independent source-side reviewer
**Status:** blank reviewer package, not replay, not validation
**Canonical parent:** Paper10 DESI shape-route replay chain

This handoff asks a narrow source-side question:

> Should the relaxed independent row-2 left-endpoint near-misses be retained as
> caveated source-window context, or should the frozen strict
> `|Delta z| <= 0.05` endpoint window remain closed?

The current frozen state is:

- Row 2 left endpoint: `z=0.934`, current endpoint family `Simon et al.`
- Strict endpoint window: `|Delta z| <= 0.05`
- Relaxed context window: `|Delta z| <= 0.10`
- Strict independent left support count: `0`
- Relaxed independent left near-misses:
  - `Stern et al. (2010)`, `z=0.88`, `|Delta z|=0.054`
  - `Moresco et al. (2012)`, `z=0.8754`, `|Delta z|=0.0586`

The reviewer must not use endpoint residuals, endpoint scores, fitted
late-time parameters, posterior chains, post-hoc clock smoothing, or validation
language. A positive response can only reopen source-side acquisition or
trigger a separate promotion review. It cannot authorize endpoint replay.

Allowed current claim:

```text
paper10_desi_shape_row2_left_endpoint_window_review_not_validation
```

# Paper 10 time-level r_d policy selection gate v1

**Doc class:** source-side nuisance-policy selection gate
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time-level route nuisance/interface freeze plan

This gate records which \(r_d\) policy is allowed for the current
`time_level_route`.

Current accepted route:

```text
rd_cancelled_differential_direction
```

This route uses only the two-point differential identity

```text
Delta[-log(D_H/r_d)] = Delta[log H]
```

and is therefore allowed only as a directional source-side check.

Future routes:

- `external_rd_prior`: requires a frozen external \(r_d\) prior artifact;
- `analytic_rd_marginalization`: requires a frozen BAO marginalization protocol.

Forbidden route:

```text
fit_rd_from_pantheon_residuals
```

This is explicitly forbidden because it would leak endpoint residual information
into the nuisance parameter that defines the time-level route.

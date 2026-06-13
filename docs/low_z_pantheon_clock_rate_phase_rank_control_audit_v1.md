# Low-z Pantheon clock-rate phase rank-control audit v1

**Doc class:** source-side diagnostic audit
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 R6 time/readout source audit

This audit explains why the source-frozen clock-rate/phase fast screen is not
control-resistant. It does not introduce a new kernel and does not authorize
endpoint replay.

The low-z Pantheon clock-rate/phase basis is built from the fetched cosmic
chronometer support table, but the low-z rows occupy only three assigned CC
support bins. Consequently the basis vectors are coarse. The diagnostic does
not claim that the vectors are perfectly redshift-order encoded; it checks the
weaker and directly relevant fact that the rank-reversed controls dominate the
local fast-screen controls.

The diagnostic checks:

- assigned CC-bin count and row counts per bin;
- unique basis values per clock family;
- Pearson and Spearman correlations with `zHD` and `source_row_index`;
- correlation with the deterministic `rank_reverse` control;
- whether the best local control is still `rank_reverse`.

The expected claim boundary is:

```text
clock_rate_phase_rank_control_audit_source_side_not_scoring_not_validation
```

Interpretation:

- a positive candidate-minus-baseline improvement in the fast screen remains a
  useful source-side signal;
- the rank-reverse win means the present low-z clock-rate/phase basis is not
  specific enough for endpoint replay, even though the redshift/order
  correlations are only moderate rather than total;
- the next honest path is either a wider redshift support, or an independent
  clock/readout observable that is not reducible to low-z bin order.

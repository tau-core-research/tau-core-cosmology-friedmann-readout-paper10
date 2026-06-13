# Paper 10 joint CC+BAO time-route consistency audit v1

**Doc class:** source-side route consistency audit
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time/readout route synthesis gate

This audit asks a narrow source-side question:

```text
Do the two radial BAO DH/rd time-observable points agree directionally with
the CC logH level route or the CC dlogH/dlog(1+z) slope route?
```

The audit uses only source-side products:

- the frozen cosmic-chronometer H(z) table;
- the frozen SDSS radial BAO `DH_over_rd` rows;
- nearest CC support at each BAO redshift;
- two-point normalized direction comparisons.

It does not use Pantheon residuals, endpoint scores, late-time fit parameters,
or post-hoc smoothing.

Current result:

```text
radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay
```

Interpretation:

Radial BAO supplies an independent expansion-level time observable, but it does
not currently strengthen the CC `clock_slope` route. With only two BAO points
and unresolved \(r_d\), this is underresolved and cannot authorize replay.

Claim boundary:

```text
source-side route consistency only;
not endpoint replay;
not validation;
not a Tau Core time-projection proof.
```

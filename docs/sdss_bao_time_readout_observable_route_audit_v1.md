# SDSS radial BAO time/readout observable route audit v1

**Doc class:** source-side route audit
**Status:** not endpoint replay, not validation
**Canonical parent:** Paper 10 time/readout source audit

This audit checks whether the existing SDSS multi-tracer BAO/RSD products
contain an independent time/readout observable route.

The relevant observable is radial BAO:

```text
D_H / r_d = c / (H(z) r_d)
```

Therefore, up to the unresolved sound-horizon nuisance \(r_d\),
`-log(DH_over_rd)` is a source-side proxy for `log H(z)`.

Result:

- available radial BAO rows: 2;
- redshift bins: `z_eff = 0.700, 0.845`;
- independent of Pantheon distance residuals;
- independent of the CC `clock_level` route;
- not endpoint-ready because the route has only two bins and leaves the
  \(r_d\) nuisance unresolved.

Interpretation:

This is a useful source-side route discovery. It supports the idea that a
non-CC time/readout observable exists in the current source base. It does not
authorize replay and does not validate a Tau Core time/readout kernel.

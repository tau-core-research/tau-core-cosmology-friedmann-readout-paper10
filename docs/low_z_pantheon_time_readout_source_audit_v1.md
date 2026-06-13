# Low-z Pantheon+ time/readout source audit v1

**Doc class:** source-side route/coverage audit
**Reader role:** Paper 10 full observer/path kernel claim-boundary audit
**Status:** partial source routes available; no numeric `W_time`
**Canonical parent:** `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`

This artifact addresses R6 of the full observer/path kernel requirements gate.
It updates the older route-ledger picture by checking the currently frozen
source products:

- the cosmic-chronometer `H(z)` table is fetched and frozen;
- SDSS DR16 multi-tracer BAO/RSD products are fetched and frozen;
- the Planck/LAMBDA CMB route page is cached.

The audit does not compute a time/readout kernel.  In particular, it does not
derive or freeze:

- `Delta_clock`,
- `Delta_clock_star`,
- a redshift-bin phase rule,
- a numeric `W_time`,
- a late-time fit parameter.

Run:

```bash
python scripts/build_low_z_pantheon_time_readout_source_audit_v1.py
python scripts/validate_low_z_pantheon_time_readout_source_audit_v1.py
```

Outputs:

- `data/derived/low_z_pantheon_time_readout_source_audit_v1.csv`
- `data/derived/low_z_pantheon_time_readout_source_audit_v1_summary.csv`

Claim boundary:

```text
time_readout_source_audit_source_side_not_scoring_not_validation
```

Interpretation:

R6 is now route-grounded more strongly than before: independent chronometer,
BAO/RSD, and CMB route families are present.  It is still not activation-ready,
because the Tau Core time/readout phase scale and numeric rule remain
unfrozen.

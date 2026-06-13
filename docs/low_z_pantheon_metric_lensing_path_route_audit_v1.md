# Low-z Pantheon+ metric/lensing path route audit v1

**Doc class:** source-side route/coverage audit
**Reader role:** Paper 10 full observer/path kernel claim-boundary audit
**Status:** route available; numeric metric/lensing path observable missing
**Canonical parent:** `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`

This artifact addresses R5 of the full observer/path kernel requirements gate.
It intentionally does not construct a physical lensing-path weight.  Instead it
records which source-side lensing routes are already present and why the R5
kernel remains blocked.

Inputs:

- low-z Pantheon+ source positions from `low_z_pantheon_void_geometry_join_v1`;
- KiDS DR4.1 path-mask tile inventory;
- cached public KiDS weak-lensing route page;
- cached public CMB-lensing route page;
- KiDS-1000 lensing product inventory.

For each low-z Pantheon+ row, the audit records the nearest KiDS tile by
filename-coordinate proxy and its angular separation.  This is a coverage/route
diagnostic only.  It does not compute:

- convergence,
- shear,
- lensing residuals,
- mass-map integral,
- metric/null-geodesic path weight.

Run:

```bash
python scripts/build_low_z_pantheon_metric_lensing_path_route_audit_v1.py
python scripts/validate_low_z_pantheon_metric_lensing_path_route_audit_v1.py
```

Outputs:

- `data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1.csv`
- `data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1_summary.csv`

Claim boundary:

```text
metric_lensing_path_route_audit_source_side_not_scoring_not_validation
```

Interpretation:

R5 is route-grounded but not observable-grounded.  Public KiDS/CMB lensing
routes and KiDS tile coverage information are present, but the required
source-aligned metric/lensing path product is still missing.

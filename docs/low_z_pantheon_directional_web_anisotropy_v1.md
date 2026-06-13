# Low-z Pantheon+ directional web anisotropy v1

**Doc class:** source-side observable note
**Reader role:** Paper 10 reproducibility / claim-boundary audit
**Status:** partial source observable; not endpoint replay; not validation
**Canonical parent:** `data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv`

This artifact is the first R4 upgrade for the full observer/path kernel
requirements gate.  It does not score cosmological models.  It computes a
source-side directional web observable from the SDSS DR17 MCPM slime-mold
catalogue for the 424 low-redshift Pantheon+ rows selected by the low-z void
scope.

For each source, the script uses the source/host sky position, a fixed
2 degree cone, and a frozen redshift window of `[-0.03,+0.03]` around the
source redshift.  Inside that cone it computes:

- web catalogue support count,
- mean and median `matterDens`,
- tangent-plane density-weighted dipole amplitude,
- tangent-plane density-weighted quadrupole amplitude and orientation.

The output is a directional web proxy, not a physical path tensor.  It is not a
metric/lensing-weighted null-geodesic-bundle calculation and it does not
authorize endpoint replay.

Run:

```bash
python scripts/build_low_z_pantheon_directional_web_anisotropy_v1.py
python scripts/validate_low_z_pantheon_directional_web_anisotropy_v1.py
```

Outputs:

- `data/derived/low_z_pantheon_directional_web_anisotropy_v1.csv`
- `data/derived/low_z_pantheon_directional_web_anisotropy_v1_summary.csv`

Claim boundary:

```text
directional_web_anisotropy_source_side_not_scoring_not_validation
```

Interpretation:

This partially improves R4 from a scalar local web proxy to a source-centered
directional web anisotropy observable.  It remains incomplete because it does
not contract a full cosmic-web tensor with the observer-source path and does
not include metric/lensing path weighting.

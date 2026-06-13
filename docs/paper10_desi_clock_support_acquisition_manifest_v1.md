# DESI Clock-Support Acquisition Manifest v1

This is a source-side acquisition manifest, not an endpoint replay and not a
validation result.

The DESI time-readout route is currently blocked by two clock-support gaps:

1. DESI radial row 4 at `z_eff=1.484` has two relaxed-window clock entries but
   only one independent reference family.
2. The excluded DESI high-redshift radial row at `z_eff=2.33` is not covered or
   bracketed by the frozen cosmic-chronometer support without extrapolation.

The manifest freezes these targets before any source fetch or reviewer handoff.
It is intended to keep the next data-acquisition step narrow and auditable.

## Artifacts

- `data/source_manifest/paper10_desi_clock_support_acquisition_manifest_policy_v1.csv`
- `data/derived/paper10_desi_clock_support_acquisition_manifest_v1.csv`
- `data/derived/paper10_desi_clock_support_acquisition_manifest_v1_summary.csv`
- `scripts/build_paper10_desi_clock_support_acquisition_manifest_v1.py`
- `scripts/validate_paper10_desi_clock_support_acquisition_manifest_v1.py`

## Claim Boundary

The claim boundary is:

`paper10_desi_clock_support_acquisition_manifest_not_validation`

Forbidden inputs remain forbidden:

- endpoint scores
- endpoint residuals
- late-time fit parameters
- post-hoc clock choice
- post-hoc cosmic-chronometer outlier removal
- post-hoc cosmic-chronometer smoothing
- validation language

The manifest does not fetch new sources. It does not authorize endpoint replay.

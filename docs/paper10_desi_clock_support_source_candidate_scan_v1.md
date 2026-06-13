# DESI Clock-Support Source Candidate Scan v1

This artifact records a source-side scan for the two DESI clock-support
acquisition targets. It is not an endpoint replay, not a source fetch into the
endpoint route, and not validation.

The scan keeps the two acquisition targets frozen:

- radial row `4`, `z_eff=1.484`, requiring an independent clock source near the
  row that is not another Simon et al. (2005) entry;
- radial row `5`, `z_eff=2.33`, requiring high-redshift clock or source-native
  time-readout support without extrapolating the frozen CC table.

## Outcome

The first pass identifies useful context sources, but no gate-closing clock
support:

- The eBOSS DR16 QSO BAO/RSD route is close to row 4 at `z_eff=1.48`, but it is
  a BAO/RSD clustering route rather than an independent clock measurement, so it
  is retained only as a row-4 cross-probe control.
- Tomasetti et al. (2023) provides a high-redshift CC point at `z=1.26`, but it
  is outside the frozen `abs(z-1.484)<=0.10` row-4 window.
- Jiao et al. (2023) and Jimenez et al. (2023) provide useful CC/photometric-CC
  context at lower redshift, but not row-4 support.
- The eBOSS/SDSS Ly-alpha BAO route is exactly at `z=2.33`, but it is a
  BAO/r_d cross-probe route rather than an independent clock measurement, so it
  is retained only as a control/context route.

The scan verdict is:

`desi_clock_support_candidate_scan_found_cross_probe_context_but_no_gate_closing_clock_support`

## Artifacts

- `data/source_manifest/paper10_desi_clock_support_source_candidate_scan_policy_v1.csv`
- `data/derived/paper10_desi_clock_support_source_candidate_scan_v1.csv`
- `data/derived/paper10_desi_clock_support_source_candidate_scan_v1_summary.csv`
- `scripts/build_paper10_desi_clock_support_source_candidate_scan_v1.py`
- `scripts/validate_paper10_desi_clock_support_source_candidate_scan_v1.py`

# Paper10 DESI Row-4 Non-Simon Clock Search v1

**Doc class:** source-side blocker audit
**Reader role:** Paper10 DESI time/readout reviewer
**Status:** negative strict-window source search; not replay; not validation
**Canonical parent:** `README.md`

This audit checks the narrow release condition for the DESI radial row at
`z_eff=1.484`: a source-native, non-Simon cosmic-clock or clock-like
time/readout source inside the frozen `|Delta z| <= 0.10` row-4 window.

The source-native Simon et al. bracket already freezes:

- `H(z=1.43)=177+/-18 km/s/Mpc`
- `H(z=1.53)=140+/-14 km/s/Mpc`

Those entries bracket row 4, but both reuse the Simon et al. (2005) reference
family. They therefore improve provenance without releasing the
independent-reference-family blocker.

The present strict-window search records the closest non-Simon chronometer
candidate found in the current source chain, Moresco (2015) at `z=1.363`, and
keeps it outside replay because `|1.363-1.484|=0.121 > 0.10`. This is a useful
near miss, not a gate-closing source.

Claim boundary:

- no endpoint replay,
- no validation claim,
- no physical-validation claim,
- no redshift-window widening,
- no use of BAO/RSD or Ly-alpha BAO as clock support,
- no post-hoc smoothing or interpolation to manufacture row-4 support.

Verdict:

`row4_non_simon_strict_window_search_negative_blocker_remains`

The next allowed action is either to find a non-Simon independent clock or
source-native time/readout support inside the frozen row-4 window, or to request
a new external-review decision that explicitly justifies a wider source window
before any replay is considered.

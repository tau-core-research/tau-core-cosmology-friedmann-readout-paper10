**Doc class:** source-side diagnostic audit
**Reader role:** Paper10 observer/path projection refinement
**Status:** source audit; not scoring and not validation
**Canonical parent:** README.md

# V2 Sky-Z Source Audit V1

This audit explains what the current `W_path_x_sky_z` replay actually uses.
It is not a new score and does not alter the authorized replay.

For each of the 12 predeclared partial-path rows, the audit records:

```text
sky_x = cos(dec) cos(ra)
sky_y = cos(dec) sin(ra)
sky_z = sin(dec)
W_path_x_sky_z_raw = W_path * sky_z
W_path_x_sky_z_normalized = W_path_x_sky_z_raw / max(abs(raw))
```

Thus `sky_z` is a minimal observer-orientation proxy: it tests whether the
source-observer sky direction adds information to the partial path proxy. It is
not a full physical null-geodesic-bundle kernel, not a lensing path weight, and
not a population validation result.

## Next Kernel Direction

The next focused source-side refinement should keep the same leakage boundary
and replace the single-coordinate proxy by a predeclared observer/path
orientation kernel. Candidate ingredients are:

```text
full sky vector: sky_x, sky_y, sky_z
coordinate-frame audit: equatorial versus Galactic coordinates
survey path support: footprint/mask/depth where source-native products exist
line-of-sight environment: frozen environment count/density fields
redshift path weighting: fixed source-side z dependence
```

Any such kernel must be frozen before replay and must be tested against
wrong-orientation, shuffled-orientation, and sign-flip controls.


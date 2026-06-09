# KiDS-1000 COSEBIs Endpoint Mode-Shape Stress v1

This post-score stress audit follows the mode-localization result. The
source-frozen endpoint candidate uses a deliberately simple, source-independent
mode carrier:

```text
M_mode(n) = n^(-1/2) / mean_{n=1..20}(n^(-1/2)).
```

Because the endpoint signal is low-mode localized, this audit asks whether the
result is purely an artifact of that chosen carrier. It keeps the same
source-frozen `W_path` mapping and the same endpoint scoring rule, but replaces
only the mode-shape carrier by a small predeclared stress family:

- `flat`;
- `n^-0.25`;
- `n^-0.5_candidate`;
- `n^-0.75`;
- `n^-1.0`;
- `high_sqrt_n`;
- `high_n`.

Current result:

- tested mode shapes: `7`;
- best mode shape: `n^-0.5_candidate`;
- candidate `n^-0.5` Delta chi-square: `-183.6152665217`;
- flat mode-shape Delta chi-square: `-136.5504934506`;
- high-`n` mode-shape Delta chi-square: `0.0`;
- verdict:
  `low_weighted_carriers_preferred_but_flat_still_improves_high_weighting_fails`.

Interpretation boundary:

The low-mode result is carrier-sensitive, but not reducible to a single
post-hoc carrier trick in this stress family. A flat mode carrier still
improves over the zero baseline, while high-mode-weighted carriers largely
remove the signal. The predeclared `n^-1/2` candidate is the best of this small
stress family, so the next source-side question is why a low-mode carrier is
natural for the path/readout shell. This is a carrier-sensitivity diagnostic,
not validation and not a final KiDS lensing theory vector.

Claim boundary:

```text
kids1000_cosebis_endpoint_mode_shape_stress_not_validation
```

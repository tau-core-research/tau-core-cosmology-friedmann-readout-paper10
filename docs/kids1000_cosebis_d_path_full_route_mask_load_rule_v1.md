# KiDS-1000 COSEBIs D_path Full-Route Mask-Load Rule v1

This artifact resolves the `D_path` source-side blocker only in a narrow,
caveated sense. It is not an endpoint score and not a physical depth-map
calibration.

The rule uses the same 196 source-frozen KiDS DR4.1 route mask products used by
the full-route `F_overlap` rule, but it extracts a different source observable:

```text
D_path(tile)
  = mean_nonzero_mask_value(tile)
    / max_tile(mean_nonzero_mask_value(tile))
```

This separates it from `F_overlap`, which uses the nonzero finite pixel
fraction. `F_overlap` measures coverage support; `D_path` is a caveated
mask-load proxy from the nonzero mask-value distribution. Because the mask
values are survey mask/quality encodings rather than a calibrated depth map,
the rule is promoted only as `source-supported mask-load proxy`, not as a final
survey-depth observable.

Leakage boundary:

- no KiDS COSEBIs data-vector values;
- no posterior chains;
- no lensing residuals;
- no fit statistics;
- no post-hoc tile/path selection;
- no endpoint scoring.

The next blocker after this rule is the web/environment factor `E_web`, followed
by source-side normalization, mapping-vector construction, theory-vector
construction, null controls, and only then endpoint scoring.

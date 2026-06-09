# KiDS-1000 COSEBIs F_overlap Resolution Decision v1

This gate records the current formal decision for the first KiDS COSEBIs
path-weight factor, `F_overlap`.

Current decision:

- an endpoint-route source support for `F_overlap` is now accepted in the narrow
  sense of a source-frozen, non-degenerate full-route pixel-fraction rule;
- the rule uses all 196 preferred-route mask products represented in the local
  full-route cache/inventory and the three committed subset masks;
- it attaches a source-only pixel-content fraction to the full
  `300 x 196 = 58,800` target-row by route-tile domain;
- the resulting `F_overlap` values are non-uniform, with 196 rounded unique tile
  values and a range of about `0.453` to `1.000`;
- the older header-footprint route remains preserved as a negative control: it
  was leakage-safe but uniform and therefore not promotable;
- the three-mask pixel-fraction pilot remains proof-of-method only;
- the official-footprint route is not needed for the current `F_overlap` gate;
- the partial-control route remains a caveated control, not endpoint evidence.

This artifact still computes no path mapping, no theory vector, no prediction,
no residual, and no score. It exists to prevent accidental promotion of source
support into endpoint validation.

The next scoring-facing action is no longer `F_overlap`. The first remaining
path-weight blocker is `D_path`, followed by `E_web`, `C_norm`, mapping-vector
construction, theory-vector construction, null controls, and only then endpoint
scoring.

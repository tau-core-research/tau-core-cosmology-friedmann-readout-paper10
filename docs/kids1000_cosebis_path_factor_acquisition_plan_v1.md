# KiDS-1000 COSEBIs Path-Factor Acquisition Plan v1

This gate declares the source-side acquisition requirements that must be met
before the KiDS-1000 COSEBIs path-weight rule can become computable.

The plan does not fetch new products and does not compute any weights. It only
records the required source classes, acceptance criteria, and leakage
boundaries for each factor in the future path-weight rule.

Current status:

- `N_pair` and `T_tile` already have source-side support for a future rule.
- `F_overlap` requires a source-frozen footprint/overlap product or rule that
  assigns route tiles to COSEBIs target rows without endpoint input.
- `D_path` requires the full preferred route mask/depth products or an accepted
  source-native mask/depth summary. The current three-mask shell is only a
  partial sanity layer.
- `E_web` requires a source-frozen web/environment catalogue covering the KiDS
  footprint.
- `C_norm` cannot be evaluated until the nonzero source-side factors exist.
- Null controls cannot run until a mapping vector exists.

The acquisition plan forbids KiDS data-vector values, posterior chains,
residuals, fit-improvement flags, or post-hoc path labels. It is not validation.

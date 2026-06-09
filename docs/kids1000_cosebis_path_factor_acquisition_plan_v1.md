# KiDS-1000 COSEBIs Path Factor Acquisition Plan v1

This plan translates the symbolic path-weight factors into source-side
requirements. It is not a fetch script and not an endpoint score.

Current status:

- `N_pair` and `T_tile` are locked from existing source inventories;
- `F_overlap` is source-supported by the full-route pixel-fraction rule;
- `D_path` is source-supported by the caveated full-route mask-load proxy;
- `E_web` is source-supported only as a uniform null-web control, with no
  positive web/environment claim;
- `C_norm` is source-side resolved by unit-mean normalization of the frozen nonzero source factors;
- null controls are declared but not executed because no mapping vector exists.

The plan fetches no external products, computes no path mapping, and reads no
KiDS data-vector values, posterior chains, residuals, or fit-improvement flags. The next blocker is the source-frozen mapping vector.

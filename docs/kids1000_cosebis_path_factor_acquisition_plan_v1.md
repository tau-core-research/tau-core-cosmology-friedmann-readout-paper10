# KiDS-1000 COSEBIs Path Factor Acquisition Plan v1

This plan translates the symbolic path-weight factors into source-side
requirements. It is not a fetch script and not an endpoint score.

Current status:

- `N_pair` and `T_tile` are locked from existing source inventories;
- `F_overlap` is source-supported by the full-route pixel-fraction rule;
- `D_path` is source-supported by the caveated full-route mask-load proxy;
- `E_web` remains unresolved and is the first missing source factor;
- `C_norm` is deferred until nonzero source factors are fixed;
- null controls are declared but not executed because no mapping vector exists.

The plan fetches no external products, computes no path mapping, and reads no
KiDS data-vector values, posterior chains, residuals, or fit-improvement flags.

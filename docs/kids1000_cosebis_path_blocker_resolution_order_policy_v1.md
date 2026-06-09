# KiDS-1000 COSEBIs Path Blocker-Resolution Order Policy v1

This gate freezes the order in which source-side blockers must be resolved
before any KiDS-1000 COSEBIs path-aware endpoint can be attempted.

The ordering is:

1. freeze a footprint or row-tile overlap rule (`F_overlap`);
2. promote the path/depth factor beyond the current three-mask shell (`D_path`);
3. freeze web/environment support or a predeclared null-web control (`E_web`);
4. define source-side normalization only after nonzero source factors exist
   (`C_norm`);
5. build the mapping vector;
6. execute null controls.

In the current source ledger, `F_overlap` is source-supported by the full-route
pixel-fraction rule, `D_path` is source-supported only as a caveated full-route
mask-load proxy, and `E_web` is source-supported only as a uniform null-web
control. This means the current route is path-only/projection-only with no
positive web/environment claim. `C_norm` is now source-side resolved by
unit-mean normalization of the frozen nonzero source factors. The first
remaining unresolved blocker is therefore the mapping vector. Later steps are
intentionally not allowed to become endpoint-bearing shortcuts around the
missing mapping vector.

This policy fetches no external products, computes no factor values, builds no
mapping vector, and performs no scoring. It only fixes the future source-side
order and leakage boundaries.

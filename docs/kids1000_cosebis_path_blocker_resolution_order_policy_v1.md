# KiDS-1000 COSEBIs Path Blocker-Resolution Order Policy v1

This gate freezes the order in which source-side blockers must be resolved
before any KiDS-1000 COSEBIs path-aware endpoint can be attempted.

The ordering is:

1. freeze a footprint or row-tile overlap rule (`F_overlap`);
2. promote the path/depth factor beyond the current three-mask shell (`D_path`);
3. freeze web/environment support or a predeclared null-web control (`E_web`);
4. define source-side normalization only after nonzero source factors exist
   (`C_norm`);
5. build the source-frozen mapping vector;
6. execute null controls and construct the source-frozen theory vector before
   scoring.

In the current source ledger, `F_overlap` is source-supported by the full-route
pixel-fraction rule, `D_path` is source-supported only as a caveated full-route
mask-load proxy, and `E_web` is source-supported only as a uniform null-web
control. This means the current route is path-only/projection-only with no
positive web/environment claim. `C_norm` is source-side resolved by unit-mean
normalization of the frozen nonzero source factors, and the source-frozen
mapping vector is available as a 300-row mapping basis. The path-side first
remaining unresolved blocker is therefore null-control execution. Endpoint
scoring still remains blocked by the missing theory vector/mode-shape and by
unexecuted null controls.

This policy fetches no external products, computes no endpoint factor from
KiDS data values, builds no theory vector, and performs no scoring. It fixes
the source-side order and leakage boundaries.

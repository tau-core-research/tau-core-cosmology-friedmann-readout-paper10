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
6. replay null controls against the source-frozen theory-vector shell before
   scoring.

In the current source ledger, `F_overlap` is source-supported by the full-route
pixel-fraction rule, `D_path` is source-supported only as a caveated full-route
mask-load proxy, and `E_web` is source-supported only as a uniform null-web
control. This means the current route is path-only/projection-only with no
positive web/environment claim. `C_norm` is source-side resolved by unit-mean
normalization of the frozen nonzero source factors, the source-frozen mapping
vector is available as a 300-row mapping basis, and the null-control theory
replay is available as deterministic control-vector digests. No path-side
blocker remains in this ledger. Endpoint scoring still remains blocked by the
separate partial-control degeneracy audit.

This policy fetches no external products, computes no endpoint factor from
KiDS data values, and performs no scoring. The separate source-frozen
theory-vector shell and null-control replay are not endpoint evidence until the
degeneracy blocker is resolved. This policy fixes the source-side order and
leakage boundaries.

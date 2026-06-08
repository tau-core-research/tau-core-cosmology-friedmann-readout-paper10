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

The first unresolved blocker is `F_overlap`. Later steps are intentionally not
allowed to become endpoint-bearing shortcuts around missing footprint support.

This policy fetches no external products, computes no factor values, builds no
mapping vector, and performs no scoring. It only fixes the future source-side
order and leakage boundaries.

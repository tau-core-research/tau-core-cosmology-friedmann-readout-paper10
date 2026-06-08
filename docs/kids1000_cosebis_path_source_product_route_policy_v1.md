# KiDS-1000 COSEBIs Path Source-Product Route Policy v1

This gate declares candidate source-product routes for resolving the blockers
identified by the path-factor acquisition plan. It does not fetch the products,
compute factor values, build path weights, build a mapping vector, or run
endpoint scoring.

The route manifest separates three classes:

- locked existing ingredients: redshift-pair support and preferred route-tile
  support already exist as source-side inventories;
- blocker-resolution candidates: footprint overlap, full path/depth support,
  web/environment support, and later source-side normalization;
- controls: documented incomplete path/depth subset, null-web absent control,
  and null-control execution after a mapping vector exists.

The accepted future order is:

1. freeze an official or source-native route for footprint overlap;
2. promote the path/depth factor beyond the current three-mask shell;
3. attach a source-frozen web/environment catalogue or predeclare a null-web
   control;
4. define normalization only after nonzero source factors exist;
5. build and audit the mapping vector;
6. only then execute null controls and endpoint scoring.

The manifest forbids KiDS data-vector values, posterior chains, residuals,
fit-improvement flags, post-hoc sky/tile/path labels, and post-hoc weight
selection. It is a source-route declaration, not validation.

# KiDS-1000 COSEBIs Path-Mapping Source Preflight v1

This ledger summarizes source-side readiness for a future path-aware COSEBIs
mapping. It is not a mapping vector and not endpoint validation.

Current status:

- target-row structure, redshift kernels, route-tile inventory, design skeleton,
  and the full 58,800-row target-tile domain skeleton are available;
- the three-mask observable shell is retained as a control layer;
- the full-route `D_path` mask-load proxy is available, but caveated as a mask
  proxy rather than a calibrated depth map;
- the web/environment catalogue is still missing;
- null controls are declared but not executed;
- no mapping vector, theory vector, prediction, residual, fit statistic, or
  endpoint score is computed.

Endpoint leakage remains forbidden.

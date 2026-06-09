# KiDS-1000 COSEBIs Path-Mapping Source Preflight v1

This ledger summarizes source-side readiness for a path-aware COSEBIs mapping.
It now records the available source-frozen mapping vector and source-frozen
null-control theory replay, but it is not endpoint validation.

Current status:

- target-row structure, redshift kernels, route-tile inventory, design skeleton,
  and the full 58,800-row target-tile domain skeleton are available;
- the three-mask observable shell is retained as a control layer;
- the full-route `D_path` mask-load proxy is available, but caveated as a mask
  proxy rather than a calibrated depth map;
- `E_web` is available only as a uniform null-web control; no positive
  web/environment catalogue is used;
- the path-weight construction rule is source-side available after `C_norm`,
  and a 300-row source-frozen mapping basis has been built;
- null controls have been replayed as deterministic theory-vector digests, but
  no null score has been computed;
- no endpoint prediction, residual, fit statistic, or endpoint score is
  computed.

Only the `source_frozen_mapping_vector` component row is allowed to carry
`path_mapping_computed=true` and `contains_mapping_vector=true`; the
`null_control_theory_replay` row records only control-vector digest readiness.
All earlier source-ledger component rows remain non-mapping evidence rows.

Endpoint leakage remains forbidden.

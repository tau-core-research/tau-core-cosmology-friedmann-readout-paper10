# Joint row-level control expansion audit v1

**Doc class:** control-scope audit.
**Status:** complete; not scoring; not validation.
**Claim boundary:** `joint_row_level_control_expansion_audit_not_scoring_not_validation`.

The strict expansion question is whether more row-level controls can
be added without changing the residual-blind alignment rule.

Current aligned controls: `6`.
Strict all-channel alignment ceiling: `6`.
Bottleneck channel: `desi_shape_time_readout`.

Under the present deterministic min-count alignment rule, there are
no additional strict controls available now. KiDS and observer/path
have many more row-level controls, but DESI shape/time has only six.

Two future options remain:

1. build more source-side DESI shape/time controls;
2. freeze a new relaxed alignment rule, such as cyclic reuse or a
   reviewed Cartesian product rule, before any expanded scoring.

No expanded scoring is authorized by this audit.

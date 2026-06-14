# Joint numeric channel z_i binding audit v1

**Doc class:** numeric-channel binding audit
**Status:** numeric source fields present; z_i standardization blocked
**Claim boundary:** `joint_numeric_channel_zi_binding_audit_not_scoring_not_validation`

This audit maps each active channel to a candidate numeric source field
that could later feed the shared statistic `T_joint = sum_i q_i z_i`.
It intentionally does not compute `z_i`, because the common signed
standardization rule for candidate and controls has not yet been frozen.

Current result:

- active channels: `3`
- numeric candidate fields present: `3`
- numeric z_i defined channels: `0`
- verdict: `NUMERIC_CHANNEL_FIELDS_PRESENT_ZI_STANDARDIZATION_BLOCKED`

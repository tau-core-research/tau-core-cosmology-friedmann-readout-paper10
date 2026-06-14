# Joint signed z_i standardization protocol v1

**Doc class:** signed standardization protocol
**Status:** rule frozen; numeric z_i blocked; not scoring; not validation
**Claim boundary:** `joint_signed_zi_standardization_protocol_not_scoring_not_validation`

This protocol freezes the sign convention and future standardization
rule for channel-level evidence before any numeric `T_joint` scoring.
For each channel, the native source value is first mapped to a
support-positive raw evidence value `e_i`. The future `z_i` may only
be standardized using the matched-control distribution, not the
candidate value.

Frozen rule:

```text
e_i = sign_i * native_value
center_i = median(e_i over matched controls only)
scale_i = MAD1.4826(e_i over matched controls only)
z_i = (e_i - center_i) / scale_i
```

If the matched-control scale is zero or unavailable, the channel remains
blocked rather than being rescued by a fitted scale.

Current result:

- active channels: `3`
- signed standardization rule frozen: `true`
- numeric z_i defined channels: `0`
- verdict: `SIGNED_ZI_STANDARDIZATION_PROTOCOL_FROZEN_NUMERIC_ZI_BLOCKED`

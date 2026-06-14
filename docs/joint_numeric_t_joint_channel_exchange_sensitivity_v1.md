# Joint numeric T_joint channel-exchange sensitivity v1

**Doc class:** channel-exchange diagnostic.
**Status:** not validation.
**Claim boundary:** `joint_numeric_t_joint_channel_exchange_sensitivity_not_validation`.

The observer-path low-z and DESI shape/time channels are source-distinct:
they use different score artifacts, different control artifacts, different
matched-control populations, and different caveats. However, after the
shared signed median/MAD standardization, their positive candidate `z_i`
values and frozen `q_i` weights are close enough that exchanging them
produces only a thin scalar `T_joint` margin.

This supports the narrow interpretation: the current scalar `T_joint`
sees source-distinct channels, but it does not strongly penalize this
particular lower-amplitude channel exchange. The next claim-safe check
is a source-side channel-distinguishability penalty or orthogonality
audit before strengthening validation language.

# Joint single-statistic binding prerequisites v1

**Doc class:** binding prerequisites ledger
**Status:** not scoring; not endpoint validation; not cosmological validation
**Claim boundary:** `joint_single_statistic_binding_prerequisites_not_scoring_not_validation`

This ledger freezes the channel-level inputs that a future single
joint statistic must bind: active-channel order, row-scope artifact,
score-source artifact, covariance object, and nuisance/amplitude rule.
It does not define the statistic and does not run a replay.

Summary:

- active channels: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- row-scope artifacts present: `2/3`
- score-source artifacts present: `2/3`
- single statistic defined: `false`
- covariance/independence closed: `false`
- scoring allowed: `false`
- verdict: `JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_FROZEN_PROTOCOL_BLOCKED`

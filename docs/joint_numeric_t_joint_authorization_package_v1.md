# Joint numeric T_joint authorization package v1

**Doc class:** external authorization handoff.
**Status:** prepared, not completed.
**Claim boundary:** `joint_numeric_t_joint_authorization_not_endpoint_scoring_not_validation`.

This package asks whether the existing channel-level numeric `z_i`
ledger may be combined once under the already frozen symbolic shell:

```text
T_joint = sum_i q_i z_i
```

The package does not authorize new endpoint scores, new fitting,
endpoint validation, cosmological validation, or physical validation.
It only asks whether the already built `z_i` ledger and frozen `q_i`
weights may be multiplied and summed into a numeric joint ledger.

The existing KiDS endpoint-score-not-validation caveat, DESI small-N
caveat, and caveated cross-probe covariance status remain attached.

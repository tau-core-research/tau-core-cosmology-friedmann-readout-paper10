# Joint multichannel block score v1

**Doc class:** block-aware joint-score preflight
**Status:** not a joint likelihood; not endpoint validation

This score combines the already frozen joint-channel candidate rows
using their weighted channel contributions. It adds exact sign-flip
controls, seeded channel-weight shuffles, and leave-one-channel checks.
It does not access raw endpoint residuals and does not estimate a
cross-probe covariance.

Summary:

- nonzero-weight channels: `5`
- block-normalized score: `0.413070369`
- protocol-normalized score: `0.200059111`
- exact sign-flip p(score >= observed): `0.375000000`
- leave-one positive: `4/5`
- verdict: `JOINT_BLOCK_SCORE_FRAGILE_OR_INCONCLUSIVE_PREVALIDATION`

Claim boundary:

```text
joint_multichannel_block_score_prevalidation_not_joint_likelihood
```

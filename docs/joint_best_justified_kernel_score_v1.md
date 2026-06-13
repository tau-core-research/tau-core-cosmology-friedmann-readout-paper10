# Joint best-justified kernel score v1

**Doc class:** source-side weighted joint-kernel preflight
**Status:** not a joint likelihood; not endpoint validation

This artifact implements the admissible joint-kernel rule from the paper:

```text
Q_i = product_a (g_i^a)^(1/7)
w_i = Q_i / sum_j Q_j
K_joint = sum_i w_i K_i
```

Only channels with `positive_support_allowed=true` and nonzero hard-gate
support receive positive joint weight. Control-dominated or source-incomplete
branches remain diagnostic/control rows.

Summary:

- positive-support channels: `3`
- channel order: `kids_lensing_cosebis_low_mode;observer_path_basis_low_z;desi_shape_time_readout`
- weighted sum: `0.412105634`
- normalized score: `0.713515777`
- exact sign-flip p(score >= observed): `0.125000000`
- combined-control p(score >= observed): `0.164682540`
- leave-one positive: `3/3`
- verdict: `BEST_JUSTIFIED_JOINT_KERNEL_POSITIVE_PREFLIGHT_NOT_VALIDATION`

Claim boundary:

```text
joint_best_justified_kernel_prevalidation_not_joint_likelihood
```

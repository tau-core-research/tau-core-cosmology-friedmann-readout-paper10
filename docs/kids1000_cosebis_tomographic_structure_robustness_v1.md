# KiDS-1000 COSEBIs Tomographic-Structure Robustness v1

This robustness run follows the endpoint scoring diagnostic. The endpoint
candidate was beaten only by tomographic-pair shuffle controls, so this audit
asks whether the low-tail result survives against stricter controls that
preserve more of the KiDS tomographic structure.

The control families are:

- `bin_label_permutation`: all 119 non-identity permutations of the five source
  bin labels, inducing a deterministic pair permutation;
- `auto_cross_preserving_shuffle`: 1000 seeded shuffles that keep auto-pairs in
  the auto-pair set and cross-pairs in the cross-pair set.

Current result:

- total structure-preserving controls: `1119`;
- candidate rank by chi-square: `4/1120`;
- plus-one tail fraction by chi-square: `0.003571428571429`;
- candidate rank by AIC: `4/1120`;
- plus-one tail fraction by AIC: `0.003571428571429`;
- better controls: 2 auto/cross-preserving shuffles and 1 bin-label
  permutation.

Interpretation boundary:

The result strengthens the low-tail character of the endpoint candidate because
the signal survives a more structured tomographic null ensemble. It is still not
validation: three structure-preserving controls beat the candidate, and the
remaining caveat is now specifically tomographic-structure robustness.

Claim boundary:

```text
kids1000_cosebis_tomographic_structure_robustness_not_validation
```

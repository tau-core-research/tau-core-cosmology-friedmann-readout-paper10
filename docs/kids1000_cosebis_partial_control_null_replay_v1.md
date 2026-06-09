# KiDS-1000 COSEBIs Partial-Control Null Replay v1

This diagnostic replay tests whether the caveated positive-mask partial-control
shape is special relative to deterministic null/control transforms.

It uses:

- the same retained KiDS COSEBIs `En` vector for scoring only;
- the same full 300 x 300 covariance Cholesky solve;
- the predeclared null-control seed inventory;
- nonnegative amplitude fitting per control draw.

Null families:

```text
sky_rotation: 4 deterministic cyclic row shifts
tomographic_pair_shuffle: 1000 deterministic pair-block permutations
wrong_channel_activation: 2 deterministic shape reversals
web_path_sign_flip: 2 deterministic sign controls
```

The replay reports a conservative plus-one tail fraction for null-control
draws with chi-square no worse than the observed `positive_mask_mean` branch.
It is not endpoint validation and not a population lensing claim.

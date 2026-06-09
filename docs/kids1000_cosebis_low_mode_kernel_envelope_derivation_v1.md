# KiDS-1000 COSEBIs Low-Mode Kernel Envelope Derivation v1

This artifact narrows the open blocker left by the low-mode carrier
source-grounding ledger. It does not claim a final KiDS lensing theory vector.
It derives only the envelope shape under an explicit source-side prior.

## Conditional Derivation

Let `n` be the dimensionless COSEBIs mode index on the retained domain
`n = 1..20`. Assume that a smooth path/readout residual is broad and coherent
across the mode hierarchy, so its source-side power is approximately neutral per
logarithmic mode band:

```text
dP / d ln n approximately constant.
```

For a unit-spaced discrete mode index,

```text
d ln n approximately dn / n,
```

so the power assigned to a single linear mode bin scales as

```text
P_n proportional to 1/n.
```

The coherent amplitude envelope is the square root of this power:

```text
M_mode(n) proportional to sqrt(P_n) proportional to n^(-1/2).
```

The finite retained KiDS mode domain fixes only a dimensionless protocol
normalization:

```text
M_mode(n) = n^(-1/2) / mean_{n=1..20}(n^(-1/2)).
```

## Claim Boundary

This is a conditional envelope derivation. The key assumption is the
log-band-neutral path/readout power prior. The artifact does not prove that this
prior is universally valid, and it does not replace a future covariant or
survey-native lensing path-kernel derivation.

Current verdict:

```text
conditional_log_band_power_envelope_derives_n_minus_half_shape_but_covariant_kernel_blocker_remains
```

Claim boundary:

```text
kids1000_cosebis_low_mode_kernel_envelope_conditional_derivation_not_validation
```

# Joint best-justified `Q_i` review package v1

Status: `SOURCE_SIDE_REVIEW_PACKAGE_NOT_SCORING`

This package prepares the next scientific gate for the Paper 10
best-justified joint kernel. It does not compute new endpoint scores and does
not change the current channel weights.

## Purpose

The current best-justified joint kernel uses protocol support scores

```text
Q_i = product_a (g_i^a)^(1/7)
```

for channels that pass the positive-support ledger. This is useful as a
preflight discipline, but it is not yet a physical likelihood weight. A
reviewer could reasonably ask why each gate value and exponent is justified.
This package freezes that question explicitly.

## Required review scope

The review must check:

1. whether each active channel's gate vector is source-side justified;
2. whether KiDS/COSEBIs, observer/path low-z, and DESI shape/readout deserve
   positive support under their current caveats;
3. whether ACT Kpath, void/web, time basis, distance shell, and sky-z remain
   correctly excluded from positive support;
4. whether the equal exponent rule `alpha_a=1/7` should remain the default or
   be replaced by a source-reviewed exponent vector;
5. whether any promotion from protocol support to validation-facing support is
   allowed before a covariance-aware joint likelihood exists.

## Forbidden inputs

The review may not use:

```text
endpoint residuals
fit improvements
posterior chains
post-score control ranks
```

If any of those fields are used, the review cannot promote the `Q_i` rule.

## Claim boundary

Allowed output:

```text
source-side Q_i review accepted/rejected/caveated
```

Forbidden output:

```text
joint likelihood validation
cosmological validation
dark-energy explanation
new gravity validation
```

The next endpoint after this package, if authorized, must be a separate
covariance-aware joint likelihood prototype with shuffled-channel,
wrong-channel, block-drop, sign-flip, and null/readout controls.

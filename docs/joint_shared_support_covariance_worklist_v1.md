# Joint Shared-Support and Covariance Worklist v1

**Doc class:** joint-kernel blocker worklist

**Reader role:** Paper 10 joint-preflight maintainer

**Status:** `JOINT_PREFLIGHT_BLOCKER_WORKLIST`

**Canonical parent:** `docs/joint_best_justified_kernel_score_v1.md`

Canonical data artifact:

```text
data/derived/joint_shared_support_covariance_worklist_v1.csv
```

## Purpose

This worklist records the finite tasks needed before the best-justified Paper
10 joint kernel can be strengthened beyond a positive preflight statistic.
It does not create a new score and does not promote the current result to a
validation-grade likelihood.

## Current Joint Object

The current joint object is:

```text
K_joint_bj = sum_i w_i K_i
```

where the positive-support components are source-frozen channel summaries such
as KiDS/COSEBIs low-mode support, observer/path low-z support, and DESI
shape/readout support.

The current status remains:

```text
BEST_JUSTIFIED_JOINT_KERNEL_POSITIVE_PREFLIGHT_NOT_VALIDATION
```

## Required Before Stronger Scoring

Three blockers must be handled before stronger joint claims:

1. **Shared-support matrix.** The same source feature cannot independently
   support multiple joint channels unless the overlap is explicitly modeled or
   deduplicated.
2. **Cross-probe covariance inventory.** A joint statistic is not a
   validation-grade likelihood without an adequate covariance treatment or a
   clearly stated block-diagonal limitation.
3. **Aligned-control inventory.** The candidate must be compared to controls
   that are symmetric under the frozen statistic and not selected after
   inspecting endpoint performance.

## Allowed Next Action

Allowed:

```text
build shared-support matrix
build covariance inventory
build aligned-control inventory
rerun only the same frozen statistic after these blocker notes are complete
```

Blocked:

```text
do not call the current joint score a p-value or likelihood
do not add/drop channels by score
do not hide relaxed-control negative or cautionary outcomes
```

## Claim Boundary

Even after this worklist is complete, the next positive result would be:

```text
covariance-aware prevalidation support
```

It would still not be dark-energy validation, Lambda-CDM replacement, or a
completed Tau Core cosmology derivation.

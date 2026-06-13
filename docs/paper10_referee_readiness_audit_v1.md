# Paper 10 referee-readiness audit v1

Status: `SUBMIT_AFTER_MAJOR_STRUCTURE_REDUCTION_OR_AS_LONG_PROTOCOL_PREFLIGHT`

This audit reviews the current Paper 10 manuscript as a cautious physics
referee would read it. It does not add new numerical evidence.

## Main claim check

Allowed claim:

```text
Paper 10 defines a source-frozen cosmological readout audit. Several individual
channels are operational; some are suggestive, some weak, and some negative.
The best-justified joint kernel is positive and robust under source-side
weighting stresses, but remains prevalidation.
```

Disallowed claim:

```text
Tau Core explains dark energy, replaces LCDM, validates a new gravity law, or
has already passed a joint cosmological endpoint.
```

## Strongest current elements

- The manuscript now distinguishes source-side readiness, single-channel replay,
  joint preflight, and future validation endpoint.
- The best-justified joint kernel has a source-side support rule and explicit
  active/zero-support channel ledger.
- ACT K-path is preserved as a controlled negative rather than removed.
- The abstract, status ledger, and conclusion now state that the result is
  prevalidation, not a joint likelihood.
- The new best-justified joint-kernel figure is generated from frozen CSV
  artifacts rather than hand-drawn.

## Reviewer-risk points

1. The manuscript remains very long and partly log-like. A journal version may
   need a shorter main text plus supplementary ledgers.
2. The Tau Core theoretical scaffold is unpublished; the operational claim must
   remain separable from accepting the full Tau Core ontology.
3. The best-justified score is a protocol support score, not a physical
   likelihood weight. The paper now states this, but a reviewer may still ask
   for source-native `Q_i` review.
4. Some LaTeX tables produce overfull/underfull warnings. The PDF builds, but
   a polished submission should move some dense tables to supplementary files.
5. The combined weight-shuffle null is weak for the conservative min-gate case
   because active weights become equal. This caveat is now explicitly reported.

## Fixes applied in this audit pass

- Abstract updated to mention the best-justified joint kernel and the five
  source-side weighting stresses while preserving the non-validation boundary.
- Added `What would count as validation?` section.
- Added a current Paper 10 status ledger.
- Updated the conclusion with the best-justified joint-kernel numbers:
  normalized score `0.713515777`, sign-flip `p=0.125000000`, combined-control
  `p=0.164682540`, robustness minimum `0.703534932`.
- Reworded narrow positive signals as protocol-level support rather than
  physical evidence.
- Reworded the ACT negative result as audit-discipline improvement rather than
  theory confirmation.

## Required next step before stronger claims

The next scientific gate is:

```text
source-native Q_i review + covariance-aware joint likelihood prototype
```

Until that gate exists, the correct paper status remains:

```text
multi-channel viability preflight, not cosmological validation
```

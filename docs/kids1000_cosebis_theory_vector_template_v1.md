# KiDS-1000 COSEBIs Theory-Vector Template v1

This artifact freezes the row interface for a future 300-row KiDS-1000 COSEBIs
theory vector.

It is not a theory vector and not a prediction. The template contains only the
retained tomographic-pair and COSEBIs-mode index:

- 15 upper-triangular tomographic source-bin pairs;
- 20 COSEBIs modes per pair;
- 300 contiguous rows.

The theory-value and channel-contribution columns are deliberately empty. A
future theory vector may fill them only after the source-frozen web/path mapping
and scoring preconditions are satisfied.

The template forbids KiDS data-vector values, posterior chains, residuals,
fit-improvement flags, post-hoc theory-vector choice, post-hoc mode cuts,
post-hoc tomographic selection, and post-hoc channel activation.

# KiDS-1000 COSEBIs `F_overlap` Execution Review Schema v1

This gate freezes the required column schema for a future fetched-batch
execution review artifact.

It does not fetch products, does not read ignored `data/local/` logs, and does
not promote any batch. Its purpose is to make the future review artifact
auditable before data acquisition is used in any source-freeze decision.

The schema requires product identity, URL, expected cache path, HTTP status,
byte count, SHA-256, review status, reviewer role, forbidden-input flags, and
claim-boundary flags. Any future promoted review must keep endpoint quantities
out of the artifact: no KiDS data-vector values, posterior chains, residuals,
fit-improvement flags, post-hoc tile selection, overlap rule, mapping vector,
theory vector, predictions, fit statistics, or endpoint score.

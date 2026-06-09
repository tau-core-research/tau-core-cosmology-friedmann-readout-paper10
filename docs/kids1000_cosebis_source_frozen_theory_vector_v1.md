# KiDS-1000 COSEBIs Source-Frozen Theory Vector v1

This artifact builds the first source-frozen unit-amplitude theory-vector shell
for the KiDS-1000 COSEBIs path-aware branch.

It is not endpoint scoring, not a likelihood, not a residual calculation, and
not empirical validation.

The frozen shell is:

```text
t_i = W_path_i * M_mode(n_i)
W_path_i = source_frozen_mapping_value_i
M_mode(n) = n^(-1/2) / mean_{n=1..20}(n^(-1/2))
W_web_i = 0
amplitude = 1, no fit and no residual calibration
```

The mode-shape is deliberately simple and source-independent. It exists only to
turn the previously built pair/redshift/path mapping basis into a 300-row
source-frozen carrier vector. The current release makes no claim that this is
the final KiDS lensing theory vector.

Leakage boundary:

```text
no KiDS data-vector values
no posterior chains
no residuals
no fit statistics
no fit-improvement flags
no post-hoc mode-shape choice
no post-hoc amplitude fit
endpoint scoring disabled
```

Completed source-side follow-up before endpoint scoring:

```text
predeclared null-control replay
non-degenerate endpoint-family geometry audit
endpoint-readiness validation after controls
```

These follow-up gates are now built as non-scoring artifacts. The endpoint
readiness ledger has no remaining blocker, but endpoint scoring is still
disabled until an explicit scoring run is opened under the frozen protocol.

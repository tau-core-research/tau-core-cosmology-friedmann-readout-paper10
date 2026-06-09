# KiDS-1000 COSEBIs Source-Frozen Mapping Vector v1

This artifact builds the first source-frozen 300-row mapping basis for the
KiDS-1000 COSEBIs path-aware branch.

It is not a theory vector, not a prediction, not a residual calculation, and
not endpoint validation.

The rule is:

```text
normalized_fde = C_norm * F_overlap * D_path * E_web
n_pair_unit_mean_factor = mean_z(pair) / mean_domain(mean_z(pair))
mapping_value(row) = mean_tiles(normalized_fde * n_pair_unit_mean_factor)
```

where `C_norm` is the already frozen source-side unit-mean normalization over
the full 58,800-row target-tile domain.

Frozen outputs:

```text
target rows:       300
domain rows:       58,800
unique values:     15
mean value:        1.0
W_path basis:      source-frozen mapping value
W_web basis:       0, because E_web is still a null control
endpoint scoring:  disabled
```

The vector has tomographic-pair/redshift/path variation, but no COSEBIs
mode-shape and no theory value. It therefore resolves the source-side
`mapping_vector` blocker only in the limited sense of providing a
source-frozen mapping basis.

Remaining blockers before endpoint scoring:

```text
theory vector / mode-shape construction
null-control execution under frozen seeds
endpoint-readiness validation after both are complete
```

Forbidden inputs remain KiDS data-vector values, posterior chains, residuals,
fit statistics, fit-improvement flags, post-hoc weights, post-hoc tile
selection, post-hoc sky-direction labels, post-hoc web/path labels, and
post-hoc mapping-rule selection.

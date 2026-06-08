# KiDS-1000 COSEBIs `F_overlap` Rule Shell v1

This gate declares the acceptance shell for the first unresolved KiDS-1000
COSEBIs path blocker, `F_overlap`.

`F_overlap` is the source-side rule that must decide which route tiles support
which COSEBIs target rows. It is structural: without it, no path/depth factor,
web/environment factor, normalization, mapping vector, null control, or
endpoint score is allowed to become active.

The shell accepts two future source routes:

- official KiDS DR4/DR4.1 footprint polygon or tile geometry;
- source-native pixel-mask overlap derived from full preferred-route mask
  products.

The declared future output schema is a row-tile support table with one row per
COSEBIs target-row by route-tile domain entry. The current domain has
`300 x 196 = 58,800` rows. This shell does not compute the support flags or
fractions.

Forbidden inputs remain: KiDS data-vector values, posterior chains, residuals,
fit-improvement flags, post-hoc path labels, post-hoc sky/tile selection, and
post-hoc weight selection. This shell is not validation and not scoring.

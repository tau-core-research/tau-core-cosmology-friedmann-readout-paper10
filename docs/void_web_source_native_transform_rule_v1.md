# Void/Web Source-Native Transform Rule V1

This transform is the first replacement for the redshift/scale-factor proxy
bases used in the previous `W_void + W_web` full-covariance pilot.

It is recorded in:

```text
data/source_manifest/void_web_source_native_transform_rule_v1.csv
```

and builds:

```text
data/derived/pantheon_void_web_source_native_design_matrix_v1.csv
data/derived/pantheon_void_web_source_native_design_matrix_v1_summary.csv
```

## Claim Boundary

This is a source-native design-matrix transform, not endpoint scoring.

The transform may use:

- source catalogue redshifts,
- source catalogue distances,
- void radii/effective radii,
- web density values,
- source masks and catalogue quality filters,
- Pantheon source-side row coordinates/redshifts already admitted by the frozen
  Pantheon scope.

The transform may not use:

- distance residuals,
- growth residuals,
- lensing residuals,
- fit-improvement flags,
- late-time fit parameters,
- post-hoc void thresholds,
- post-hoc environment labels.

## Void Rule

The VAST/SDSS DR7 Planck2018 maximal-void table is low-redshift and
comoving-distance based. For this first transform, Pantheon `zHD` is mapped to
a low-redshift comoving-distance proxy:

```text
r_pantheon = 2997.92458 * zHD  Mpc/h
```

This is a source-side coordinate matching rule, not a cosmological fit.

The void load is the cumulative, normalized effective-volume proxy:

```text
W_void = cumulative_sum(Reff^3) / total_sum(Reff^3)
```

inside the source support. It is set to zero outside the void-catalogue support.

## Web Rule

The SDSS DR17 MCPM SlimeMold catalogue provides source-native galaxy redshifts
and `matterDens`. The first transform applies a catalogue quality filter:

```text
0 < z < 3
matterDens > -90
```

Then it bins the catalogue in redshift and uses the median `matterDens` per bin.
The resulting bin medians are robust-normalized with source-only 10th and 90th
percentiles and clipped to `[0,1]`.

## Remaining Gate

The transform creates source-native `W_void_source_native_basis` and
`W_web_source_native_basis` columns. A later pilot may score these columns under
full covariance, but that scoring must be declared separately and retain
wrong-family and shuffled controls.

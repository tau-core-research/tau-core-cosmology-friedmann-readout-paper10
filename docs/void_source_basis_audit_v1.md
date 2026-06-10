# Void Source-Basis Audit v1

## Status

This is a source-basis audit following the void-channel inactivity diagnostic.
It does not reopen endpoint scoring and does not claim physical validation.

## Finding

The present source-native void basis is a low-redshift, volume-limited void
catalogue mapped onto the full Pantheon distance block.

Key values:

- Pantheon scope: `zHD = 0.02303` to `2.26137`
- Void catalogue proxy support: `z = 0.0103747416544` to `0.108950468807`
- Void-active Pantheon rows: `426 / 1371`
- Void-active fraction: `0.310722100656`
- Void-zero fraction: `0.689277899344`
- Best non-zero void profile still worsens over `omega_void=0` by
  `delta_chi2 = 0.16283019`

The redshift-bin audit shows zero void support for all Pantheon rows above
`z=0.2`.

## Verdict

`low_z_volume_limited_void_catalog_mapped_to_full_pantheon_distance_block`

This explains why the combined endpoint suppresses the void channel. The current
void basis is not source-complete for the declared full-Pantheon distance scope.

## Consequence

The next claim-safe action is not endpoint scoring. The void mapping must be
rebuilt for the declared observable scope before the combined void/web endpoint
can be reopened. Acceptable routes include:

- restrict a future endpoint to a predeclared low-redshift Pantheon subset, or
- acquire/freeze a void/environment source basis with support matched to the
  intended distance block, or
- move the void channel out of the full-distance likelihood until a matched
  support rule exists.

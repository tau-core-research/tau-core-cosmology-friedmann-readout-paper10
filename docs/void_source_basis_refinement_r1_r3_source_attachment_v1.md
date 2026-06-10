# Void Source-Basis Refinement R1-R3 Source Attachment v1

**Doc class:** source-side attachment ledger  
**Status:** R1-R3 attached; R4-R6 still open; not scoring

This artifact attaches the first three source-side routes required by the void
source-basis refinement acquisition manifest. It does not compute endpoint
scores, authorize a replay, tune amplitudes, or claim validation.

## Attached routes

1. `R1_void_catalogue_object_properties`

   The source-native VAST/SDSS DR7 VoidFinder Planck2018 maximal void table is
   attached as an object-level void catalogue. It provides void center
   coordinates, effective radius, catalogue radius, sky position, and object id.

2. `R2_supernova_host_to_void_geometry`

   A residual-blind low-z Pantheon geometry join is built. For each frozen low-z
   Pantheon row, the script uses host coordinates when present and otherwise the
   supernova sky coordinates as a documented fallback. It then computes nearest
   void id, center distance, wall distance, angular separation, and whether the
   row lies inside the nearest effective void radius.

3. `R3_line_of_sight_environment`

   A source-side line-of-sight environment proxy is built from the SDSS DR17 MCPM
   slime-mold galaxy catalogue. The rule uses a fixed redshift window and fixed
   angular cone before scoring: `|dz| <= 0.01` and `theta <= 2 deg`.

## Current counts

```text
low_z_rows = 424
void_catalogue_rows = 1163
inside_effective_void_radius_rows = 43
los_environment_nonempty_rows = 230
```

## What remains blocked

The attachment does not make the refined void basis endpoint-ready. The next
required gates remain:

- `R4_redshift_degeneracy_independence_preflight`;
- `R5_control_resistance_preflight`;
- `R6_independent_leakage_review`.

No replay request is allowed until those gates are completed.

## Claim boundary

```text
r1_r3_source_attachment_not_scoring_not_validation
```

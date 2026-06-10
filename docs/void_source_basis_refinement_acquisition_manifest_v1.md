# Void Source-Basis Refinement Acquisition Manifest v1

**Doc class:** source-side acquisition manifest  
**Status:** frozen, sources not attached, not scoring  

This manifest is the only next artifact allowed by the void source-basis
refinement gate. It does not acquire data, compute scores, authorize a replay,
or claim validation. It freezes what evidence must be attached before any new
void replay can be requested.

## Why this manifest exists

The current `W_VOID_MATURITY` basis failed the low-z replay diagnostic because
it was redshift-degenerate and not control-unique:

```text
current_W_void_not_endpoint_ready_redshift_degenerate_not_control_unique
```

The next step is therefore source-side refinement, not amplitude or grid tuning.

## Required acquisition routes

1. `R1_void_catalogue_object_properties`

   Attach a source-native void catalogue with object-level radius, depth,
   center, redshift, boundary, membership, and selection-function fields.

2. `R2_supernova_host_to_void_geometry`

   Attach a residual-blind host-to-void geometry join: membership or nearest
   void, wall distance, host position inside/outside the void, and line-of-sight
   relative position.

3. `R3_line_of_sight_environment`

   Attach an independent line-of-sight density/environment proxy so the refined
   basis can distinguish void maturity from path/environment effects.

4. `R4_redshift_degeneracy_independence_preflight`

   Before scoring, show that the refined basis is not mostly a redshift or
   source-row-index proxy.

5. `R5_control_resistance_preflight`

   Predeclare shuffled, wrong-sign, wrong-threshold, and zero-void controls
   before replay authorization.

6. `R6_independent_leakage_review`

   Complete independent review confirming that distance residuals, fit
   statistics, endpoint scores, and post-hoc threshold choices were not used.

## Forbidden route

The manifest forbids:

- basis construction from distance residuals;
- catalogue choice from fit improvement;
- post-hoc row selection;
- post-hoc void thresholds;
- post-hoc amplitude tuning;
- covariance rescue;
- endpoint score or validation claims.

## Current verdict

```text
void_source_basis_refinement_acquisition_manifest_frozen_sources_not_attached
```

## Claim boundary

```text
void_source_basis_refinement_acquisition_manifest_not_scoring_not_validation
```

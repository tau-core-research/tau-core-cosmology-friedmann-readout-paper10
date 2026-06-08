# Tau Core Cosmology Friedmann-Readout Paper 10

This repository is the initial private reproducibility scaffold for Paper 10:

**A source-frozen Friedmann-readout audit protocol for late-time cosmology**

The paper is a protocol and pilot-analysis design. It connects the
Koushiappas uncertainty-Friedmann external comparison to a Tau Core
Friedmann-readout residual audit, then defines the data blocks needed to test
whether late-time acceleration is better read as a structured projection/readout
residual than as a homogeneous fluid.

## Main Claim

The repository defines a reproducible audit protocol:

```text
source-frozen void maturity and cosmic-web anisotropy proxies
    -> late-time activation shells
    -> distance, growth, lensing, and CMB safety tests
    -> shuffled and wrong-proxy null controls.
```

## Does Not Claim

- It does not claim that Tau Core explains dark energy.
- It does not claim a detection of a Friedmann-readout residual.
- It does not replace Lambda-CDM.
- It does not validate the Koushiappas uncertainty-Friedmann model.
- It does not use CMB maps as direct evidence for a Tau Core effect.
- It does not contain a completed perturbation-level or covariant Tau Core
  cosmology derivation.

## Included Data

This first scaffold contains only compact protocol artifacts in `data/derived/`.
No raw survey products are included.

The source-freeze manifest is:

```text
data/source_manifest/paper10_source_freeze_manifest.csv
```

It records candidate public source families, their current freeze status,
planned local artifact paths, and endpoint fields that are forbidden during
source selection.

The first explicit multi-channel readout manifest is:

```text
data/source_manifest/cosmology_channel_manifest_v1.csv
data/source_manifest/cosmology_activation_rule_manifest_v1.csv
data/source_manifest/cosmology_activation_parameter_freeze_plan_v1.csv
data/source_manifest/cosmology_source_grounding_gate_v1.csv
docs/cosmology_channel_manifest_v1.md
docs/cosmology_activation_rule_manifest_v1.md
docs/cosmology_activation_parameter_freeze_plan_v1.md
docs/cosmology_source_grounding_gate_v1.md
scripts/validate_cosmology_channel_manifest_v1.py
scripts/validate_cosmology_activation_rule_manifest_v1.py
scripts/validate_cosmology_activation_parameter_freeze_plan_v1.py
scripts/validate_cosmology_source_grounding_gate_v1.py
```

It declares the four source-frozen channel families `W_void`, `W_web`,
`W_path`, and `W_time`, plus their allowed source families, forbidden endpoint
fields, activation-rule IDs, null controls, and projection-induction roles.
The activation-rule manifest adds non-numeric formula shells and source-only
parameter-freeze policies. The parameter-freeze plan declares how scales such
as `S_void_star`, `Q_env_star`, `P_lens_star`, and `Delta_clock_star` may later
be frozen from source-native data. The source-grounding manifest then freezes
the four missing projection-induction checks for each channel: activation,
quotient survival, closure stability, and 4D readout survival. Every row
remains `endpoint_scoring_allowed=false`.

## Reproduce

```bash
python scripts/reproduce.py
```

The reproduction script compiles the manuscript with `tectonic`, validates the
source-freeze and channel manifests, builds the arXiv source package, and runs
smoke tests.

## arXiv Source Package

`arxiv_submission_source.zip` is generated from `paper10_submission_source/`
and excludes `main.pdf` plus TeX build byproducts.

## Online Data Dependencies

The one-command reproduction path does not perform live online data acquisition.
Future source-acquisition scripts should document exact URLs, versions, hashes
where possible, and redistribution boundaries.

For provenance, the repository includes a compact cache of the official source
landing pages listed in the manifest:

```bash
python scripts/acquire_source_pages.py
python scripts/validate_cached_source_pages.py
```

The acquisition script is intentionally separate from `scripts/reproduce.py`;
reproduction validates the committed cache hashes instead of depending on live
network access.

Current source manifest status:

- all required source families now have a candidate public source route,
- official source landing pages are cached with SHA-256 hashes,
- no source row is `FETCHED_FROZEN`,
- no endpoint scoring is allowed from this scaffold.

The first source-selection audit is recorded in:

```text
docs/source_selection_audit_001.md
```

The product-freeze preflight plan is recorded in:

```text
data/source_manifest/paper10_product_freeze_plan.csv
docs/product_freeze_plan.md
```

It declares the product roles, transformation-rule IDs, covariance/mask policy
requirements, and `endpoint_allowed=false` status for every planned product.

The next source-native void/web upgrade gate is recorded in:

```text
data/source_manifest/void_web_source_native_freeze_plan_v1.csv
docs/void_web_source_native_freeze_plan_v1.md
scripts/validate_void_web_source_native_freeze_plan_v1.py
```

It declares one preferred VAST/SDSS DR7 void-catalogue route and one SDSS DR17
MCPM cosmic-web route for replacing the proxy `W_void` and `W_web` bases. Both
rows are `SOURCE_NATIVE_CANDIDATE_SELECTED_NOT_FETCHED`, and both keep
`endpoint_scoring_allowed=false`.

The first fetched source-native void/web products are recorded in:

```text
data/source_manifest/void_web_source_native_frozen_products_v1.csv
data/derived/void_web_source_native_inventory_v1.csv
docs/void_web_source_native_products_v1.md
scripts/acquire_void_web_source_native_products_v1.py
scripts/validate_void_web_source_native_products_v1.py
scripts/build_void_web_source_native_inventory_v1.py
scripts/validate_void_web_source_native_inventory_v1.py
```

This freezes a VAST/SDSS DR7 Planck2018 maximal void table, the associated NSA
mask, the SDSS DR17 MCPM SlimeMold galaxy catalogue, and the provider sha1sum
file. The inventory records `void_rows=1163` and
`fits_bintable_rows=638820`. These products remain endpoint-disabled because
the catalogue-to-scoring transform is not yet frozen.

The first source-native transform and distance-only pilot are recorded in:

```text
data/source_manifest/void_web_source_native_transform_rule_v1.csv
data/derived/pantheon_void_web_source_native_design_matrix_v1.csv
data/source_manifest/pantheon_void_web_source_native_full_cov_pilot_v1.csv
data/derived/pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv
docs/void_web_source_native_transform_rule_v1.md
docs/pantheon_void_web_source_native_design_matrix_v1.md
docs/pantheon_void_web_source_native_full_cov_pilot_v1.md
```

The design matrix is not scored and contains no residuals. The separate
full-covariance pilot remains
`VOID_WEB_SOURCE_NATIVE_FULL_COV_PILOT_NOT_VALIDATION`. It improves
Pantheon-only full-covariance chi-square by `0.508` relative to the
flat-Lambda-CDM branch, but loses under AIC by `3.492`, and the deterministic
shuffled control can still do better in chi-square. This is therefore a useful
source-native pipeline step, not a detection or endpoint validation.

The first growth-side multi-probe step is recorded in:

```text
data/source_manifest/sdss_final_bao_rsd_growth_summary_v1.csv
data/source_manifest/growth_web_source_native_transform_rule_v1.csv
data/derived/growth_web_source_native_design_matrix_v1.csv
data/source_manifest/growth_web_source_native_pilot_v1.csv
data/derived/growth_web_source_native_pilot_v1_summary.csv
docs/sdss_final_bao_rsd_growth_summary_v1.md
docs/growth_web_source_native_design_matrix_v1.md
docs/growth_web_source_native_pilot_v1.md
```

This freezes six SDSS final BAO/RSD `f sigma8(z)` summary points and attaches
the source-native `W_web` basis to them. The pilot is diagonal-summary only. It
improves chi-square by `0.306`, but loses under AIC by `1.694`, and the
wrong-sign control is equally good on the symmetric pilot grid. This is a first
growth-side stress test, not a growth endpoint validation.

The first official-covariance BAO/RSD growth block is recorded in:

```text
data/source_manifest/sdss_multitracer_bao_rsd_products_v1.csv
data/source_manifest/sdss_multitracer_bao_rsd_transform_rule_v1.csv
data/derived/sdss_multitracer_bao_rsd_design_matrix_v1.csv
data/source_manifest/sdss_multitracer_bao_rsd_full_cov_pilot_v1.csv
data/derived/sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv
docs/sdss_multitracer_bao_rsd_products_v1.md
docs/sdss_multitracer_bao_rsd_transform_rule_v1.md
docs/sdss_multitracer_bao_rsd_design_matrix_v1.md
docs/sdss_multitracer_bao_rsd_full_cov_pilot_v1.md
```

This freezes the official SDSS DR16 LRG+ELG multi-tracer BAO/RSD compressed
products and uses the Fourier-space six-component vector with its official
6x6 covariance. In this pilot the web channel modifies only the `f sigma8`
entries while the BAO distance entries remain in the shared covariance block.
The result is effectively neutral: chi-square improves by only `0.010`, AIC
loses by `1.990`, and the wrong-sign control is equally good. This is a useful
multi-probe covariance gate and a seminegative control, not evidence for a
preferred web-growth direction.

The first CMB-safety support check is recorded in:

```text
data/source_manifest/cmb_safety_lowz_support_v1.csv
data/derived/cmb_safety_lowz_support_v1.csv
data/derived/cmb_safety_lowz_support_v1_summary.csv
docs/cmb_safety_lowz_support_v1.md
scripts/build_cmb_safety_lowz_support_v1.py
scripts/validate_cmb_safety_lowz_support_v1.py
```

This is not a CMB likelihood and contains no CMB map data. It checks only that
the currently active late-time source-native void/web bases vanish above a
conservative safety floor (`z=10`) and at a recombination proxy (`z=1089.92`).
The check passes, so the current late-time pilots do not directly modify the
early-universe safety regime.

The first lensing route-freeze check is recorded in:

```text
data/source_manifest/kids1000_lensing_route_v1.csv
data/derived/kids1000_lensing_route_v1_head.csv
data/derived/kids1000_lensing_route_v1_summary.csv
docs/kids1000_lensing_route_v1.md
scripts/check_kids1000_lensing_route_v1.py
scripts/validate_kids1000_lensing_route_v1.py
```

This checks the public KiDS-1000 cosmic-shear tarball route by HEAD metadata
only. It does not fetch or redistribute the lensing tarball and contains no
data vector, covariance matrix, posterior chain, lensing residual, or fit
statistic. Lensing scoring remains forbidden until tomographic-bin policy,
statistic choice, covariance block, mask policy, and readout policy are frozen.

The first fetched KiDS lensing source product and COSEBIs route inventory are
recorded in:

```text
data/source_manifest/kids1000_lensing_products_v1.csv
data/source_manifest/kids1000_cosebis_lensing_route_v1.csv
data/raw/weak_lensing/kids1000/KiDS1000_cosmic_shear_data_release.tgz
data/derived/kids1000_lensing_inventory_v1.csv
data/derived/kids1000_lensing_inventory_v1_summary.csv
docs/kids1000_lensing_products_v1.md
docs/kids1000_cosebis_lensing_route_v1.md
scripts/acquire_kids1000_lensing_products_v1.py
scripts/validate_kids1000_lensing_products_v1.py
scripts/build_kids1000_lensing_inventory_v1.py
scripts/validate_kids1000_lensing_inventory_v1.py
```

The inventory finds `28` non-directory tarball members, `3` FITS products, and
exactly one selected COSEBIs FITS product for the future narrow lensing route.
This remains endpoint disabled and contains no lensing score.

The first COSEBIs FITS HDU policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_hdu_policy_v1.csv
data/derived/kids1000_cosebis_hdu_inventory_v1.csv
data/derived/kids1000_cosebis_hdu_inventory_v1_summary.csv
docs/kids1000_cosebis_hdu_policy_v1.md
scripts/build_kids1000_cosebis_hdu_inventory_v1.py
scripts/validate_kids1000_cosebis_hdu_inventory_v1.py
```

It freezes `COVMAT` as a `300x300` covariance matrix, `En` as a 300-row
COSEBIs data-vector table, and `NZ_SOURCE` as a 119-row redshift-distribution
table. The covariance is positive definite. This is still not a lensing
likelihood and contains no model residuals or fit statistics.

The COSEBIs tomographic/mode policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_mode_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_mode_inventory_v1.csv
data/derived/kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv
docs/kids1000_cosebis_tomographic_mode_policy_v1.md
scripts/build_kids1000_cosebis_tomographic_mode_inventory_v1.py
scripts/validate_kids1000_cosebis_tomographic_mode_inventory_v1.py
```

It freezes the selected `En` data-vector structure as `5` source bins, `15`
upper-triangular tomographic pairs, and `20` COSEBIs modes per pair, for `300`
rows. This is a source-side structure freeze only: it does not set a mode cut,
does not invert the covariance, and does not compute lensing predictions,
residuals, likelihood values, or Tau Core amplitudes.

The COSEBIs covariance-readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_covariance_readiness_policy_v1.csv
data/derived/kids1000_cosebis_covariance_readiness_v1.csv
data/derived/kids1000_cosebis_covariance_readiness_v1_summary.csv
docs/kids1000_cosebis_covariance_readiness_policy_v1.md
scripts/build_kids1000_cosebis_covariance_readiness_v1.py
scripts/validate_kids1000_cosebis_covariance_readiness_v1.py
```

It records only source-side covariance diagnostics for the selected `COVMAT`
block: shape, symmetry error, diagonal positivity, eigenvalue range, condition
number, and Cholesky readiness. It does not save an inverse covariance, select a
data-vector mask, choose a theory vector, or compute lensing scores.

The first COSEBIs mask/mode-cut policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_mask_modecut_policy_v1.csv
data/derived/kids1000_cosebis_mask_modecut_inventory_v1.csv
data/derived/kids1000_cosebis_mask_modecut_inventory_v1_summary.csv
docs/kids1000_cosebis_mask_modecut_policy_v1.md
scripts/build_kids1000_cosebis_mask_modecut_inventory_v1.py
scripts/validate_kids1000_cosebis_mask_modecut_inventory_v1.py
```

It retains all `300` source rows: all `15` tomographic pairs and modes `1..20`.
This deliberately avoids residual-based row or mode removal. It is not an
endpoint and does not define a theory vector, inverse covariance, likelihood, or
Tau Core lensing amplitude.

The first COSEBIs tomographic-pair retention-weight policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_weight_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_weight_inventory_v1.csv
data/derived/kids1000_cosebis_tomographic_weight_inventory_v1_summary.csv
docs/kids1000_cosebis_tomographic_weight_policy_v1.md
scripts/build_kids1000_cosebis_tomographic_weight_inventory_v1.py
scripts/validate_kids1000_cosebis_tomographic_weight_inventory_v1.py
```

It assigns unit source-retention weights to all `15` tomographic pairs. These
are not likelihood weights, fitted amplitudes, or covariance weights; they only
state that no pair is upweighted or downweighted using residuals, fit
statistics, posterior chains, or endpoint behavior.

The first COSEBIs covariance-subselection policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_covariance_subselection_policy_v1.csv
data/derived/kids1000_cosebis_covariance_subselection_inventory_v1.csv
data/derived/kids1000_cosebis_covariance_subselection_inventory_v1_summary.csv
docs/kids1000_cosebis_covariance_subselection_policy_v1.md
scripts/build_kids1000_cosebis_covariance_subselection_inventory_v1.py
scripts/validate_kids1000_cosebis_covariance_subselection_inventory_v1.py
```

It retains the full `300x300` covariance block because all `300` data-vector
rows are retained. It records the contiguous 20-row covariance intervals for
each of the `15` tomographic pairs, but it does not save an inverse covariance,
select a likelihood, or compute a lensing score.

The first COSEBIs covariance-inversion readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_covariance_inversion_policy_v1.csv
data/derived/kids1000_cosebis_covariance_inversion_readiness_v1.csv
data/derived/kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv
docs/kids1000_cosebis_covariance_inversion_policy_v1.md
scripts/build_kids1000_cosebis_covariance_inversion_readiness_v1.py
scripts/validate_kids1000_cosebis_covariance_inversion_readiness_v1.py
```

It freezes the future numerical solve policy as Cholesky solve on the full
`300x300` covariance, but explicitly does not execute the solve and does not
store an inverse covariance. A frozen theory vector and scoring protocol are
still required before any lensing likelihood can be evaluated.

The first COSEBIs theory-vector readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_theory_vector_policy_v1.csv
data/derived/kids1000_cosebis_theory_vector_readiness_v1.csv
data/derived/kids1000_cosebis_theory_vector_readiness_v1_summary.csv
docs/kids1000_cosebis_theory_vector_policy_v1.md
scripts/build_kids1000_cosebis_theory_vector_readiness_v1.py
scripts/validate_kids1000_cosebis_theory_vector_readiness_v1.py
```

It declares a future `300`-row COSEBIs theory vector for the active
`W_WEB_ANISOTROPY` and `W_PATH_PROJECTION` lensing route, but does not compute
the vector. It also forbids using KiDS data-vector values, posterior chains,
residuals, or fit-improvement flags to choose the theory vector.

The first COSEBIs web/path mapping readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv
data/derived/kids1000_cosebis_web_path_mapping_readiness_v1.csv
data/derived/kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv
docs/kids1000_cosebis_web_path_mapping_policy_v1.md
scripts/build_kids1000_cosebis_web_path_mapping_readiness_v1.py
scripts/validate_kids1000_cosebis_web_path_mapping_readiness_v1.py
```

It declares the source-side inputs required before a future `W_WEB_ANISOTROPY`
and `W_PATH_PROJECTION` COSEBIs theory vector can be built. It does not compute
a mapping, does not compute a theory vector, and forbids KiDS data-vector values,
posterior chains, residuals, fit-improvement flags, and post-hoc sky-direction
selection.

The first COSEBIs redshift-kernel inventory is recorded in:

```text
data/source_manifest/kids1000_cosebis_redshift_kernel_policy_v1.csv
data/derived/kids1000_cosebis_redshift_kernel_inventory_v1.csv
data/derived/kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv
docs/kids1000_cosebis_redshift_kernel_policy_v1.md
scripts/build_kids1000_cosebis_redshift_kernel_inventory_v1.py
scripts/validate_kids1000_cosebis_redshift_kernel_inventory_v1.py
```

It reads only the selected `NZ_SOURCE` table and records source-bin redshift
areas, mean redshifts, and support intervals for the five KiDS source bins. This
is a source-side kernel inventory, not a COSEBIs theory vector, lensing
prediction, residual, or likelihood score.

The first COSEBIs path mask/depth gap audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_mask_depth_gap_policy_v1.csv
data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1.csv
data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1_summary.csv
docs/kids1000_cosebis_path_mask_depth_gap_policy_v1.md
scripts/build_kids1000_cosebis_path_mask_depth_gap_inventory_v1.py
scripts/validate_kids1000_cosebis_path_mask_depth_gap_inventory_v1.py
```

It scans the selected KiDS-1000 cosmic-shear release tarball and records that no
standalone source-frozen footprint, path mask, depth map, random catalogue, or
equivalent path-load product is accepted from that tarball. Filename `mask`
tokens in the statistic FITS products are classified as statistic-product
metadata, not as survey path maps. The future `W_PATH_PROJECTION` route
therefore remains blocked on an external source-frozen path/mask/depth product.

The first official KiDS DR4 path-mask route-script freeze is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_route_scripts_v1.csv
data/raw/weak_lensing/kids1000_path_masks/kids_dr4.1_9band_msk_wget.sh
data/raw/weak_lensing/kids1000_path_masks/kids_dr4.0_9band_msk_wget.sh
data/raw/weak_lensing/kids1000_path_masks/kids_dr4.0_msk_wget.sh
data/derived/kids1000_dr4_path_mask_route_scripts_inventory_v1.csv
data/derived/kids1000_dr4_path_mask_route_scripts_inventory_v1_summary.csv
docs/kids1000_dr4_path_mask_route_scripts_v1.md
scripts/acquire_kids1000_dr4_path_mask_route_scripts_v1.py
scripts/validate_kids1000_dr4_path_mask_route_scripts_v1.py
```

This freezes the small official KiDS DR4 wget scripts that point to external
mask FITS products. The preferred DR4.1 9-band route script lists `196` mask
products. Those mask FITS files are not downloaded in this package, and no
path-mapping vector or COSEBIs theory vector is computed.

The preferred-route tile inventory is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_route_tile_inventory_policy_v1.csv
data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1.csv
data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv
docs/kids1000_dr4_path_mask_route_tile_inventory_policy_v1.md
scripts/build_kids1000_dr4_path_mask_route_tile_inventory_v1.py
scripts/validate_kids1000_dr4_path_mask_route_tile_inventory_v1.py
```

It parses all `196` preferred DR4.1 9-band mask-product URLs into
filename-derived tile coordinates. This gives a source-frozen route geometry
index, but still does not download the 196 mask products, compute a footprint
polygon, build a path map, or connect anything to COSEBIs rows.

The first preferred-route HEAD sample is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_head_sample_policy_v1.csv
data/derived/kids1000_dr4_path_mask_head_sample_v1.csv
data/derived/kids1000_dr4_path_mask_head_sample_v1_summary.csv
docs/kids1000_dr4_path_mask_head_sample_policy_v1.md
scripts/check_kids1000_dr4_path_mask_head_sample_v1.py
scripts/validate_kids1000_dr4_path_mask_head_sample_v1.py
```

It checks only the first, middle, and last mask-product URLs from the preferred
DR4.1 9-band route. All three return HTTP `200` with FITS content and positive
content length. This is an availability sanity check only: the mask FITS files
are not downloaded and no path mapping is computed.

The first source-frozen KiDS DR4 path-mask subset inventory is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_subset_policy_v1.csv
data/raw/weak_lensing/kids1000_path_masks/mask_subset_v1/
data/derived/kids1000_dr4_path_mask_subset_inventory_v1.csv
data/derived/kids1000_dr4_path_mask_subset_inventory_v1_summary.csv
docs/kids1000_dr4_path_mask_subset_policy_v1.md
scripts/acquire_kids1000_dr4_path_mask_subset_v1.py
scripts/validate_kids1000_dr4_path_mask_subset_v1.py
```

It downloads and hash-freezes the first/middle/last DR4.1 9-band mask FITS
products from the predeclared HEAD sample, then records FITS image shape and
basic finite/nonzero pixel summaries. The three masks total `15,091,583` bytes
and `1,323,000,000` image pixels. This still does not compute a path map, does
not connect masks to COSEBIs rows, and does not score a lensing model.

The first source-only mask observable shell is recorded in:

```text
data/source_manifest/kids1000_dr4_path_mask_observable_shell_policy_v1.csv
data/derived/kids1000_dr4_path_mask_observable_shell_v1.csv
data/derived/kids1000_dr4_path_mask_observable_shell_v1_summary.csv
docs/kids1000_dr4_path_mask_observable_shell_policy_v1.md
scripts/build_kids1000_dr4_path_mask_observable_shell_v1.py
scripts/validate_kids1000_dr4_path_mask_observable_shell_v1.py
```

It parses only filename tile coordinates and the subset inventory's nonzero
mask-pixel fractions, then builds a centered zero-fraction shell across the
three frozen masks. This is a pre-mapping source observable only: mask-value
semantics are not interpreted as a physical lensing path weight, no COSEBIs-row
mapping is constructed, and no theory vector or endpoint score is computed.

The first COSEBIs path-mapping design skeleton is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_mapping_design_skeleton_policy_v1.csv
data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1.csv
data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1_summary.csv
docs/kids1000_cosebis_path_mapping_design_skeleton_policy_v1.md
scripts/build_kids1000_cosebis_path_mapping_design_skeleton_v1.py
scripts/validate_kids1000_cosebis_path_mapping_design_skeleton_v1.py
```

It builds the 300-row future mapping layout from COSEBIs row structure,
tomographic-pair redshift summaries, and the preferred 196-tile route span. It
does not compute tile/path weights, a path mapping vector, a theory vector,
predictions, residuals, or endpoint scores.

The full target-row by route-tile domain skeleton is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.csv
data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1.csv
data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1_summary.csv
docs/kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.md
scripts/build_kids1000_cosebis_path_mapping_domain_skeleton_v1.py
scripts/validate_kids1000_cosebis_path_mapping_domain_skeleton_v1.py
```

It forms the complete `300 x 196 = 58,800` source-side mapping domain from
COSEBIs target rows and preferred-route tiles. It still does not compute
footprint overlap, tile weights, path weights, web-environment labels, a mapping
vector, a theory vector, predictions, residuals, or scores.

The path-weight construction-rule ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_weight_construction_rule_v1.csv
data/derived/kids1000_cosebis_path_weight_construction_rule_v1.csv
data/derived/kids1000_cosebis_path_weight_construction_rule_v1_summary.csv
docs/kids1000_cosebis_path_weight_construction_rule_v1.md
scripts/build_kids1000_cosebis_path_weight_construction_rule_v1.py
scripts/validate_kids1000_cosebis_path_weight_construction_rule_v1.py
```

It declares the future factorization
`N_pair * T_tile * F_overlap * D_path * E_web * C_norm` and records which
factors are source-supported. The rule is not computable yet: footprint overlap
and web-environment factors are missing, the path/mask factor is only partial,
and no numeric weight or mapping vector is produced.

The source-factor acquisition plan is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_factor_acquisition_plan_v1.csv
data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1.csv
data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1_summary.csv
docs/kids1000_cosebis_path_factor_acquisition_plan_v1.md
scripts/build_kids1000_cosebis_path_factor_acquisition_plan_v1.py
scripts/validate_kids1000_cosebis_path_factor_acquisition_plan_v1.py
```

It converts the missing-factor status into seven source-side acquisition
requirements. Four requirements block numeric path-weight computation:
footprint/row-tile overlap, full path/depth support, web/environment support,
and normalization after nonzero factors exist. It fetches no products and
computes no weights.

The source-product route candidate manifest is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_source_product_route_policy_v1.csv
data/derived/kids1000_cosebis_path_source_product_route_manifest_v1.csv
data/derived/kids1000_cosebis_path_source_product_route_manifest_v1_summary.csv
docs/kids1000_cosebis_path_source_product_route_policy_v1.md
scripts/build_kids1000_cosebis_path_source_product_route_manifest_v1.py
scripts/validate_kids1000_cosebis_path_source_product_route_manifest_v1.py
```

It declares ten source-product routes for the next source-gathering step:
two already-supported locks, five blocker-resolving candidates, and three
control/deferred routes. It still fetches no external products, computes no
factor values, and creates no path mapping or score.

The blocker-resolution order policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_blocker_resolution_order_policy_v1.csv
data/derived/kids1000_cosebis_path_blocker_resolution_order_v1.csv
data/derived/kids1000_cosebis_path_blocker_resolution_order_v1_summary.csv
docs/kids1000_cosebis_path_blocker_resolution_order_policy_v1.md
scripts/build_kids1000_cosebis_path_blocker_resolution_order_v1.py
scripts/validate_kids1000_cosebis_path_blocker_resolution_order_v1.py
```

It freezes the future source-side order: `F_overlap` first, then `D_path`,
then `E_web`, then `C_norm`, then a mapping vector, then null controls. It
fetches no products and keeps mapping and endpoint scoring disabled.

The first-blocker `F_overlap` rule shell is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_rule_shell_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_rule_shell_v1.csv
data/derived/kids1000_cosebis_f_overlap_rule_shell_v1_summary.csv
docs/kids1000_cosebis_f_overlap_rule_shell_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_rule_shell_v1.py
scripts/validate_kids1000_cosebis_f_overlap_rule_shell_v1.py
```

It declares the accepted future output schema for the row-tile overlap factor
over the full `300 x 196 = 58,800` target-row by route-tile domain. It accepts
only source-frozen official footprint geometry or source-native full-mask
overlap derivations. It computes no overlap values and still forbids mapping
and scoring.

The `F_overlap` source-availability audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_source_availability_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_source_availability_v1.csv
data/derived/kids1000_cosebis_f_overlap_source_availability_v1_summary.csv
docs/kids1000_cosebis_f_overlap_source_availability_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_source_availability_v1.py
scripts/validate_kids1000_cosebis_f_overlap_source_availability_v1.py
```

It records that the route script and three-mask subset are not sufficient for a
full overlap rule. No official footprint geometry product or full 196-mask
source-native product set is currently accepted, so `F_overlap` remains
unresolved and mapping remains disabled.

The `F_overlap` full-mask acquisition manifest is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.py
```

It expands the preferred route into a 196-row acquisition manifest. Three mask
products are currently present locally and 193 remain missing; therefore the
full-mask source-native route is not accepted for `F_overlap` yet.

The `F_overlap` full-mask batch plan is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_batch_plan_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.py
```

It splits the 193 missing mask products into ten future acquisition batches of
at most 20 files each. Future large FITS products are assigned to an ignored
cache directory; only manifests and derived summaries should be committed.

The first `F_overlap` batch dry run is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.md
scripts/acquire_kids1000_cosebis_f_overlap_full_mask_batch_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.py
```

The public reproduction path runs this script only in dry-run mode on batch 0.
It inspects the 20 planned product URLs and cache paths without fetching any
large FITS product, without computing overlap fractions, without constructing a
path-mapping vector, and without enabling endpoint scoring. Manual acquisition
is available only through the explicit `--execute` option; outputs from that
mode are written under ignored `data/local/` execution logs plus the ignored
full-route FITS cache. They remain outside the public reproduce path until
separately reviewed, checksum-frozen, and promoted through a source-freeze
artifact.

The COSEBIs path-mapping source-preflight ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_mapping_source_preflight_policy_v1.csv
data/derived/kids1000_cosebis_path_mapping_source_preflight_v1.csv
data/derived/kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv
docs/kids1000_cosebis_path_mapping_source_preflight_policy_v1.md
scripts/build_kids1000_cosebis_path_mapping_source_preflight_v1.py
scripts/validate_kids1000_cosebis_path_mapping_source_preflight_v1.py
```

It summarizes the current source-side state for a future path-aware COSEBIs
endpoint: target row structure, redshift kernels, the 196-tile route coordinate
index, the 300-row design skeleton, and the 58,800-row target-tile domain
skeleton are available; the path-weight construction rule is declared but not
computable; the three-mask observable shell is only partial; the full path/depth
footprint mapping and web-environment catalogue remain missing; and null
controls are declared but not executed. It contains no mapping vector, theory
vector, predictions, residuals, or scores.

The first COSEBIs null-control readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_null_control_policy_v1.csv
data/derived/kids1000_cosebis_null_control_readiness_v1.csv
data/derived/kids1000_cosebis_null_control_readiness_v1_summary.csv
docs/kids1000_cosebis_null_control_policy_v1.md
scripts/build_kids1000_cosebis_null_control_readiness_v1.py
scripts/validate_kids1000_cosebis_null_control_readiness_v1.py
```

It declares four future null-control families: sky rotation, tomographic-pair
shuffle, wrong-channel activation, and web/path sign flip. These controls are
not run yet; seed and multiplicity policies must be frozen before any null
scores can be interpreted.

The first COSEBIs null-control seed and multiplicity policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_null_control_seed_policy_v1.csv
data/derived/kids1000_cosebis_null_control_seed_inventory_v1.csv
data/derived/kids1000_cosebis_null_control_seed_inventory_v1_summary.csv
docs/kids1000_cosebis_null_control_seed_policy_v1.md
scripts/build_kids1000_cosebis_null_control_seed_inventory_v1.py
scripts/validate_kids1000_cosebis_null_control_seed_inventory_v1.py
```

It freezes deterministic family seeds and planned multiplicities for the four
future null-control families, totaling `1008` declared future control draws. It
does not execute controls and contains no control scores, predictions,
residuals, or fit statistics.

The first tiny pilot product freeze is recorded in:

```text
data/source_manifest/pilot_frozen_product_manifest.csv
docs/pilot_product_freeze_001.md
```

It freezes three public distance-side files for provenance and covariance-shape
testing only: one Cosmic Chronometers table, one Pantheon+ distance table, and
one Pantheon+ STAT+SYS covariance matrix. All rows remain
`endpoint_allowed=false`.

The first Pantheon+ endpoint-eligible scope declaration is recorded in:

```text
data/source_manifest/pantheon_endpoint_scope_v1.csv
data/derived/pantheon_scope_v1_summary.csv
docs/pantheon_endpoint_scope_v1.md
```

It freezes a residual-blind row rule and covariance-submatrix policy, but it is
still `SCOPE_FROZEN_NOT_SCORED`.

The first scoring grammar is frozen here:

```text
data/source_manifest/pantheon_scoring_protocol_v1.csv
docs/pantheon_scoring_protocol_v1.md
```

It declares the baseline family, nuisance policy, Tau activation family, and
required future controls. It also keeps endpoint `scoring_allowed=false`.

The dry-run design matrix is frozen here:

```text
data/source_manifest/pantheon_design_matrix_protocol_v1.csv
data/derived/pantheon_design_matrix_v1.csv
data/derived/pantheon_design_matrix_v1_summary.csv
docs/pantheon_design_matrix_v1.md
```

It contains source and activation-basis columns only. It contains no model
predictions, residuals, likelihoods, or fit statistics.

The first Pantheon+ numerical smoke test is recorded here:

```text
data/source_manifest/pantheon_pilot_scoring_v1.csv
data/derived/pantheon_pilot_scoring_v1_summary.csv
data/derived/pantheon_pilot_scoring_v1_grid.csv
docs/pantheon_pilot_scoring_v1.md
```

This is a diagonal-covariance pilot score, not endpoint validation. On the
current frozen grid, the Tau late-activation shell improves diagonal-covariance
\(\chi^2\) by only `0.084` relative to the flat-Lambda-CDM branch, while its
AIC is worse by `5.916` because the Tau shell carries more effective
parameters. This is therefore a reproducible scoring-pipeline smoke test, not
evidence for dark energy or for Tau Core cosmology.

The pilot diagnostic figure is generated reproducibly from the frozen grid:

```text
scripts/build_figures.py
figures/fig_pantheon_full_cov_pilot_branch_diagnostics.pdf
paper10_submission_source/figures/fig_pantheon_full_cov_pilot_branch_diagnostics.pdf
```

The first full-covariance pilot repeats the same frozen branch grammar using
the retained Pantheon+ STAT+SYS covariance submatrix with Cholesky solves:

```text
data/source_manifest/pantheon_full_cov_pilot_scoring_v1.csv
data/derived/pantheon_full_cov_pilot_scoring_v1_summary.csv
data/derived/pantheon_full_cov_pilot_scoring_v1_grid.csv
docs/pantheon_full_cov_pilot_scoring_v1.md
```

It gives `Delta chi2 = -0.192` for the Tau shell relative to flat-Lambda-CDM,
but `Delta AIC = +5.808`. This preserves the same conclusion as the diagonal
smoke test: the scoring ladder works, but this is not evidence for a new
cosmological model.

The first two-channel full-covariance proxy pilot is:

```text
data/source_manifest/pantheon_void_web_proxy_full_cov_pilot_v1.csv
data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_summary.csv
data/derived/pantheon_void_web_proxy_full_cov_pilot_v1_grid.csv
docs/pantheon_void_web_proxy_full_cov_pilot_v1.md
```

It activates only `W_VOID_MATURITY` and `W_WEB_ANISOTROPY`; `W_PATH_PROJECTION`
and `W_TIME_READOUT` remain disabled. Because no source-native void/web product
values are frozen yet, the current bases are leakage-safe redshift/scale-factor
proxies. This is a two-channel scoring-grammar stress test, not a void/web
detection. The current full-covariance distance-only proxy result is
`Delta chi2 = -0.05994162` and `Delta AIC = +3.94005838`, so it is
model-selection negative despite a tiny chi-square improvement.

The multi-probe full-covariance endpoint plan is recorded in:

```text
docs/multi_probe_full_cov_scoring_plan_v1.md
```

That future gate must combine distance, growth, lensing, and CMB-safety blocks.
It is not implemented in this scaffold.

## General Tau Core Readout Continuation

The weak full-covariance Pantheon+ pilot should be read primarily as a
limitation of the homogeneous late-activation shell, not as a true negative
against the broader Tau Core morphology/projection-readout framework. The
current pilot tests only one smooth proxy:

```text
W_tau(a)
```

The next step is not to import the galaxy TPG bridge itself. Rather, it is to
use the general Tau Core readout principle made explicit by the galactic bridge
discipline:
four-dimensional residuals may be readouts of deeper morphology/projection
channels. In cosmology this requires source-frozen channel families:

```text
W_void(a)          void maturity / distance activation
W_web(a,k,env)     cosmic-web anisotropy for growth and lensing
W_path(z,n_hat)    observer/path projection along the null-geodesic bundle
W_time(a)          time/readout projection for observed a(t), H(t)
```

These channels must be frozen from independent source-side observables before
distance, growth, lensing, or CMB-safety residuals are scored.

## Scope

This is a protocol scaffold and branch-opening paper package. The next
scientific milestone is a real-data pilot using public distance, void,
cosmic-web, growth, lensing, and CMB products under the frozen audit ladder.

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
data/source_manifest/kids1000_cosebis_theory_vector_template_policy_v1.csv
data/derived/kids1000_cosebis_theory_vector_template_v1.csv
data/derived/kids1000_cosebis_theory_vector_template_v1_summary.csv
docs/kids1000_cosebis_theory_vector_template_v1.md
scripts/build_kids1000_cosebis_theory_vector_template_v1.py
scripts/validate_kids1000_cosebis_theory_vector_template_v1.py
data/source_manifest/kids1000_cosebis_source_frozen_theory_vector_policy_v1.csv
data/derived/kids1000_cosebis_source_frozen_theory_vector_v1.csv
data/derived/kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv
docs/kids1000_cosebis_source_frozen_theory_vector_v1.md
scripts/build_kids1000_cosebis_source_frozen_theory_vector_v1.py
scripts/validate_kids1000_cosebis_source_frozen_theory_vector_v1.py
data/source_manifest/kids1000_cosebis_mapping_template_join_contract_policy_v1.csv
data/derived/kids1000_cosebis_mapping_template_join_contract_v1.csv
data/derived/kids1000_cosebis_mapping_template_join_contract_v1_summary.csv
docs/kids1000_cosebis_mapping_template_join_contract_v1.md
scripts/build_kids1000_cosebis_mapping_template_join_contract_v1.py
scripts/validate_kids1000_cosebis_mapping_template_join_contract_v1.py
```

It declares the `300`-row COSEBIs theory-vector gate for the active
`W_WEB_ANISOTROPY` and `W_PATH_PROJECTION` lensing route. The parent policy
remains endpoint-disabled and declarative. A separate source-frozen,
unit-amplitude theory-vector shell is now computed from the frozen mapping basis
and a predeclared unit-mean `mode^{-1/2}` mode-shape rule. This shell forbids
KiDS data-vector values, posterior chains, residuals, fit-improvement flags,
post-hoc mode cuts, and post-hoc amplitude calibration. It is not endpoint
scoring and not empirical validation.
The accompanying template freezes the 300-row tomographic-pair/mode interface
with empty theory-value and channel-contribution fields. It is a row-index
template only, not a prediction.
The mapping-to-template join contract then freezes the future source-frozen
join key and required mapping columns for that same 300-row interface. It does
not fill any mapping value, theory value, channel contribution, prediction, or
score.

The first COSEBIs web/path mapping readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv
data/derived/kids1000_cosebis_web_path_mapping_readiness_v1.csv
data/derived/kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv
docs/kids1000_cosebis_web_path_mapping_policy_v1.md
scripts/build_kids1000_cosebis_web_path_mapping_readiness_v1.py
scripts/validate_kids1000_cosebis_web_path_mapping_readiness_v1.py
data/source_manifest/kids1000_cosebis_source_frozen_mapping_vector_policy_v1.csv
data/derived/kids1000_cosebis_source_frozen_mapping_domain_weights_v1.csv
data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1.csv
data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv
docs/kids1000_cosebis_source_frozen_mapping_vector_v1.md
scripts/build_kids1000_cosebis_source_frozen_mapping_vector_v1.py
scripts/validate_kids1000_cosebis_source_frozen_mapping_vector_v1.py
```

It declares the source-side inputs required before a future `W_WEB_ANISOTROPY`
and `W_PATH_PROJECTION` COSEBIs theory vector can be built. The current release
now includes a source-frozen 300-row mapping basis with 15 tomographic-pair
values. This basis has pair/redshift/path variation, but no COSEBIs mode-shape
and no theory value; `W_web` remains a zero null-control channel. It therefore
does not compute a theory vector, prediction, residual, fit statistic, or score,
and forbids KiDS data-vector values, posterior chains, residuals,
fit-improvement flags, and post-hoc sky-direction selection.

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

The source-side normalization rule is recorded in:

```text
data/source_manifest/kids1000_cosebis_c_norm_source_side_rule_policy_v1.csv
data/derived/kids1000_cosebis_c_norm_source_side_domain_rule_v1.csv
data/derived/kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv
docs/kids1000_cosebis_c_norm_source_side_rule_v1.md
scripts/build_kids1000_cosebis_c_norm_source_side_rule_v1.py
scripts/validate_kids1000_cosebis_c_norm_source_side_rule_v1.py
```

It declares the future factorization
`N_pair * T_tile * F_overlap * D_path * E_web * C_norm` and records which
factors are source-supported. The source-weight rule is now source-side computable: `F_overlap` has
non-degenerate source support from the full-route pixel-fraction rule,
`D_path` has caveated non-degenerate source support from the full-route
mask-load proxy, `E_web` is source-supported only as a uniform null-web
control, and `C_norm = 2.110707798749` normalizes the frozen raw source-factor
product to unit mean over the 58,800-row domain. This does not make a positive
web/environment claim. No mapping vector, theory vector, residual, or endpoint
score is produced.

The source-factor acquisition plan is recorded in:

```text
data/source_manifest/kids1000_cosebis_path_factor_acquisition_plan_v1.csv
data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1.csv
data/derived/kids1000_cosebis_path_factor_acquisition_plan_v1_summary.csv
docs/kids1000_cosebis_path_factor_acquisition_plan_v1.md
scripts/build_kids1000_cosebis_path_factor_acquisition_plan_v1.py
scripts/validate_kids1000_cosebis_path_factor_acquisition_plan_v1.py
```

It converts the source-factor status into seven source-side acquisition
requirements. At the current stage none of the seven requirements blocks the
source-weight algebra: source-side normalization is resolved after the nonzero
source factors and the null-web control exist. It fetches no products and
computes no endpoint weights. The next blocker is the mapping vector.

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
six already-supported locks/routes, no remaining blocker-resolving candidate
before the mapping vector, two alternative-not-needed routes, one unfetched
external web route kept as a future positive-web option, and one deferred null-control route. The supported
`E_web` route is a null-web control only; the external web/environment catalogue
route remains unfetched and does not support a positive web claim. The manifest
still fetches no external products, creates no path mapping, and computes no
score.

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
records that `F_overlap`, a caveated `D_path` mask-load proxy, a uniform
null-web `E_web` control, and source-side `C_norm` are now supported. The first
remaining blocker is the mapping vector. It fetches no products and keeps
mapping and endpoint scoring disabled.

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

It expands the preferred route into a 196-row acquisition manifest. In the
public reproduce path this manifest remains conservative: the package contains
the three committed sample masks and records the remaining 193 products as
fetch-required. A separate author-local full-route cache inventory, described
below, records a completed source-cache snapshot without making the large raw
FITS cache part of the public package.

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

The author-local full-route cache inventory is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_route_cache_inventory_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.md
scripts/build_kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.py
```

This local snapshot accounts for all 196 expected mask products: 193 products
in the ignored `data/raw/weak_lensing/kids1000_path_masks/full_route_cache_v1/`
cache plus the three committed subset masks. Each product is recorded with a
relative path, byte size, and SHA-256 hash. Public reproduction does not require
the ignored raw cache; it uses the committed inventory snapshot only. The
inventory does not compute overlap fractions, path mapping, a theory vector,
predictions, residuals, or scores. It moves the first `F_overlap` blocker from
"source products missing" to "derive a source-frozen full-mask overlap rule
without endpoint inputs."

The first source-frozen full-route overlap rule candidate is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_header_footprint_rule_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_tile_rule_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_rule_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_rule_v1_summary.csv
docs/kids1000_cosebis_f_overlap_header_footprint_rule_v1.md
scripts/build_kids1000_cosebis_f_overlap_header_footprint_rule_v1.py
scripts/validate_kids1000_cosebis_f_overlap_header_footprint_rule_v1.py
```

It derives a header-WCS area proxy from the 196 mask products and attaches it
to the full `300 x 196 = 58,800` target-row by route-tile domain. This is a
source-only `F_overlap` rule candidate, but it does not read pixel-mask values
and does not construct a path mapping or score.

The corresponding degeneracy audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.csv
data/derived/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1_summary.csv
docs/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.md
scripts/build_kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.py
scripts/validate_kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.py
```

The audit preserves an important negative result: all route tiles have the
same header-footprint area at this precision, so `F_overlap=1` for every tile.
This rule is source-frozen and leakage-safe, but it is too uniform to support a
non-degenerate endpoint mapping. The next scoring-facing `F_overlap` step is a
pixel-mask or sub-tile overlap rule derived without endpoint inputs.

The first pixel-content `F_overlap` pilot is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_pixel_fraction_pilot_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_pixel_fraction_pilot_tile_v1.csv
data/derived/kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1_summary.csv
docs/kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.md
scripts/build_kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.py
scripts/validate_kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1.py
```

It uses only the three committed, source-frozen mask products and their
upstream parsed finite/nonzero pixel fractions. Unlike the header footprint
proxy, this pixel-content pilot is non-uniform (`F_overlap` ranges from about
`0.866` to `1.000` on the subset). This is a proof-of-method result, not a
population endpoint: it resolves the header-uniformity concern only for the
subset and motivates a full-route streaming/cache pixel or sub-tile extractor.

The source-frozen full-route pixel-fraction `F_overlap` rule is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_tile_rule_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.csv
data/derived/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1_summary.csv
docs/kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.md
scripts/build_kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.py
scripts/validate_kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.py
```

It reads the 196 source mask products from the local full-route cache plus the
committed subset masks, computes a finite/nonzero pixel-content fraction for
each route tile, and attaches the resulting source-only factor to the full
`300 x 196 = 58,800` target-row by route-tile domain. The rule is
non-degenerate (`F_overlap` ranges from about `0.453` to `1.000`, with 196
rounded unique tile values). This resolves the `F_overlap` source blocker, but
it still computes no path mapping, theory vector, prediction, residual, or
score. Public reproduction validates the committed outputs; rebuilding them
requires the ignored local raw mask cache documented in the full-route cache
inventory.

The source-frozen full-route `D_path` mask-load proxy is recorded in:

```text
data/source_manifest/kids1000_cosebis_d_path_full_route_mask_load_rule_policy_v1.csv
data/derived/kids1000_cosebis_d_path_full_route_mask_load_tile_rule_v1.csv
data/derived/kids1000_cosebis_d_path_full_route_mask_load_rule_v1.csv
data/derived/kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv
docs/kids1000_cosebis_d_path_full_route_mask_load_rule_v1.md
scripts/build_kids1000_cosebis_d_path_full_route_mask_load_rule_v1.py
scripts/validate_kids1000_cosebis_d_path_full_route_mask_load_rule_v1.py
```

It uses the same 196 source mask products, but extracts a different observable:
the mean nonzero mask value per tile, normalized by the maximum tile mean. This
is not a calibrated survey-depth map; it is a caveated source-side mask-load
proxy. It is non-degenerate (`D_path` ranges from about `0.508` to `1.000`) and
is not identical to the `F_overlap` coverage channel. This resolves the
`D_path` source blocker only as a mask-load proxy; it still computes no mapping
vector, theory vector, prediction, residual, or endpoint score.

The source-frozen `E_web` null-control rule is recorded in:

```text
data/source_manifest/kids1000_cosebis_e_web_null_control_rule_policy_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_tile_rule_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_rule_v1.csv
data/derived/kids1000_cosebis_e_web_null_control_rule_v1_summary.csv
docs/kids1000_cosebis_e_web_null_control_rule_v1.md
scripts/build_kids1000_cosebis_e_web_null_control_rule_v1.py
scripts/validate_kids1000_cosebis_e_web_null_control_rule_v1.py
```

It freezes `E_web(tile)=1` for all 196 route tiles and all 58,800 domain rows.
This is intentionally uniform and therefore is not a non-degenerate
web/environment measurement. It resolves the web gate only as a path-only
null-control route with no positive web claim, and computes no mapping vector,
theory vector, prediction, residual, or endpoint score.

The `F_overlap` batch-promotion review checklist is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_batch_promotion_review_v1.csv
data/derived/kids1000_cosebis_f_overlap_batch_promotion_review_v1_summary.csv
docs/kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_batch_promotion_review_v1.py
scripts/validate_kids1000_cosebis_f_overlap_batch_promotion_review_v1.py
```

It is currently expected to remain `promotion_ready=false`: there is no
committed fetched-batch review artifact, no checksum manifest for fetched
products, and no forbidden-input audit for a fetched batch. This checklist
does not read ignored `data/local/` execution logs and computes no overlap
rule, mapping vector, theory vector, prediction, residual, or score.
The checklist also records the availability of the filled-review validator as a
satisfied-but-not-promoting item; this makes the future review path more
auditable without changing the current negative promotion status.

The future fetched-batch execution-review schema is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1.csv
data/derived/kids1000_cosebis_f_overlap_execution_review_schema_v1_summary.csv
docs/kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_execution_review_schema_v1.py
scripts/validate_kids1000_cosebis_f_overlap_execution_review_schema_v1.py
```

It freezes the required columns for a later committed fetched-batch review
artifact: product identity, URL, cache path, HTTP status, byte count, SHA-256,
review status, reviewer role, forbidden-input flags, and claim-boundary flags.
It does not fetch products or promote a batch.

The default batch-0 execution-review template is recorded in:

```text
data/source_manifest/kids1000_cosebis_f_overlap_execution_review_template_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1.csv
data/derived/kids1000_cosebis_f_overlap_execution_review_template_v1_summary.csv
docs/kids1000_cosebis_f_overlap_execution_review_template_policy_v1.md
scripts/build_kids1000_cosebis_f_overlap_execution_review_template_v1.py
scripts/validate_kids1000_cosebis_f_overlap_execution_review_template_v1.py
docs/kids1000_cosebis_f_overlap_filled_execution_review_validator_v1.md
scripts/validate_kids1000_cosebis_f_overlap_filled_execution_review_artifact_v1.py
data/source_manifest/kids1000_cosebis_f_overlap_resolution_decision_policy_v1.csv
data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1.csv
data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv
docs/kids1000_cosebis_f_overlap_resolution_decision_v1.md
scripts/build_kids1000_cosebis_f_overlap_resolution_decision_v1.py
scripts/validate_kids1000_cosebis_f_overlap_resolution_decision_v1.py
data/source_manifest/kids1000_cosebis_partial_control_scoring_protocol_v1.csv
docs/kids1000_cosebis_partial_control_scoring_protocol_v1.md
scripts/validate_kids1000_cosebis_partial_control_scoring_protocol_v1.py
data/source_manifest/kids1000_cosebis_partial_control_mapping_shell_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_shell_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_shell_v1_summary.csv
docs/kids1000_cosebis_partial_control_mapping_shell_v1.md
scripts/build_kids1000_cosebis_partial_control_mapping_shell_v1.py
scripts/validate_kids1000_cosebis_partial_control_mapping_shell_v1.py
```

It materializes the 20 planned batch-0 product rows using the frozen
execution-review schema, but keeps all network, checksum, timestamp, and
reviewer fields empty or pending. It is a reviewer template, not an execution
log or source-freeze artifact.

The filled execution-review validator is a utility for checking either this
committed empty template (`--mode template`) or a future manually filled
execution-review artifact (`--mode filled`) against the frozen schema and
batch-0 dry-run identities. It does not fetch products, promote a batch,
derive an overlap rule, construct a path-mapping vector, or enable endpoint
scoring.
The F-overlap resolution decision gate records the current formal blocker
decision: no endpoint-grade overlap route is accepted; the three source-frozen
mask products are accepted only as a caveated partial path-mask control; the
official-geometry and batch-0 dry-run routes remain unresolved. The
full-196-mask route is now source-cache complete in the committed local
inventory snapshot. A source-frozen header-footprint rule has also been
derived, but the degeneracy audit shows it is uniform and not promotable as a
non-degenerate endpoint mapping support. The route remains endpoint-disabled
until a pixel-mask or sub-tile overlap rule is derived without endpoint inputs.
The partial-control scoring protocol freezes only a future diagnostic grammar
for that caveated three-mask control. It keeps both partial-control scoring and
endpoint scoring disabled and emits no score artifacts.
The partial-control mapping shell materializes the `300 x 3 = 900` source-side
support table linking the COSEBIs template rows to the three caveated mask
controls. It carries mask-shell observables and row identities only; no mapping
value, theory vector, residual, or score is computed.
The subsequent partial-control mapping-values artifact applies a frozen
source-only diagnostic rule to that same `900`-row support table:
`source_mask_shell_value * normalized_pair_mean_z_weight * mode^{-1/2}`.
The mean-redshift weight comes from the source-frozen KiDS `NZ_SOURCE`
inventory and the mode weight comes from COSEBIs row structure. This is a
caveated partial-control mapping-value vector only; it is not an endpoint
mapping vector, not a COSEBIs theory vector, and still emits no residual,
likelihood, score, AIC value, or validation result.

```text
data/source_manifest/kids1000_cosebis_partial_control_mapping_values_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_values_v1.csv
data/derived/kids1000_cosebis_partial_control_mapping_values_v1_summary.csv
docs/kids1000_cosebis_partial_control_mapping_values_v1.md
scripts/build_kids1000_cosebis_partial_control_mapping_values_v1.py
scripts/validate_kids1000_cosebis_partial_control_mapping_values_v1.py
```
The partial-control design matrix then reduces those `900` mapping values to
six deterministic `300`-row diagnostic branches: `baseline_zero`,
`mask_sample_0`, `mask_sample_98`, `mask_sample_195`, `positive_mask_mean`, and
`sign_flip_positive_mean`. This is scoring-facing support only; it is not an
endpoint theory vector and still does not use the KiDS data vector, covariance
solve, residuals, fit statistics, or post-hoc branch selection.

```text
data/source_manifest/kids1000_cosebis_partial_control_design_matrix_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_design_matrix_v1.csv
data/derived/kids1000_cosebis_partial_control_design_matrix_v1_summary.csv
docs/kids1000_cosebis_partial_control_design_matrix_v1.md
scripts/build_kids1000_cosebis_partial_control_design_matrix_v1.py
scripts/validate_kids1000_cosebis_partial_control_design_matrix_v1.py
```
The first caveated partial-control diagnostic score is recorded in:

```text
data/source_manifest/kids1000_cosebis_partial_control_diagnostic_scoring_v1.csv
data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_grid.csv
data/derived/kids1000_cosebis_partial_control_diagnostic_scoring_v1_summary.csv
docs/kids1000_cosebis_partial_control_diagnostic_scoring_v1.md
scripts/run_kids1000_cosebis_partial_control_diagnostic_scoring_v1.py
scripts/validate_kids1000_cosebis_partial_control_diagnostic_scoring_v1.py
```

This run compares the frozen 300x6 branch matrix to the retained KiDS COSEBIs
`En` data vector using the full 300x300 covariance and a nonnegative
one-amplitude-per-branch rule. It improves the zero-branch diagnostic
chi-square by about `183.6`, but it is explicitly not endpoint validation. In
this simplified control, the positive mask branches are effectively
amplitude-degenerate, so the result should be read only as a successful
diagnostic scoring smoke test for the partial-control route.

The corresponding null replay is recorded in:

```text
data/source_manifest/kids1000_cosebis_partial_control_null_replay_v1.csv
data/derived/kids1000_cosebis_partial_control_null_replay_v1_grid.csv
data/derived/kids1000_cosebis_partial_control_null_replay_v1_summary.csv
docs/kids1000_cosebis_partial_control_null_replay_v1.md
scripts/run_kids1000_cosebis_partial_control_null_replay_v1.py
scripts/validate_kids1000_cosebis_partial_control_null_replay_v1.py
```

This replay compares the observed positive-mask diagnostic branch against
`1008` deterministic controls: sky rotations, tomographic-pair shuffles,
wrong-channel activations, and sign-flip controls. One pair-shuffle null
slightly outperforms the observed branch, so the observed branch is not an
absolute winner. The conservative plus-one tail fraction is `0.001982160555`.
This is a diagnostic rarity check only, not endpoint validation and not a
KiDS lensing population claim.

The partial-control degeneracy audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_partial_control_degeneracy_audit_policy_v1.csv
data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_pair_grid.csv
data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_summary.csv
docs/kids1000_cosebis_partial_control_degeneracy_audit_v1.md
scripts/build_kids1000_cosebis_partial_control_degeneracy_audit_v1.py
scripts/validate_kids1000_cosebis_partial_control_degeneracy_audit_v1.py
```

It shows that the positive partial-control branches are effectively rank one:
their covariance-metric absolute cosine is numerically unity and the maximum
positive-branch relative shape residual is about `2.2e-12`. This remains a
preserved negative result for the caveated three-mask partial-control route. It
is not erased by later gates: the partial-control branch is still unsuitable as
an endpoint family on its own.

The endpoint-family geometry audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_family_geometry_audit_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_family_geometry_audit_v1.csv
data/derived/kids1000_cosebis_endpoint_family_geometry_audit_v1_summary.csv
docs/kids1000_cosebis_endpoint_family_geometry_audit_v1.md
scripts/build_kids1000_cosebis_endpoint_family_geometry_audit_v1.py
scripts/validate_kids1000_cosebis_endpoint_family_geometry_audit_v1.py
```

This audit replaces the three-mask partial-control geometry as the
endpoint-readiness geometry test. It uses the source-frozen candidate theory
shell plus the predeclared source-frozen null-control theory replay, with the
KiDS covariance used only as a geometry metric. It does not read the KiDS `En`
data-vector values, residuals, posterior chains, fit statistics, or endpoint
scores. The resulting endpoint comparison family has `1009` vectors over the
`300` retained COSEBIs rows and effective rank `15` in both the raw Euclidean
and covariance-metric geometry audits. This resolves the geometry readiness
blocker without converting the earlier partial-control diagnostic into
endpoint evidence.

The non-degenerate mapping promotion gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_non_degenerate_mapping_promotion_gate_policy_v1.csv
data/derived/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.csv
data/derived/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1_summary.csv
docs/kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.md
scripts/build_kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.py
scripts/validate_kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.py
```

It freezes six required promotion gates before any endpoint scoring: endpoint
grade `F_overlap`, source-preflight readiness, endpoint-family geometry,
a frozen 300-row theory vector, null controls after mapping, and leakage
guards. In the current repository the `F_overlap` endpoint-route gate,
source-preflight mapping state, source-frozen theory-vector gate, null-control
theory replay, endpoint-family geometry audit, and leakage guard pass. The
promotion gate now records `6` passed gates and `0` blockers. Endpoint scoring
remained disabled at this gate until a separate explicitly approved scoring run
was opened under the frozen protocol below.

The endpoint scoring-readiness ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_readiness_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv
docs/kids1000_cosebis_endpoint_scoring_readiness_v1.md
scripts/build_kids1000_cosebis_endpoint_scoring_readiness_v1.py
scripts/validate_kids1000_cosebis_endpoint_scoring_readiness_v1.py
```

It collects the current pre-scoring state in one place. The data-vector
structure, covariance matrix, covariance solve policy, theory-vector
row-interface template, mapping-to-template join contract, F-overlap
resolution/control decision, web/path mapping ledger, and source preflight are
source-side ready. `F_overlap`, caveated `D_path`, null-control `E_web`,
source-side `C_norm`, the source-frozen mapping basis, and a source-frozen
unit-amplitude theory-vector shell are supported. The predeclared null controls
have also been replayed against the source-frozen theory shell as deterministic
control-vector digests, but no null score has been computed. The
endpoint-family geometry audit now passes, so the readiness ledger records `12`
ready components and `0` blockers. This readiness ledger does not itself score;
the separate approved run below is the first endpoint scoring artifact.

The frozen endpoint scoring protocol shell is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_protocol_v1.csv
docs/kids1000_cosebis_endpoint_scoring_protocol_v1.md
scripts/validate_kids1000_cosebis_endpoint_scoring_protocol_v1.py
```

It declares the future COSEBIs scoring grammar
`chi2 = (d - t)^T C^{-1} (d - t)`, the Cholesky solve policy, required
baseline/candidate/null-control comparisons, AIC/control-rank reporting, and
pass-condition shell. The protocol shell itself is not a score. The separate
approved run below is the first artifact that computes endpoint residuals,
chi-square values, AIC values, and null-control scores under that frozen
grammar.

The first approved endpoint scoring run is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_run_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_results.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_residuals.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_grid.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_null_controls.csv
data/derived/kids1000_cosebis_endpoint_scoring_v1_summary.csv
docs/kids1000_cosebis_endpoint_scoring_v1.md
scripts/run_kids1000_cosebis_endpoint_scoring_v1.py
scripts/validate_kids1000_cosebis_endpoint_scoring_v1.py
```

This run is opened only after the readiness ledger records `12` ready
components and `0` blockers. It uses the retained 300-row KiDS COSEBIs `En`
vector only for scoring, not for source selection or post-hoc channel choices.
The source-frozen candidate improves over the zero baseline by
`Delta chi2 = -183.6152665217` and `Delta AIC = -181.6152665217` under the
full covariance Cholesky policy and a nonnegative single-amplitude branch rule.
Against the `1008` predeclared null-control vectors, the candidate ranks
`3/1009` by both chi-square and AIC, with a plus-one null tail fraction of
`0.002973240832507`. This is an endpoint score, not a KiDS validation claim:
two predeclared null controls score better than the candidate, so the
claim-safe reading is a low-tail endpoint signal that requires follow-up
robustness.

The endpoint scoring diagnostics are recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_diagnostics_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_family_summary.csv
data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_top_nulls.csv
data/derived/kids1000_cosebis_endpoint_scoring_diagnostics_v1_summary.csv
scripts/build_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py
scripts/validate_kids1000_cosebis_endpoint_scoring_diagnostics_v1.py
```

The diagnostic result is
`candidate_low_tail_but_not_absolute_winner_tomographic_shuffle_controls_dominate`.
The two controls that beat the candidate both come from the
`tomographic_pair_shuffle` family. No `sky_rotation`, `wrong_channel_activation`,
or `web_path_sign_flip` control beats the candidate. This narrows the next
robustness question to tomographic-pair structure rather than to a generic
wrong-channel or sign-flip failure.

The tomographic-structure robustness run is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_structure_robustness_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_controls.csv
data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_family_summary.csv
data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv
data/derived/kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv
docs/kids1000_cosebis_tomographic_structure_robustness_v1.md
scripts/run_kids1000_cosebis_tomographic_structure_robustness_v1.py
scripts/validate_kids1000_cosebis_tomographic_structure_robustness_v1.py
```

This run compares the same endpoint candidate against stricter tomographic
controls: all `119` non-identity five-bin label permutations and `1000`
auto/cross-preserving pair shuffles. The candidate remains low-tail with rank
`4/1120` and plus-one tail fraction `0.003571428571429`. Three structured
controls beat it, so this is robustness evidence rather than validation. The
remaining caveat is specifically tomographic-structure robustness.

The tomographic-control plausibility audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_control_plausibility_audit_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_control_plausibility_audit_v1.csv
data/derived/kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv
docs/kids1000_cosebis_tomographic_control_plausibility_audit_v1.md
scripts/build_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py
scripts/validate_kids1000_cosebis_tomographic_control_plausibility_audit_v1.py
```

This audit checks whether the better tomographic controls should be interpreted
as physical alternatives. It reads the top `25` tomographic controls and the
source-side redshift kernel inventory, computes mapping-geometry diagnostics,
and computes no new scores. Among the three audited controls that beat the
candidate, two are control-only non-global pair shuffles and one is only a
conditional source-systematic candidate requiring independent photo-z or
tomographic calibration support. No better control is accepted as a physical
alternative in the current source state. Therefore the controls do not refute
the endpoint signal, but they still block validation.

The tomographic holdout/calibration gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_tomographic_holdout_calibration_gate_policy_v1.csv
data/derived/kids1000_cosebis_tomographic_holdout_calibration_gate_v1.csv
data/derived/kids1000_cosebis_tomographic_holdout_calibration_gate_v1_summary.csv
docs/kids1000_cosebis_tomographic_holdout_calibration_gate_v1.md
scripts/build_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py
scripts/validate_kids1000_cosebis_tomographic_holdout_calibration_gate_v1.py
```

This gate is the next validation-facing work order, not a new score. It freezes
the conditions required before any tomographic endpoint replay can be treated as
validation-facing: independent photo-z or tomographic-calibration evidence, a
source-bin or tomographic-pair holdout partition, a rule for promoting a
tomographic control to a source-systematic candidate, a frozen replay protocol,
and a leakage validator. It explicitly forbids observed COSEBIs values,
endpoint residuals, `Delta chi2`, null-control ranks, best-control identity, and
post-score residual shape from source-side selection. Its verdict is
`tomographic_holdout_required_before_endpoint_replay_or_validation`.

The first source-frozen tomographic holdout manifest is recorded in:

```text
data/source_manifest/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_policy_v1.csv
data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_bins_v1.csv
data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_pairs_v1.csv
data/derived/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1_summary.csv
docs/kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.md
scripts/build_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py
scripts/validate_kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1.py
```

This manifest freezes the H2 holdout partition as a deterministic
leave-one-source-bin schedule. In fold `k`, all tomographic pairs touching
source bin `k` are held out, and all other pairs are calibration pairs. The
manifest uses the committed source-native redshift-kernel inventory only; it
does not use observed COSEBIs values, residuals, fit statistics, or null ranks.
It does not complete H1: independent external photo-z/tomographic calibration is
still open, so endpoint replay remains forbidden. Its verdict is
`holdout_partition_frozen_but_independent_photoz_calibration_still_open`.

The source-side photo-z/tomographic calibration evidence ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_photoz_tomographic_calibration_evidence_policy_v1.csv
data/derived/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.csv
data/derived/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1_summary.csv
docs/kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.md
scripts/build_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py
scripts/validate_kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.py
```

This ledger records the H1 state without reopening endpoint scoring. It accepts
the checksum-frozen KiDS lensing product, cached public KiDS DR4 lensing-page
photo-z/SOM-gold documentation markers, and the committed source-native
`NZ_SOURCE` five-bin inventory. It also records the remaining blocker:
independent external photo-z or tomographic calibration is not yet attached.
Endpoint replay and validation claims remain forbidden. Its verdict is
`partial_photoz_tomographic_evidence_available_but_h1_external_calibration_open`.

The external photo-z/tomographic calibration acquisition plan is recorded in:

```text
data/source_manifest/kids1000_cosebis_external_photoz_calibration_acquisition_plan_policy_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.csv
data/derived/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1_summary.csv
docs/kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.md
scripts/build_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py
scripts/validate_kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.py
```

This plan freezes the missing H1 acquisition routes: a source-frozen photo-z
calibration reference or product manifest, a SOM-gold or redshift-distribution
validation manifest, tomographic-bin quality or \(\Delta z\) prior evidence, and
a leakage review for any attached calibration artifacts. No route is attached
yet, so H1 remains open and endpoint replay remains forbidden. Its verdict is
`external_photoz_calibration_acquisition_plan_frozen_h1_still_open`.

The endpoint jackknife/localization robustness audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_jackknife_robustness_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_jackknife_robustness_v1_grid.csv
data/derived/kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv
docs/kids1000_cosebis_endpoint_jackknife_robustness_v1.md
scripts/run_kids1000_cosebis_endpoint_jackknife_robustness_v1.py
scripts/validate_kids1000_cosebis_endpoint_jackknife_robustness_v1.py
```

This post-score audit keeps the source-frozen theory vector fixed and reruns
the same full-covariance, nonnegative single-amplitude scoring rule on
predeclared localization masks. All `20/20` leave-one source-bin and
leave-one tomographic-pair subsets retain negative `Delta chi2` and negative
`Delta AIC`, so the endpoint signal is not carried by a single source bin or
single tomographic pair under this first jackknife. The mode-band result is
more caveated: only `2/3` mode-band subsets improve, and the low-mode-removed
subset has `Delta chi2 = 0`. This is localization robustness, not validation.

The endpoint mode-localization audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_mode_localization_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_mode_localization_v1_grid.csv
data/derived/kids1000_cosebis_endpoint_mode_localization_v1_summary.csv
docs/kids1000_cosebis_endpoint_mode_localization_v1.md
scripts/run_kids1000_cosebis_endpoint_mode_localization_v1.py
scripts/validate_kids1000_cosebis_endpoint_mode_localization_v1.py
```

This follow-up audit localizes the mode-band caveat. It scores predeclared
single-mode, cumulative-low-mode, and low-mode-removal subsets under the same
full-covariance submatrix and nonnegative single-amplitude policy. The best
single mode is `single_mode_1` with `Delta chi2 = -101.5735188246`; the best
cumulative low-mode subset is `cumulative_low_modes_1_to_3` with
`Delta chi2 = -237.1074068478`; and removing modes `1-5` gives
`Delta chi2 = 0`. The claim-safe verdict is that the endpoint signal is
strongly low-mode localized: this is a useful diagnostic and a sharpened
follow-up target, not validation.

The endpoint mode-shape stress audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_mode_shape_stress_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_mode_shape_stress_v1_grid.csv
data/derived/kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv
docs/kids1000_cosebis_endpoint_mode_shape_stress_v1.md
scripts/run_kids1000_cosebis_endpoint_mode_shape_stress_v1.py
scripts/validate_kids1000_cosebis_endpoint_mode_shape_stress_v1.py
```

This stress test keeps the same source-frozen `W_path` mapping and endpoint
scoring rule, but replaces the source-independent mode carrier. The predeclared
candidate `n^-0.5` carrier remains best in this small stress family with
`Delta chi2 = -183.6152665217`; a flat carrier still improves with
`Delta chi2 = -136.5504934506`; and high-`n` weighting removes the signal
with `Delta chi2 = 0`. Thus the low-mode result is carrier-sensitive, but the
signal is not produced solely by the exact `n^-0.5` carrier choice. This is a
mode-shape sensitivity diagnostic, not validation.

The endpoint scoring synthesis ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_endpoint_scoring_synthesis_ledger_policy_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.csv
data/derived/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1_summary.csv
docs/kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.md
scripts/build_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py
scripts/validate_kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.py
```

This ledger does not compute a new score. It aggregates the approved endpoint
score, null-control diagnostics, tomographic-structure robustness, jackknife,
mode-localization, mode-shape stress, and physical-promotion blocker ledger into
one claim-safe synthesis. The current verdict is
`endpoint_signal_low_tail_caveated_by_tomographic_controls_and_physical_promotion_blockers`.
In plain terms, the KiDS COSEBIs branch has a low-tail diagnostic endpoint
signal, but it is not an absolute control winner, the tomographic-structure
caveat remains active. The better tomographic controls are not accepted as
physical alternatives without independent photo-z/tomographic calibration
support, and physical promotion is still blocked by the five requirements listed
below.

The low-mode carrier source-grounding ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_low_mode_carrier_source_grounding_policy_v1.csv
data/derived/kids1000_cosebis_low_mode_carrier_source_grounding_v1.csv
data/derived/kids1000_cosebis_low_mode_carrier_source_grounding_v1_summary.csv
docs/kids1000_cosebis_low_mode_carrier_source_grounding_v1.md
scripts/build_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py
scripts/validate_kids1000_cosebis_low_mode_carrier_source_grounding_v1.py
```

This ledger answers the immediate reviewer question raised by the low-mode
diagnostics. It records that the `n^-0.5` carrier is source independent,
predeclared, unit-mean normalized, and not selected from KiDS data-vector values.
It is consistent with a broad coherent path/readout prior and with the post-score
diagnostics, but it is not a first-principles Tau Core lensing kernel derivation.
The verdict is
`partial_protocol_grounding_with_open_first_principles_derivation_blocker`.

The low-mode kernel-envelope derivation artifact is recorded in:

```text
data/source_manifest/kids1000_cosebis_low_mode_kernel_envelope_derivation_policy_v1.csv
data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.csv
data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_mode_weights.csv
data/derived/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_summary.csv
docs/kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.md
scripts/build_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py
scripts/validate_kids1000_cosebis_low_mode_kernel_envelope_derivation_v1.py
```

This artifact narrows the open blocker. Under the explicit source-side prior
that a smooth path/readout residual has approximately constant power per
logarithmic COSEBIs mode band, the discrete mode power scales as `P_n ~ 1/n`
and the coherent amplitude envelope scales as `sqrt(P_n) ~ n^-0.5`. The
finite retained mode domain then fixes the unit-mean normalization over
`n=1..20`. This is a conditional envelope derivation, not a covariant KiDS
lensing/path kernel theorem; the remaining blocker is the survey-native or
covariant derivation of when the log-band-neutral prior applies.

The log-band prior eligibility gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_log_band_prior_eligibility_gate_policy_v1.csv
data/derived/kids1000_cosebis_log_band_prior_eligibility_gate_v1.csv
data/derived/kids1000_cosebis_log_band_prior_eligibility_gate_v1_summary.csv
docs/kids1000_cosebis_log_band_prior_eligibility_gate_v1.md
scripts/build_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py
scripts/validate_kids1000_cosebis_log_band_prior_eligibility_gate_v1.py
```

This gate states when the conditional log-band prior is allowed as a protocol
object. The current COSEBIs route passes ordered-mode, no-posthoc-mode-cut,
source-side path-mapping, and no-high-frequency-only guardrails. It still leaves
one unproven smoothness assumption and one open full-kernel blocker. The verdict
is `protocol_eligible_for_conditional_envelope_but_not_full_kernel_validated`.

The log-band prior deterministic mock-sanity suite is recorded in:

```text
data/source_manifest/kids1000_cosebis_log_band_prior_mock_sanity_policy_v1.csv
data/derived/kids1000_cosebis_log_band_prior_mock_sanity_v1_grid.csv
data/derived/kids1000_cosebis_log_band_prior_mock_sanity_v1_summary.csv
docs/kids1000_cosebis_log_band_prior_mock_sanity_v1.md
scripts/run_kids1000_cosebis_log_band_prior_mock_sanity_v1.py
scripts/validate_kids1000_cosebis_log_band_prior_mock_sanity_v1.py
```

This is a deterministic template-recovery sanity check, not physical mock
validation. It tests four synthetic truth families over the retained `15 x 20`
COSEBIs row structure: low log-band `n^-0.5`, flat coherent, high-mode `n`,
and oscillatory alternating. Each truth recovers its matching template. The
purpose is only to show that the protocol does not automatically classify every
deterministic pattern as low-mode. The suite uses no KiDS data-vector values, no
fit statistics, no random noise, and makes no endpoint-validation claim. Its
verdict is
`deterministic_template_recovery_pass_not_physical_mock_validation`.

The survey-native path-kernel derivation gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_survey_native_path_kernel_derivation_gate_policy_v1.csv
data/derived/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.csv
data/derived/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1_summary.csv
docs/kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.md
scripts/build_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py
scripts/validate_kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.py
```

This gate separates route support from full kernel derivation. The current
source route has a source-frozen mapping basis, a caveated full-route mask-load
path proxy, a source-side path-weight factorization rule, a source-frozen
theory-vector shell, and the deterministic template-recovery guardrail. These
are enough to make the route support concrete, but not enough to claim a
survey-native Tau Core lensing kernel. Three blockers remain explicit: a
survey-native operator from path observables to COSEBIs mode response, a
derivation of the log-band prior from that response spectrum, and a covariant or
survey-native lensing/path limit. The verdict is
`survey_native_path_route_available_but_mode_response_and_covariant_kernel_derivation_blocked`.

The COSEBIs mode-response operator specification is recorded in:

```text
data/source_manifest/kids1000_cosebis_mode_response_operator_spec_policy_v1.csv
data/derived/kids1000_cosebis_mode_response_operator_spec_v1.csv
data/derived/kids1000_cosebis_mode_response_operator_spec_v1_summary.csv
docs/kids1000_cosebis_mode_response_operator_spec_v1.md
scripts/build_kids1000_cosebis_mode_response_operator_spec_v1.py
scripts/validate_kids1000_cosebis_mode_response_operator_spec_v1.py
```

This artifact freezes what a future survey-native mode-response operator must
satisfy before the low-mode envelope can be promoted beyond a conditional
protocol carrier. It defines the path-observable domain, retained COSEBIs-row
codomain, linearity-before-amplitude rule, pair/redshift/path separation,
no-feedback constraint, gauge/mask null-safety requirement, and standard-lensing
null limit. It does not derive the operator. The verdict is
`operator_requirements_frozen_but_survey_native_mode_response_not_derived`.

The COSEBIs mode-response spectrum attempt is recorded in:

```text
data/source_manifest/kids1000_cosebis_mode_response_spectrum_attempt_policy_v1.csv
data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1.csv
data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1_spectra.csv
data/derived/kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv
docs/kids1000_cosebis_mode_response_spectrum_attempt_v1.md
scripts/build_kids1000_cosebis_mode_response_spectrum_attempt_v1.py
scripts/validate_kids1000_cosebis_mode_response_spectrum_attempt_v1.py
```

This artifact keeps the spectrum-level argument conditional. Under the explicit
smooth coherent path/readout prior, constant power per logarithmic COSEBIs mode
band gives `P_n ~ 1/n` and coherent amplitude `M_n ~ n^-0.5`. The flat spectrum
is preserved as a boundary control, while high-mode and oscillatory spectra are
rejected only under that smooth-path prior. The mode-response operator and
operator-level gauge/null safety remain open blockers. The verdict is
`conditional_source_spectrum_attempt_preserves_operator_and_null_safety_blockers`.

The COSEBIs operator null-safety gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_operator_null_safety_gate_policy_v1.csv
data/derived/kids1000_cosebis_operator_null_safety_gate_v1.csv
data/derived/kids1000_cosebis_operator_null_safety_gate_v1_summary.csv
docs/kids1000_cosebis_operator_null_safety_gate_v1.md
scripts/build_kids1000_cosebis_operator_null_safety_gate_v1.py
scripts/validate_kids1000_cosebis_operator_null_safety_gate_v1.py
```

This artifact audits the remaining null-safety blocker at operator level. It
records that source-frozen null controls exist and have been replayed without
endpoint scores, that the domain/codomain route exists with a caveated
path/mask-load proxy, and that a uniform web route is accepted only as a null
control. It does not prove operator-level null safety. Three blockers remain:
pure-mask response, gauge/quotient descent, and coupling the conditional mode
spectrum to null transforms through one source-native operator. The verdict is
`null_controls_exist_but_operator_level_null_safety_remains_blocked`.

The COSEBIs pure-mask response gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_pure_mask_response_gate_policy_v1.csv
data/derived/kids1000_cosebis_pure_mask_response_gate_v1.csv
data/derived/kids1000_cosebis_pure_mask_response_gate_v1_summary.csv
data/derived/kids1000_cosebis_pure_mask_response_tile_basis_v1.csv
data/derived/kids1000_cosebis_pure_mask_response_domain_basis_v1.csv
docs/kids1000_cosebis_pure_mask_response_gate_v1.md
scripts/build_kids1000_cosebis_pure_mask_response_gate_v1.py
scripts/validate_kids1000_cosebis_pure_mask_response_gate_v1.py
```

This artifact narrows the pure-mask branch of the null-safety blocker. It
constructs a centered, unit-RMS, source-only pure-mask perturbation basis from
the full-route `F_overlap` and `D_path` mask observables, and lifts that basis
to the `58,800` target-by-route-tile domain. The centered basis has rank `2`.
It still does not construct a mapping vector, theory vector, prediction,
residual, fit statistic, or endpoint score. Quotient triviality and coupling to
the COSEBIs mode response remain open blockers. The verdict is
`pure_mask_basis_exists_but_quotient_triviality_and_mode_coupling_remain_blocked`.

The COSEBIs mask-mode leakage audit is recorded in:

```text
data/source_manifest/kids1000_cosebis_mask_mode_leakage_audit_policy_v1.csv
data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1.csv
data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1_grid.csv
data/derived/kids1000_cosebis_mask_mode_leakage_audit_v1_summary.csv
docs/kids1000_cosebis_mask_mode_leakage_audit_v1.md
scripts/build_kids1000_cosebis_mask_mode_leakage_audit_v1.py
scripts/validate_kids1000_cosebis_mask_mode_leakage_audit_v1.py
```

This artifact audits a source-side leakage risk. The centered pure-mask basis
collapses to zero under uniform tile averaging, with
`max_uniform_collapse_norm` at numerical roundoff level. However, if a future
survey-native operator couples non-uniform mask amplitudes into a mode
envelope, mask-only leakage into the low-mode carrier is not yet ruled out.
The verdict is
`uniform_mask_collapse_is_null_but_nonuniform_operator_leakage_remains_open`.

The COSEBIs operator-leakage theorem requirements gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_operator_leakage_theorem_requirements_policy_v1.csv
data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1.csv
data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv
docs/kids1000_cosebis_operator_leakage_theorem_requirements_v1.md
scripts/build_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py
scripts/validate_kids1000_cosebis_operator_leakage_theorem_requirements_v1.py
```

This artifact converts the mask-mode leakage audit into a frozen requirement
list for a future survey-native operator theorem. It records the uniform
tile-average null limit as a source-side limit, keeps the non-uniform leakage
risk open, freezes the pure-mask rejection/control-subspace requirement and the
mode-spectrum/null-coupling requirement, and leaves two explicit blockers:
operator leakage theorem and gauge/quotient descent. The verdict is
`requirements_frozen_for_operator_leakage_theorem_but_proof_remains_open`.

The COSEBIs gauge/quotient descent gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_gauge_quotient_descent_gate_policy_v1.csv
data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1.csv
data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv
docs/kids1000_cosebis_gauge_quotient_descent_gate_v1.md
scripts/build_kids1000_cosebis_gauge_quotient_descent_gate_v1.py
scripts/validate_kids1000_cosebis_gauge_quotient_descent_gate_v1.py
```

This artifact freezes the representation-invariance requirements for a future
survey-native path/readout operator. It records allowed representative changes,
the uniform mask-offset null limit, normalization and tile-relabeling
invariance requirements, and pure-mask control compatibility. It does not prove
gauge/quotient descent and does not construct the missing survey-native
operator. The verdict is
`gauge_quotient_descent_requirements_frozen_but_theorem_remains_open`.

The COSEBIs survey-native operator construction attempt is recorded in:

```text
data/source_manifest/kids1000_cosebis_survey_native_operator_construction_attempt_policy_v1.csv
data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1.csv
data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_ledger.csv
data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv
docs/kids1000_cosebis_survey_native_operator_construction_attempt_v1.md
scripts/build_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py
scripts/validate_kids1000_cosebis_survey_native_operator_construction_attempt_v1.py
```

This artifact writes the first explicit source-side factorized operator
skeleton for the KiDS COSEBIs branch, \(K_i=M_iS_n\), using the frozen mapping
component and the conditional log-band mode-response weight. It is a
unit-amplitude source-side kernel, not a survey-native operator theorem and not
an endpoint prediction. Mask-leakage theorem, gauge/quotient descent, and
physical operator-unit derivation remain open. The verdict is
`factorized_source_side_operator_skeleton_exists_but_operator_theorem_remains_open`.

The COSEBIs physical operator-units gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_physical_operator_units_gate_policy_v1.csv
data/derived/kids1000_cosebis_physical_operator_units_gate_v1.csv
data/derived/kids1000_cosebis_physical_operator_units_gate_v1_summary.csv
docs/kids1000_cosebis_physical_operator_units_gate_v1.md
scripts/build_kids1000_cosebis_physical_operator_units_gate_v1.py
scripts/validate_kids1000_cosebis_physical_operator_units_gate_v1.py
```

This artifact records the unit and normalization blockers left by the
operator-skeleton attempt. The current \(K_i=M_iS_n\) kernel is identified as a
dimensionless unit-amplitude source-side object. The gate freezes the need for
physical response units, a source-side amplitude map, and a standard-lensing
null normalization before any physical COSEBIs prediction can be claimed. The
verdict is
`dimensionless_operator_kernel_identified_but_physical_units_and_amplitude_remain_open`.

The COSEBIs source-side amplitude-map attempt is recorded in:

```text
data/source_manifest/kids1000_cosebis_source_side_amplitude_map_attempt_policy_v1.csv
data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1.csv
data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1_ledger.csv
data/derived/kids1000_cosebis_source_side_amplitude_map_attempt_v1_summary.csv
docs/kids1000_cosebis_source_side_amplitude_map_attempt_v1.md
scripts/build_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py
scripts/validate_kids1000_cosebis_source_side_amplitude_map_attempt_v1.py
```

This artifact freezes only the internal dimensionless source-normalized
amplitude map \(A_{\rm src}=1\) induced by the unit-mean `C_norm` rule and the
unit-mean operator skeleton. It removes an arbitrary source-side scale from the
current skeleton, but it does not derive physical COSEBIs response units, does
not calibrate an endpoint amplitude, and does not prove the standard-lensing
null amplitude. The verdict is
`dimensionless_source_amplitude_map_exists_but_physical_amplitude_remains_open`.

The COSEBIs physical-amplitude requirements gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_physical_amplitude_requirements_gate_policy_v1.csv
data/derived/kids1000_cosebis_physical_amplitude_requirements_gate_v1.csv
data/derived/kids1000_cosebis_physical_amplitude_requirements_gate_v1_summary.csv
docs/kids1000_cosebis_physical_amplitude_requirements_gate_v1.md
scripts/build_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py
scripts/validate_kids1000_cosebis_physical_amplitude_requirements_gate_v1.py
```

This gate states what remains after \(A_{\rm src}=1\): a physical response
amplitude \(A_{\rm phys}\) would still need the missing COSEBIs response-unit
normalization and the standard-lensing/no-Tau-source null amplitude theorem.
The covariance metric is preserved as a future scoring metric but is explicitly
not used as an amplitude derivation. The verdict is
`dimensionless_source_amplitude_available_but_physical_response_amplitude_remains_open`.

The COSEBIs response-unit normalization requirements gate is recorded in:

```text
data/source_manifest/kids1000_cosebis_response_unit_normalization_requirements_gate_policy_v1.csv
data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1.csv
data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv
docs/kids1000_cosebis_response_unit_normalization_requirements_gate_v1.md
scripts/build_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py
scripts/validate_kids1000_cosebis_response_unit_normalization_requirements_gate_v1.py
```

This gate freezes the requirements for mapping the dimensionless source kernel
and \(A_{\rm src}=1\) into COSEBIs response units. The 300-row COSEBIs domain,
dimensionless kernel/source amplitude, and covariance metric are available, but
the response-unit map itself remains open and must be compatible with the
standard-lensing/no-\(\tau\)-source null limit. The verdict is
`cosebis_response_unit_requirements_frozen_but_normalization_remains_open`.

The COSEBIs standard-lensing null-amplitude theorem-requirements gate is
recorded in:

```text
data/source_manifest/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_policy_v1.csv
data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.csv
data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv
docs/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.md
scripts/build_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py
scripts/validate_kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.py
```

This gate freezes the theorem requirements for the no-\(\tau\)-source limit:
source-replayed null controls are available only as controls, the zero-Tau
amplitude statement is specified but not derived, and operator null safety,
gauge/quotient descent, and non-uniform leakage control remain open blockers.
The verdict is
`standard_lensing_null_amplitude_requirements_frozen_but_theorem_remains_open`.

The COSEBIs physical-promotion blocker ledger is recorded in:

```text
data/source_manifest/kids1000_cosebis_physical_promotion_blocker_ledger_policy_v1.csv
data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1.csv
data/derived/kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv
docs/kids1000_cosebis_physical_promotion_blocker_ledger_v1.md
scripts/build_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py
scripts/validate_kids1000_cosebis_physical_promotion_blocker_ledger_v1.py
```

This ledger separates diagnostic endpoint readiness from physical promotion.
The diagnostic endpoint pipeline is ready, but physical promotion remains
blocked by five open requirements: survey-native operator theorem, operator
leakage theorem, gauge/quotient descent, response-unit normalization, and
standard-lensing/no-\(\tau\)-source null-amplitude theorem. The verdict is
`diagnostic_endpoint_ready_but_physical_promotion_blocked_by_five_open_requirements`.

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
skeleton are available; the path-weight construction rule is source-side
computable; the three-mask observable shell is preserved as a control; the
full-route `D_path` mask-load proxy is available but caveated; the positive
web-environment catalogue remains absent and is represented only by a null-web
control; and source-frozen null-control theory replay is available. It contains
no endpoint predictions, residuals, fit statistics, or scores.

The first COSEBIs null-control readiness policy is recorded in:

```text
data/source_manifest/kids1000_cosebis_null_control_policy_v1.csv
data/derived/kids1000_cosebis_null_control_readiness_v1.csv
data/derived/kids1000_cosebis_null_control_readiness_v1_summary.csv
docs/kids1000_cosebis_null_control_policy_v1.md
scripts/build_kids1000_cosebis_null_control_readiness_v1.py
scripts/validate_kids1000_cosebis_null_control_readiness_v1.py
```

It declares four null-control families: sky rotation, tomographic-pair shuffle,
wrong-channel activation, and web/path sign flip. In this release these controls
are replayed only as source-frozen theory-vector digests, not as null scores.

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

The first COSEBIs null-control theory replay is recorded in:

```text
data/source_manifest/kids1000_cosebis_null_control_theory_replay_policy_v1.csv
data/derived/kids1000_cosebis_null_control_theory_replay_v1.csv
data/derived/kids1000_cosebis_null_control_theory_replay_v1_summary.csv
docs/kids1000_cosebis_null_control_theory_replay_v1.md
scripts/build_kids1000_cosebis_null_control_theory_replay_v1.py
scripts/validate_kids1000_cosebis_null_control_theory_replay_v1.py
```

It applies the predeclared control transformations to the source-frozen
unit-amplitude theory-vector shell and stores compact vector digests and source
statistics for `1008` controls. It does not compare those controls to the KiDS
data vector and does not compute scores.

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
figures/fig_kids1000_cosebis_mode_localization.pdf
paper10_submission_source/figures/fig_kids1000_cosebis_mode_localization.pdf
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

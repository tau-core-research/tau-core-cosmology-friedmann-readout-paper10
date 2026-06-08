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

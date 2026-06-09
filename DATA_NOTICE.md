# Data Notice

This repository is a protocol scaffold for Paper 10. It does not redistribute
raw survey data, CMB maps, MCMC chains, FITS products, void catalogues, weak
lensing catalogues, or proprietary survey products.

The first release contains only compact protocol artifacts and smoke-test
tables. Future empirical versions should keep raw data acquisition separate and
document any online data dependencies explicitly.

The current source registry is a manifest, not a data release:

```text
data/source_manifest/paper10_source_freeze_manifest.csv
```

Rows marked `SOURCE_SELECTED_NOT_FETCHED` identify candidate public source
families that still need acquisition, checksums, and frozen transformation
rules. Rows marked `BLOCKED_SOURCE_SELECTION` would identify scientifically
required blocks for which no accepted public source product has yet been
selected. In the current manifest, the first source-selection audit has selected
candidate public source families for all required blocks, but none of them are
yet `FETCHED_FROZEN`.

Planned public data families include:

- DESI BAO / cosmology products for distance constraints.
- Public supernova compilations such as Pantheon+ or DES-SN products where
  license and redistribution terms allow derived summaries.
- Cosmic chronometer `H(z)` compilations with citation and provenance.
- Planck / NASA LAMBDA CMB products for early-universe safety and CMB-lensing
  controls.
- Public void catalogues and cosmic-web / large-scale-structure classifiers.
- Public growth and lensing summaries such as RSD `f sigma_8`, weak-lensing,
  CMB-lensing, and cluster-lensing products.

No result in this repository should be read as a measurement claim until those
source blocks are acquired, frozen, and audited under the protocol in the
manuscript.

Endpoint scoring is not allowed until the required source blocks are either
`FETCHED_FROZEN` or explicitly excluded by a predeclared pilot-scope rule.

The committed provenance cache contains only official landing/source pages,
not raw survey products. It is used to verify source routes and URLs, not to
compute cosmological observables.

The product-freeze plan also contains no raw survey products. It records product
roles and unresolved acquisition policies. Every current product row has
`endpoint_allowed=false`.

The void/web source-native freeze plan similarly contains no raw void or
cosmic-web catalogue. It records the preferred candidate routes for replacing
the proxy `W_void` and `W_web` bases with a future VAST/SDSS DR7 void product
and an SDSS DR17 MCPM cosmic-web product. Both rows remain selected-not-fetched
and endpoint disabled.

The source-native void/web frozen-products manifest does include four compact
public products under `data/raw/`: a VAST/SDSS DR7 Planck2018 maximal void
table, its NSA mask, the SDSS DR17 MCPM SlimeMold galaxy catalogue, and the
provider sha1sum file. These files are checksum-locked source products, not
endpoint scoring inputs. The derived inventory records only source-side row
counts and hashes; it contains no residuals, no fitted parameters, and no
endpoint scores.

The source-native void/web design matrix maps those products into fixed
`W_void` and `W_web` basis columns without using endpoint residuals. The
subsequent full-covariance pilot is explicitly labelled non-validation and
should not be read as empirical evidence for a cosmological signal.

The growth-side pilot uses six SDSS final BAO/RSD `f sigma8(z)` summary values
with diagonal published errors only. It does not include the full official
compressed-parameter covariance and is therefore not an endpoint growth
likelihood.

The SDSS multi-tracer BAO/RSD pilot freezes the official public DR16 LRG+ELG
compressed BAO/RSD products and their covariance matrix under `data/raw/`.
The derived six-component design matrix and pilot summary use the official
6x6 compressed-parameter covariance, but the run remains
`SDSS_MULTITRACER_BAO_RSD_FULL_COV_PILOT_NOT_VALIDATION`. It is a covariance
grammar test and seminegative control, not endpoint validation and not evidence
for a new cosmological model.

The CMB-safety low-redshift support check contains no CMB maps, no Planck
likelihood, and no CMB residuals. It only verifies that the currently active
late-time void/web basis functions are zero at a conservative high-redshift
safety floor and at a recombination-scale proxy. Passing this check is a
known-limit sanity condition, not CMB evidence.

The KiDS-1000 lensing route check contains only HTTP HEAD metadata for a public
cosmic-shear tarball. It does not fetch, store, or redistribute KiDS lensing
catalogues, data vectors, covariance matrices, posterior chains, or likelihood
files. It is a source-route/provenance gate only.

The KiDS-1000 lensing product manifest does include the public cosmic-shear
tarball under `data/raw/weak_lensing/kids1000/`. The derived inventory records
tarball member names, sizes, and the predeclared COSEBIs member route. It does
not extract a lensing likelihood, does not score a model, and does not contain
residuals or fitted Tau parameters.

The COSEBIs HDU inventory reads only FITS metadata and array/table dimensions
from the selected KiDS product. It records the covariance/data-vector/redshift
distribution HDU roles and checks covariance positive definiteness, but it does
not compute lensing predictions, residuals, likelihood values, or posterior
weights.

The COSEBIs tomographic/mode inventory reads only the selected `En` data-vector
table to record source-side structure: five source bins, 15 upper-triangular
tomographic bin pairs, 20 modes per pair, and 300 rows. It does not define a
theory vector, covariance inverse, mode cut, residual, likelihood, posterior
weight, or fitted Tau parameter.

The COSEBIs covariance-readiness inventory records only numerical diagnostics
of the selected `COVMAT` block: shape, symmetry, diagonal positivity, eigenvalue
range, condition number, and Cholesky readiness. It does not store an inverse
covariance and does not compute lensing predictions, residuals, likelihood
values, posterior weights, or fitted Tau parameters.

The COSEBIs mask/mode-cut inventory retains all 300 source rows and all modes
1..20 for all 15 tomographic pairs. It is a leakage-prevention artifact: no row,
tomographic pair, or mode is removed using endpoint residuals, fit statistics,
posterior chains, or model-performance information.

The COSEBIs tomographic-weight inventory assigns unit source-retention weights
to every tomographic pair. These are not likelihood weights and not fitted
amplitudes; they only document that no pair is preferred using residuals,
posterior chains, fit statistics, or endpoint behavior.

The COSEBIs covariance-subselection inventory retains the full 300 x 300
covariance block and records the 20-row pair blocks. It does not save an inverse
covariance, does not select a likelihood, and does not remove covariance rows or
columns using endpoint behavior.

The COSEBIs covariance-inversion readiness inventory freezes only the future
numerical solve policy: Cholesky solve against the full covariance after a
theory vector is frozen. It does not execute the solve, does not store an
inverse covariance, and does not compute predictions, residuals, or likelihoods.

The COSEBIs theory-vector readiness inventory declares only the future
requirement for a 300-row theory vector. It does not compute that vector and
does not use KiDS data-vector values, posterior chains, residuals, or
fit-improvement information to choose a lensing formula.
The associated theory-vector template freezes only the 300-row tomographic
pair/mode interface and leaves all theory-value and channel-contribution fields
empty. It contains no prediction, residual, likelihood value, fit statistic, or
endpoint score.
The mapping-to-template join contract freezes only the future row-level join
grammar between a source-frozen web/path mapping and that 300-row template. It
leaves all source-frozen basis, activation, provenance, mapping, and theory
fields empty and contains no prediction, residual, likelihood value, fit
statistic, or endpoint score.

The COSEBIs web/path mapping readiness inventory declares only the future
source-side mapping requirements for the active web/path channels. It does not
compute a mapping vector or theory vector and does not use KiDS data-vector
values, posterior chains, residuals, fit-improvement information, or post-hoc
sky-direction choices.

The COSEBIs redshift-kernel inventory reads only the selected `NZ_SOURCE` table
from the KiDS FITS product. It records per-source-bin redshift-distribution
area, mean redshift, and support intervals. It contains no COSEBIs predictions,
residuals, likelihood values, posterior-chain use, fit statistics, or data-vector
value use.

The COSEBIs path mask/depth gap inventory scans only the selected KiDS tarball
membership and release note. It records that the present package does not
contain an accepted standalone footprint, path mask, depth map, random catalogue,
or equivalent path-load product. The inventory contains no path mapping vector,
theory vector, predictions, residuals, likelihood values, posterior-chain use,
fit statistics, or data-vector-value use.

The KiDS DR4 path-mask route-script inventory freezes only the official wget
scripts that list external mask FITS products. The preferred DR4.1 9-band route
script lists 196 mask products, but those mask FITS products are not downloaded
or redistributed here. The inventory contains no parsed mask map, no path
mapping vector, no theory vector, no predictions, no residuals, no likelihood
values, and no data-vector-value use.

The KiDS DR4 path-mask route-tile inventory parses the preferred DR4.1 9-band
route URLs into 196 filename-derived tile coordinates. It does not download the
196 mask FITS products, parse pixels, infer a footprint polygon, build a path
mapping vector, or use endpoint residuals.

The KiDS DR4 path-mask HEAD sample checks only HTTP metadata for the first,
middle, and last products in the preferred route script. It records HTTP status,
content type, and content length. It does not download mask FITS products,
redistribute mask maps, parse pixels, compute a path mapping vector, or use
endpoint residuals.

The KiDS DR4 path-mask subset inventory downloads only the three predeclared
first/middle/last mask FITS products from that HEAD sample. It records hashes,
FITS image shapes, and basic finite/nonzero pixel summaries. It does not compute
a path mapping vector, does not connect mask pixels to COSEBIs rows, does not
build a theory vector, and does not use KiDS data-vector values or endpoint
residuals.

The KiDS DR4 path-mask observable shell uses only that three-product subset
inventory. It records filename-derived tile coordinates and a centered
zero-fraction shell across the three masks. The mask values are not interpreted
as a physical path weight in this gate. The shell contains no COSEBIs-row
mapping vector, no theory vector, no predictions, no residuals, no likelihood
values, and no endpoint score.

The COSEBIs path-mapping design skeleton combines the COSEBIs row structure,
tomographic redshift-kernel summaries, and preferred-route tile span into a
300-row source-side layout. It does not compute tile weights, path weights,
mapping-vector elements, theory-vector elements, predictions, residuals,
likelihood values, or endpoint scores.

The COSEBIs path-mapping domain skeleton expands that layout to the full
300-by-196 target-row by preferred-route-tile domain. It records no footprint
overlap, tile weight, path weight, web-environment label, mapping-vector element,
theory-vector element, prediction, residual, likelihood value, or endpoint
score.

The COSEBIs path-weight construction-rule ledger declares only a future
factorization of target-tile path weights. It records available, partial,
missing, declared-not-computed, and declared-not-executed factors. It does not
compute any numeric factor value, tile weight, path mapping, theory vector,
prediction, residual, likelihood value, or endpoint score.

The COSEBIs path-factor acquisition plan records only source-side requirements
for making that weight rule computable. It fetches no new products and computes
no factor values. It identifies footprint overlap, full path/depth support,
web/environment support, and later normalization as the current direct blockers
for numeric path weights.

The COSEBIs source-product route candidate manifest declares which source
routes can later be used to resolve those blockers. It records locked existing
ingredients, blocker-resolution candidates, and controls/deferred routes, but
fetches no products and computes no factor values, path mapping, theory vector,
prediction, residual, likelihood value, or endpoint score.

The COSEBIs blocker-resolution order policy freezes the source-side order in
which blockers may be resolved. Footprint overlap must be resolved first,
followed by path/depth support, web/environment support, source-side
normalization, mapping-vector construction, and null controls. This order gate
also fetches no products and computes no factor values, mapping vector, theory
vector, prediction, residual, likelihood value, or endpoint score.

The `F_overlap` rule shell declares the accepted future source-side schema for
the first unresolved KiDS path blocker. It uses the existing 58,800-row
COSEBIs target-row by route-tile domain, but computes no overlap support flags
or fractions. It accepts only source-frozen official footprint geometry or
source-native full-mask overlap derivations, and it keeps mapping and endpoint
scoring disabled.

The `F_overlap` source-availability audit records the current negative/partial
state: the route script lists 196 preferred tiles and the three-mask subset is
present, but neither an official footprint geometry product nor a full 196-mask
source-native product set is accepted. Thus the overlap rule is not ready and
mapping remains disabled.

The `F_overlap` full-mask acquisition manifest expands the preferred route into
196 expected mask products without fetching them. It records that three are
locally present and 193 are missing, so the full source-native overlap route is
still not accepted.

The `F_overlap` full-mask batch plan splits the 193 missing products into ten
future acquisition batches and assigns future large FITS files to an ignored
cache directory. No products are fetched by this gate; it only records the
source-side acquisition plan.

The `F_overlap` batch dry-run gate inspects the first planned acquisition batch
without downloading any FITS products. It records the 20 intended product URLs
and cache paths for batch 0, but keeps `external_products_fetched=false`,
`overlap_rule_computed=false`, `path_mapping_computed=false`, and
`endpoint_scoring_allowed=false`. The same script has a manual `--execute`
mode for future source acquisition, but that mode is not called by
`scripts/reproduce.py` and does not by itself create an accepted overlap rule,
mapping vector, theory vector, or endpoint score. Manual execution logs are
written under ignored `data/local/` paths so that a fetch cannot overwrite the
committed dry-run artifacts.

The batch-promotion review checklist is also committed, but it is a negative
source-side gate in this release. It records that no fetched-batch review
artifact or checksum manifest has been promoted from `data/local/`, so
`promotion_ready=false`. It does not inspect machine-local execution logs and
does not compute overlap, mapping, theory-vector, prediction, residual, or
endpoint-score quantities.
The checklist records the filled-review validator as available, but that row is
only a future-review readiness item; it is not a fetched-batch artifact and does
not change the negative promotion status.

The execution-review schema gate freezes the columns that a future committed
fetched-batch review artifact must contain. It is a schema declaration only:
there is still no fetched-batch review artifact in this release, and the schema
does not fetch products, compute overlap, or enable scoring.

The execution-review template gate materializes the default batch-0 rows in
that schema, but it is still not an execution log. Network fields, checksums,
timestamps, and reviewer fields are empty or pending, and all endpoint and
forbidden-input flags remain false.

The filled execution-review validator is a schema and leakage-boundary utility
only. In template mode it checks the committed empty batch-0 template; in
filled mode it can later check a manually completed review artifact against the
frozen schema and dry-run batch identities. It does not acquire data, promote a
batch, compute overlap, construct a mapping or theory vector, or enable
endpoint scoring.
The F-overlap resolution decision gate records that no endpoint-grade overlap
route is currently accepted. The three source-frozen mask products are accepted
only as a caveated partial path-mask control; they are not promoted to a
population endpoint overlap rule. The decision computes no overlap fraction,
path mapping, theory vector, prediction, residual, likelihood value, fit
statistic, or endpoint score.
The partial-control scoring protocol freezes only a future diagnostic grammar
for this caveated three-mask control. It does not run scoring and it does not
emit result, residual, grid, null-control, summary, likelihood, AIC, endpoint,
or validation artifacts.
The partial-control mapping shell materializes only the `300 x 3 = 900`
source-side support table between COSEBIs rows and the three caveated mask
controls. It carries mask-shell observables and row identities, but no mapping
value, theory vector, prediction, residual, likelihood, fit statistic, endpoint
score, or validation artifact.
The partial-control mapping-values artifact then applies only a frozen,
source-side diagnostic rule to that shell:
`source_mask_shell_value * normalized_pair_mean_z_weight * mode^{-1/2}`.
The redshift factor comes from the KiDS `NZ_SOURCE` mean-redshift inventory and
the mode factor from the COSEBIs row index. This artifact is not an endpoint
mapping vector, not a theory vector, and not a score; it contains no KiDS
data-vector values, posterior chains, residuals, likelihood values, fit
statistics, AIC values, endpoint scores, or validation claims.
The partial-control design matrix reduces the `900` mapping values to six
deterministic `300`-row diagnostic branches: a zero baseline, the three
individual mask-sample branches, the positive-mask mean, and a sign-flipped
positive-mask control. It is a scoring-facing support object only. It contains
no endpoint theory vector, predictions, residuals, likelihood values, fit
statistics, AIC values, endpoint scores, or validation claims.
The partial-control diagnostic scoring artifact is the first caveated score
using this branch matrix. It uses the KiDS COSEBIs `En` data vector and full
`COVMAT` covariance for scoring only, with one nonnegative amplitude per
predeclared branch. It does not use the KiDS data vector for source, branch,
mask, or weight selection. Because the positive mask branches are
amplitude-degenerate in this simplified control, the score is a diagnostic
smoke test only, not endpoint validation or a population lensing claim.

The endpoint scoring-readiness ledger is a no-go summary, not a score. It
records that the COSEBIs data-vector structure, covariance matrix, covariance
solve policy, theory-vector row-interface template, and mapping-to-template
join contract are source-side ready, and the F-overlap resolution/control
decision is recorded, while the theory vector, web/path mapping, source
preflight, blocker-resolution order, and null controls still block
scoring. It contains no predictions,
residuals, fit statistics, or endpoint scores.

The endpoint scoring protocol shell freezes only the future scoring grammar:
the chi-square form, Cholesky solve policy, required candidate/control
comparisons, AIC/control-rank outputs, and pass-condition shell. It is not a
score artifact and contains no theory vector, residuals, likelihood values,
control scores, or validation result.

The COSEBIs path-mapping source-preflight ledger combines only source-side
availability flags. It records that COSEBIs target rows, redshift kernels, and
the 196-tile route coordinate index, the 300-row design skeleton, and the
58,800-row target-tile domain skeleton are available; that the path-weight rule
is declared but not computable; that the three-mask observable shell is partial;
and that a full source-frozen path/depth footprint mapping and web-environment
catalogue remain missing. It does not compute a mapping vector, theory vector,
predictions, residuals, likelihood values, or endpoint score.

The COSEBIs null-control readiness inventory declares four future control
families but does not execute them. It contains no control scores, predictions,
residuals, fit statistics, posterior-chain use, or data-vector-value use.

The COSEBIs null-control seed inventory freezes deterministic family seeds and
planned multiplicities for those future control families. It does not execute
sky rotations, pair shuffles, wrong-channel activations, or sign flips, and it
contains no control scores, predictions, residuals, fit statistics, posterior
chain use, or data-vector-value use.

The pilot frozen-product manifest includes three public distance-side files
under `data/raw/` only to test acquisition, hashing, covariance-shape checks,
and local provenance. These files are not sufficient for endpoint scoring
because the endpoint mask, calibration, nuisance-parameter, or systematics
policies are not frozen.

The Pantheon+ scope artifacts under `data/derived/` are row masks and summaries
derived only from source-side fields. They do not contain model residuals,
fitted Tau parameters, or endpoint scores.

The Pantheon+ scoring protocol manifest is also non-data. It freezes the future
scoring grammar and explicitly forbids score artifacts in the current scaffold.

The Pantheon+ design matrix is a dry-run input matrix. It contains source
columns and fixed basis columns only; it does not contain predictions,
residuals, likelihoods, or fitted parameters.

The Pantheon+ pilot scoring artifacts under `data/derived/` are a numerical
smoke test of the frozen scoring grammar. They use the diagonal of the retained
STAT+SYS covariance submatrix and are explicitly marked
`PILOT_SCORING_NOT_VALIDATION`. They are not a covariance-complete likelihood,
not empirical validation, and not evidence for a new dark-energy model.

The Pantheon+ full-covariance pilot scoring artifacts use the retained
STAT+SYS covariance submatrix with Cholesky solves and are explicitly marked
`FULL_COV_PILOT_SCORING_NOT_VALIDATION`. They are a stronger single-probe
pilot than the diagonal smoke test, but still not multi-probe validation and
not evidence for a new dark-energy model.

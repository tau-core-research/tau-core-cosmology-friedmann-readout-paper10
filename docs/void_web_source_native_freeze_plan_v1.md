# Void/Web Source-Native Freeze Plan V1

The first void/web full-covariance pilot intentionally used leakage-safe
redshift/scale-factor proxy bases. That pilot tested the scoring grammar, not
void or cosmic-web evidence.

This manifest is the next preflight layer:

```text
data/source_manifest/void_web_source_native_freeze_plan_v1.csv
```

It declares two source-native candidate routes:

- `VOID_VAST_DR7_PLANCK2018_V1` for `W_VOID_MATURITY`.
- `WEB_SDSS_DR17_MCPM_V1` for `W_WEB_ANISOTROPY`.

Both rows remain:

```text
SOURCE_NATIVE_CANDIDATE_SELECTED_NOT_FETCHED
endpoint_scoring_allowed=false
```

## Why This Gate Exists

The proxy pilot showed that the numerical pipeline can score a two-channel
void/web branch under the retained Pantheon+ full covariance, but the proxy
bases were functions of redshift and scale factor only. A real source-native
pilot must replace those bases with independent catalogue values before any
endpoint claim is allowed.

This gate prevents a common failure mode:

```text
look at distance residuals
    -> choose a convenient void threshold or web environment label
    -> rerun the endpoint
```

That route is forbidden. Void and web observables must be chosen from catalogue
metadata, masks, redshift ranges, and transformation rules before endpoint
residuals are inspected.

## Candidate Routes

### Void Maturity

The preferred next route is a VAST/SDSS DR7 void catalogue archive. This
replaces the previous Google Sites landing-page route for the numerical pilot,
because the cached Google Sites page is useful as provenance but is not a clean
source-native data product route in the current cache.

Allowed observables include void centres, redshifts, effective radii,
algorithm labels, cosmology labels, masks, and catalogue selection functions.

Forbidden inputs include distance residuals, fit-improvement flags, post-hoc
void thresholds, and late-time fit parameters.

### Cosmic-Web Anisotropy

The preferred next route is the SDSS DR17 MCPM cosmic-web density catalogue
identified by the SDSS DR18 value-added-catalogue page.

Allowed observables include galaxy identifiers or positions, redshifts,
MCPM density estimates, survey-program labels, sample masks, and release
metadata.

Forbidden inputs include growth residuals, lensing residuals, distance
residuals, fit-improvement flags, and post-hoc environment labels.

## Promotion Rule

These rows may be promoted only after a future manifest records:

- exact product file paths or immutable archive identifiers,
- local artifact paths,
- SHA-256 checksums,
- source-only transformation rules,
- mask/selection policies,
- and null controls.

Until then, the existing `W_void + W_web` result remains a proxy-only
full-covariance scoring-grammar stress test.

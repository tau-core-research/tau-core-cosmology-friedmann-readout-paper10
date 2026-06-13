**Doc class:** preauthorization diagnostic screen
**Reader role:** Paper10 observer/path projection audit
**Status:** fast screen; not replay authorization; not validation
**Canonical parent:** README.md

# V2 Observer-Basis Fast Screen

This screen accelerates the source-side observer/projection search after the
centered observer-orientation replay returned a useful diagnostic negative.
It does not require a reviewer before running because it is not an endpoint
replay and does not claim validation.

The screen uses the already frozen 12-row observer-orientation source table and
tests predeclared source-only basis functions built from:

- `W_path`
- sky-vector components `sky_x`, `sky_y`, `sky_z`
- scope-centered sky-vector components
- fixed sky-plane combinations
- source-redshift modulation by centered `zHD`

No distance residual, endpoint score, or fit statistic is allowed in family
construction. If a family both improves the baseline and survives its local
controls, the next step is a reviewer authorization package for that specific
family.

## Result

The screen finds a stronger preauthorization candidate:

```text
best_candidate_family = W_path_x_sky_x_x_zcenter
best_candidate_delta_chi2_minus_baseline = -0.58072431813
best_candidate_delta_chi2_minus_best_global_control = -0.02302956281
surviving_family_count = 4
surviving_families =
  W_path_x_sky_x_x_zcenter;
  W_path_x_centered_sky_yz_plus;
  W_path_x_sky_yz_plus;
  W_path_x_sky_z
```

The best family improves on the raw `W_path_x_sky_z` replay candidate, but this
is still only a preauthorization diagnostic screen. The next admissible step is
an external reviewer authorization package for
`W_path_x_sky_x_x_zcenter`.

## Claim Boundary

```text
v2_observer_basis_fast_screen_not_endpoint_not_validation
```

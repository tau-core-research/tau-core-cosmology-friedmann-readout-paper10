# Void Source-Basis Refinement V2 Projection/Morphology Gate

**Doc class:** source-side gate  
**Reader role:** reproducibility / claim-boundary reviewer  
**Status:** declared source-basis expansion, not endpoint scoring  
**Canonical parent:** `README.md`

This gate is the direct response to the weak refined-void replay result.  The
previous replay used a narrow void/source-basis and was beaten by frozen
controls.  V2 therefore does not introduce a new endpoint.  It first accounts
for the missing Tau Core projection/morphology channels:

- void morphology / maturity;
- cosmic-web morphology / anisotropy;
- observer/path projection along the null-geodesic bundle;
- time/readout projection for observed `a(t)`, `H(z)`, BAO, and CMB
  reconstruction consistency;
- CMB/lensing safety;
- multi-channel coupling controls.

The gate is intentionally blocking.  A component is not endpoint-ready merely
because it has a declared formula shell or a source route somewhere in the
repository.  It must have source-frozen values for the refined low-z replay and
family-appropriate null controls before a new endpoint authorization can be
requested.

This artifact does not compute scores, likelihoods, fit statistics, or physical
validation.  Its purpose is to prevent another void-only replay from being
overread as a full Tau Core projection/morphology test.

## Current source-freeze status

The first component promoted from "declared/available" to source-frozen is
`V2_WEB_MORPHOLOGY`.  Its low-z scope values are recorded in:

```text
data/derived/void_source_basis_refinement_v2_web_morphology_values.csv
data/derived/void_source_basis_refinement_v2_web_morphology_values_summary.csv
scripts/build_void_source_basis_refinement_v2_web_morphology_values_v1.py
scripts/validate_void_source_basis_refinement_v2_web_morphology_values_v1.py
```

These values are derived from the existing source-native `W_web` design matrix
and include deterministic null controls.  They do not contain endpoint scores,
distance residuals, or fit statistics, and they do not authorize replay.  The
V2 gate therefore remains blocked until the remaining projection/morphology
components are frozen with the same source-side discipline.

The second frozen support component is `V2_CMB_SAFETY`:

```text
data/derived/void_source_basis_refinement_v2_cmb_safety_values.csv
data/derived/void_source_basis_refinement_v2_cmb_safety_values_summary.csv
scripts/build_void_source_basis_refinement_v2_cmb_safety_values_v1.py
scripts/validate_void_source_basis_refinement_v2_cmb_safety_values_v1.py
```

This is a safety/support ledger only.  It records that the low-z replay scope is
below the predeclared CMB safety floor and that the existing late-time void/web
support check passes.  It does not use CMB map data, CMB likelihoods, endpoint
residuals, or fit statistics.

The observer/path projection channel is recorded as a route ledger:

```text
data/derived/void_source_basis_refinement_v2_path_projection_route_ledger.csv
data/derived/void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv
scripts/build_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py
scripts/validate_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py
```

This ledger preserves the current blocker rather than hiding it.  KiDS/path
source products are route-supported, but the low-z Pantheon scope does not
currently carry the sky-coordinate crossmap needed to assign source-frozen
`W_path` values.  Therefore `W_path_source_value` remains `NA` and endpoint
replay remains forbidden.

The time/readout projection channel is also recorded as a route ledger:

```text
data/derived/void_source_basis_refinement_v2_time_readout_route_ledger.csv
data/derived/void_source_basis_refinement_v2_time_readout_route_ledger_summary.csv
scripts/build_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py
scripts/validate_void_source_basis_refinement_v2_time_readout_route_ledger_v1.py
```

This ledger records that the clock/readout channel is declared, but the
required CC/BAO/CMB products remain selected-not-fetched and the activation
rule remains non-numeric.  Therefore `W_time_source_value` remains `NA`; no
clock anomaly, late-time fit, endpoint residual, or time-kernel score is
claimed.

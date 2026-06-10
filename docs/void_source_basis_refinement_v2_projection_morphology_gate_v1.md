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

The void-morphology component is source-frozen, but its weak-negative status is
preserved:

```text
data/derived/void_source_basis_refinement_v2_void_morphology_values.csv
data/derived/void_source_basis_refinement_v2_void_morphology_values_summary.csv
scripts/build_void_source_basis_refinement_v2_void_morphology_values_v1.py
scripts/validate_void_source_basis_refinement_v2_void_morphology_values_v1.py
```

This ledger carries the existing low-z `W_void` values and deterministic null
controls, but it also records the previous control-dominance audit verdict:
the refined void replay remains weak-negative because shuffled controls beat
the candidate.  This is intentionally preserved rather than repaired
post-hoc.

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
data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit.csv
data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_policy.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_values.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_values_summary.csv
docs/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.md
data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_policy_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_response_template_v1.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip.sha256
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_manifest.csv
data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_summary.csv
data/derived/void_source_basis_refinement_v2_path_projection_route_ledger.csv
data/derived/void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv
scripts/build_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py
scripts/validate_void_source_basis_refinement_v2_path_projection_crossmap_audit_v1.py
scripts/build_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_policy_v1.py
scripts/build_void_source_basis_refinement_v2_path_partial_scope_values_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_values_v1.py
scripts/build_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py
scripts/validate_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py
scripts/build_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py
scripts/validate_void_source_basis_refinement_v2_path_projection_route_ledger_v1.py
```

This ledger preserves the current blocker rather than hiding it.  KiDS/path
source products are route-supported, and the low-z Pantheon geometry join does
carry RA/DEC.  The crossmap audit finds partial KiDS tile candidates, but not a
complete low-z crossmap and not a frozen Pantheon-row path-weight rule.
The partial-scope policy freezes this as 5 strict and 7 caveated path-scope
candidate rows.  This is not enough to promote `W_path` as a full low-z channel.
For those 12 rows only, a source-only tile-proximity control value is frozen
from the nearest KiDS tile separation.  This value is a residual-blind control
proxy, not a calibrated physical lensing-path weight and not a replay
authorization.
The accompanying reviewer package exposes the crossmap audit, partial-scope
policy, frozen values, and blank response template for a reviewer without
repository access.  That package is source-side only: even an accepted response
can only support a later, separate partial-scope replay authorization request.
Therefore `W_path_source_value` remains `NA` and endpoint replay remains
forbidden.

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

The multi-channel coupling component is recorded as a source-side coupling
ledger:

```text
data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger.csv
data/derived/void_source_basis_refinement_v2_multichannel_coupling_ledger_summary.csv
scripts/build_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py
scripts/validate_void_source_basis_refinement_v2_multichannel_coupling_ledger_v1.py
```

This ledger does not repair the weak replay.  It freezes the current coupling
accounting: void and web source values are present, CMB safety is satisfied for
the low-z support scope, but path and time values remain unavailable and the
void branch keeps its weak-negative/control-dominance verdict.  Therefore even
the computable void-web value pair is not endpoint-ready.  All coupling rules
keep `endpoint_ready=false`, `endpoint_replay_allowed=false`, and
`endpoint_validation_claimed=false`.

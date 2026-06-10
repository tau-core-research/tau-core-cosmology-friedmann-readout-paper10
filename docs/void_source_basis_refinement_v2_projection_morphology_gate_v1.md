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

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

## Reproduce

```bash
python scripts/reproduce.py
```

The reproduction script compiles the manuscript with `tectonic`, validates the
source-freeze manifest, builds the arXiv source package, and runs smoke tests.

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

The first scoring grammar is frozen, but not run:

```text
data/source_manifest/pantheon_scoring_protocol_v1.csv
docs/pantheon_scoring_protocol_v1.md
```

It declares the baseline family, nuisance policy, Tau activation family, and
required future controls. It also keeps `scoring_allowed=false`.

## Scope

This is a protocol scaffold and branch-opening paper package. The next
scientific milestone is a real-data pilot using public distance, void,
cosmic-web, growth, lensing, and CMB products under the frozen audit ladder.

# Void Source-Basis Refinement R6 External Reviewer Instructions v1

**Doc class:** external reviewer instructions  
**Reader role:** independent source-side reviewer  
**Status:** handoff instruction; not a completed review  
**Canonical parent:** `docs/void_source_basis_refinement_r6_reviewer_handoff_package_v1.md`

## Purpose

This handoff asks you to review only the attached source-side void-basis
refinement materials. The goal is to decide whether R1-R5 provide a caveated
source-side basis that is clean enough to request a separate replay gate later.

This review does not authorize endpoint replay and does not claim empirical or
physical validation.

## Transfer Integrity Check

If you received the ZIP and `.zip.sha256` sidecar together, first put both files
in the same directory and verify that the transferred ZIP matches the recorded
checksum:

```bash
shasum -a 256 -c void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip.sha256
```

Expected result:

```text
void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip: OK
```

You can inspect the package contents without extracting it:

```bash
unzip -l void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip
```

## Files to Inspect

- `data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1.csv`
- `data/derived/void_source_basis_refinement_r4_independence_preflight_v1.csv`
- `data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1.csv`
- `data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv`
- `data/derived/low_z_pantheon_void_geometry_join_v1.csv`
- `data/derived/low_z_pantheon_los_environment_v1.csv`
- the corresponding docs under `docs/`
- the source-native void catalogue and SDSS/MCPM line-of-sight source product
  included under `data/raw/`

## File to Complete

Complete:

```text
data/derived/void_source_basis_refinement_r6_reviewer_template_v1.csv
```

Return the completed CSV to the author. Do not add endpoint scores, distance
residuals, fit statistics, post-score residual-shape notes, or validation
claims.

## Forbidden Inputs

Do not use:

- endpoint scores;
- distance residuals;
- fit statistics;
- post-score residual shapes;
- post-hoc row or source selection;
- post-hoc void thresholds;
- post-hoc amplitude tuning;
- post-hoc covariance reweighting;
- physical-validation claims.

## Allowed Accepting Verdict

The only accepting verdict in this handoff is:

```text
ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW
```

This means the source-side review is acceptable as caveated input evidence. It
does not authorize endpoint replay and does not claim endpoint validation.

## Claim Boundary

This review can only close the R6 source-side leakage review. Any future replay
still requires a separate endpoint authorization gate.

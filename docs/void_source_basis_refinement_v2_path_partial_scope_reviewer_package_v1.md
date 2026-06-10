# V2 Path Partial-Scope Reviewer Package v1

**Doc class:** external reviewer handoff  
**Reader role:** source-side / leakage reviewer  
**Status:** reviewer package, not endpoint replay authorization  
**Canonical parent:** `docs/void_source_basis_refinement_v2_projection_morphology_gate_v1.md`

This package asks an external or author-side reviewer to audit the current
`W_path` partial-scope result without repository access.

The package does not request endpoint scoring.  It asks only whether the
12-row partial path-scope control can be kept as a source-side candidate for a
future, separate partial-scope replay authorization review, or whether `W_path`
must remain disabled for the low-z Pantheon replay.

## Current frozen facts

- The full low-z scope contains 424 rows.
- Low-z Pantheon RA/DEC are available.
- KiDS tile coordinates are available from source-side mask-route filenames.
- The crossmap audit finds 5 strict and 7 caveated path-scope candidate rows.
- The remaining 412 rows are not path-scope eligible.
- A source-only tile-proximity control value is frozen for the 12 candidate
  rows.
- The value is not a calibrated physical lensing-path weight.
- No endpoint residuals, distance residuals, lensing residuals, fit statistics,
  posterior chains, or KiDS data-vector values are used.

## Frozen rule under review

For the 12 predeclared partial-scope candidate rows only:

```text
P_tile = max(0, (2 deg - nearest_tile_sep_deg) / 2 deg)
W_path = P_tile / (1 + abs(P_tile))
```

Rows outside the partial-scope candidate set keep:

```text
W_path = 0
```

This is a residual-blind tile-proximity control.  It is not promoted here as a
physical lensing kernel and not as a full low-z `W_path` channel.

## Reviewer decision requested

Please fill the included response CSV.  The key decision is one of:

```text
ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE
REJECT_KEEP_W_PATH_DISABLED
REQUEST_MORE_SOURCE_EVIDENCE
```

Even an accepted response does not authorize endpoint scoring.  It only permits
the authors to prepare a separate partial-scope replay authorization package.

## Integrity check

If you received the `.zip` and `.zip.sha256` files together, place them in the
same directory and run:

```bash
shasum -a 256 -c void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip.sha256
```

Expected output:

```text
void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.zip: OK
```

## Included key files

- `data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_response_template_v1.csv`
- `data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv`
- `data/derived/void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv`
- `data/derived/void_source_basis_refinement_v2_path_partial_scope_values_summary.csv`
- `data/derived/void_source_basis_refinement_v2_path_partial_scope_policy.csv`
- `data/derived/void_source_basis_refinement_v2_path_partial_scope_values.csv`
- `docs/void_source_basis_refinement_v2_projection_morphology_gate_v1.md`

The detailed per-row files are included so the reviewer can inspect which rows
are strict, caveated, or path-off without accessing the repository.

# KiDS-1000 COSEBIs External Photo-z Calibration Reviewer Instructions V1

**Doc class:** external reviewer instructions
**Reader role:** independent source-side reviewer
**Status:** handoff instruction; not a completed review
**Canonical parent:** `docs/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.md`

## Purpose

This handoff asks you to review only the attached public source-side materials
for the KiDS-1000 external photo-z calibration route. The goal is to decide
whether the attached sources support a caveated source-side R4 leakage review
without inspecting endpoint results.

## Transfer Integrity Check

If you received the ZIP and `.zip.sha256` sidecar together, first put both files
in the same directory and verify that the transferred ZIP matches the recorded
checksum:

```bash
shasum -a 256 -c kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip.sha256
```

The expected result is:

```text
kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip: OK
```

You can inspect the package contents without extracting it:

```bash
unzip -l kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip
```

## Files to Inspect

- `data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv`
- `data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.csv`
- `docs/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.md`
- `docs/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.md`
- cached source pages under `data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1/`

## File to Complete

Complete:

```text
data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv
```

Return the completed CSV to the author. Do not add endpoint scores, endpoint
residuals, ranks, fit statistics, observed COSEBIs values, or post-score
residual-shape notes.

## Forbidden Inputs

Do not use:

- observed COSEBIs values,
- endpoint residuals,
- endpoint scores,
- `Delta chi2` or AIC endpoint statistics,
- null-control ranks,
- best-control identities,
- post-score residual shapes,
- any endpoint-scoring outputs.

## Allowed Verdict

The only accepting R4 verdict in this handoff is:

```text
ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW
```

This means the source-side review is acceptable as caveated input evidence. It
does not authorize endpoint replay and does not claim endpoint validation.

## Optional Local Validation

After filling the CSV, the author can validate it with:

```bash
python scripts/validate_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.py \
  completed_reviewer_response.csv \
  --summary-out completed_reviewer_response_summary.csv
```

An accepted validation summary still keeps:

```text
endpoint_replay_allowed=false
endpoint_validation_claimed=false
```

## Claim Boundary

This review can only close the source-side reviewer attestation for the
external photo-z calibration route. It cannot by itself promote the endpoint to
validation status.

# KiDS-1000 Photo-z Reviewer Handoff

This package is a source-side reviewer handoff for the KiDS-1000 external
photo-z calibration route. It is not an endpoint replay package and it is not a
validation claim.

## First Checks

If you received the ZIP and `.zip.sha256` sidecar together, place both files in
the same directory and run:

```bash
shasum -a 256 -c kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip.sha256
```

Expected result:

```text
kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip: OK
```

## Start Here

Read:

```text
docs/kids1000_cosebis_external_photoz_calibration_external_reviewer_instructions_v1.md
```

Complete:

```text
data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv
```

## Boundary

Do not inspect or use endpoint residuals, endpoint scores, ranks, fit
statistics, observed COSEBIs values, post-score residual shapes, or endpoint
scoring outputs. A completed review can only support a source-side, caveated
R4/H1 reviewer attestation. It does not authorize endpoint replay or endpoint
validation.

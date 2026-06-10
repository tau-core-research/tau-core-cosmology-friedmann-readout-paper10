# KiDS-1000 COSEBIs External Photo-z Calibration Reviewer Handoff Package V1

**Doc class:** independent reviewer handoff package
**Reader role:** portable ZIP package for the remaining R4 attestation
**Status:** package built; review not completed
**Canonical parent:** `README.md`

## Contents

The package contains a root reviewer README, the blank reviewer attestation
template, external reviewer instructions, the source manifest, the
leakage-review preflight, the completed-response validation policy and script,
short documentation, and the three cached public source pages used by the
source manifest.

## Boundary

The package contains no endpoint residuals, endpoint scores, ranks, fit
statistics, or post-score residual shapes. It does not complete R4, does not
complete H1, does not authorize endpoint replay, and does not claim validation.
The included completed-response validator only checks a returned reviewer CSV
against the source-side no-leakage rules.

The adjacent `.zip.sha256` file is an integrity sidecar for transfer checks. It
does not add reviewer evidence and does not change the claim boundary.

## Transfer Check

The recipient can verify the transferred ZIP after placing the ZIP and
`.zip.sha256` files in the same directory:

```bash
shasum -a 256 -c kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip.sha256
```

This check only verifies file integrity. It is not a source review and does not
complete R4 or H1.

## Verdict

`reviewer_handoff_package_ready_not_completed`

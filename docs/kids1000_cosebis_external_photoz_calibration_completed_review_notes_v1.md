# KiDS-1000 COSEBIs External Photo-z Calibration Completed Source-Side Review V1

## Completed response

- Completed reviewer response CSV: `kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.csv`
- Validation summary CSV: `kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1_summary.csv`
- Accepted source-side verdict: `ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW`

## Checks performed

- Verified the inner reviewer handoff ZIP against the provided `.zip.sha256` sidecar: `OK`.
- Checked the extracted package manifest hashes against the extracted files: all listed artifacts matched.
- Inspected only the allowed source-side materials: source manifest, leakage preflight, reviewer instructions/template, and cached public source pages under `data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1/`.
- Did not inspect or use observed COSEBIs values, endpoint residuals, endpoint scores, ranks, fit statistics, post-score residual shapes, or endpoint-scoring outputs.
- Kept `forbidden_inputs_used=false`, `endpoint_replay_allowed=false`, and `endpoint_validation_claimed=false` in all completed response rows.

## Source-side basis for acceptance

- `KIDS1000_PHOTOZ_CALIBRATION_AANDA.html` matched the A&A article `KiDS-1000 catalogue: Redshift distributions and their calibration` and contained the expected SOM calibration, five tomographic-bin, gold-selection, mean-redshift calibration-bias/uncertainty, clustering-redshift cross-check, and Table 3 markers.
- `KIDS1000_PHOTOZ_CALIBRATION_ARXIV.html` matched `arXiv:2007.15635` with the same title and DOI metadata.
- `KIDS1000_SOM_GOLD_CATALOGUE.html` matched the official KiDS DR4 `Weak lensing SOM-gold catalogue` page and included the KiDS-1000 catalogue and SOM-calibrated n(z) tarball route for the five tomographic bins.

## Validation note

The bundled validator script references `data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_summary.csv`, which was not present in the supplied ZIP. In a scratch copy, I reconstructed the minimal handoff summary from the package manifest so that the bundled validator could perform its declared handoff-verdict and no-replay checks. The completed response then passed the bundled validator, producing the included validation summary.

The validation summary still keeps `endpoint_replay_allowed=false` and `endpoint_validation_claimed=false`; this review is source-side only and does not authorize endpoint replay or claim endpoint validation.

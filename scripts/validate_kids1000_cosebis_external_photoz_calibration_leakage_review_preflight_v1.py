#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_policy_v1.csv"
PREFLIGHT = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(PREFLIGHT)
    summary = read_one(SUMMARY)

    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_LEAKAGE_REVIEW_PREFLIGHT_POLICY_FROZEN":
        raise SystemExit("unexpected leakage-review preflight policy status")
    if policy["current_endpoint_replay_allowed"] != "false":
        raise SystemExit("policy must not authorize replay")
    if summary["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_LEAKAGE_REVIEW_PREFLIGHT_BUILT":
        raise SystemExit("unexpected leakage-review preflight summary status")
    if summary["check_count"] != "4" or len(rows) != 4:
        raise SystemExit("expected four leakage preflight checks")
    if summary["passed_checks"] != "3" or summary["failed_checks"] != "0" or summary["open_checks"] != "1":
        raise SystemExit("expected three automated passes and one open reviewer check")
    if summary["automated_leakage_preflight_complete"] != "true":
        raise SystemExit("automated leakage preflight should be complete")
    if summary["independent_reviewer_attestation_complete"] != "false":
        raise SystemExit("independent reviewer attestation must remain open")
    if summary["r4_leakage_review_complete"] != "false":
        raise SystemExit("full R4 leakage review must remain incomplete")
    if summary["h1_independent_evidence_complete"] != "false":
        raise SystemExit("H1 must remain incomplete")
    for key in [
        "computes_new_scores",
        "uses_kids_data_vector_values_for_scoring",
        "uses_kids_data_vector_values_for_source_selection",
        "uses_residuals",
        "uses_fit_statistics",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    expected_status = {
        "L1_manifest_metadata_no_forbidden_inputs": "PASS",
        "L2_cached_public_sources_present": "PASS",
        "L3_source_manifest_builder_has_no_endpoint_dependencies": "PASS",
        "L4_independent_reviewer_attestation": "OPEN",
    }
    for row in rows:
        if expected_status.get(row["check_id"]) != row["check_status"]:
            raise SystemExit(f"unexpected check status for {row['check_id']}")
        if row["uses_endpoint_fields"] != "false":
            raise SystemExit("preflight checks must not use endpoint fields")
        if row["forbidden_inputs_used"] != "false":
            raise SystemExit("preflight checks must not use forbidden inputs")
        if row["endpoint_replay_allowed"] != "false" or row["endpoint_validation_claimed"] != "false":
            raise SystemExit("preflight rows must not authorize replay or validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    if summary["verdict"] != "automated_leakage_preflight_passed_independent_reviewer_still_open":
        raise SystemExit("unexpected leakage-review preflight verdict")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_LEAKAGE_REVIEW_PREFLIGHT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

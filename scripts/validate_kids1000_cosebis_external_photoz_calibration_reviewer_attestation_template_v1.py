#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_policy_v1.csv"
TEMPLATE = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1_summary.csv"


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
    rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)
    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_ATTESTATION_TEMPLATE_POLICY_FROZEN":
        raise SystemExit("unexpected reviewer-attestation template policy status")
    if summary["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_ATTESTATION_TEMPLATE_BUILT_NOT_COMPLETED":
        raise SystemExit("unexpected reviewer-attestation template summary status")
    if len(rows) != 4 or summary["question_count"] != "4":
        raise SystemExit("reviewer-attestation template must contain four questions")
    for key in [
        "review_completed",
        "independent_reviewer_attestation_complete",
        "r4_leakage_review_complete",
        "h1_independent_evidence_complete",
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
    expected = {
        "Q1_source_identity",
        "Q2_no_endpoint_fields",
        "Q3_route_coverage",
        "Q4_r4_decision",
    }
    if {row["question_id"] for row in rows} != expected:
        raise SystemExit("unexpected reviewer template question set")
    for row in rows:
        for empty_key in ["reviewer_response", "reviewer_rationale", "reviewer_id_or_role"]:
            if row[empty_key]:
                raise SystemExit(f"template must leave {empty_key} blank")
        if row["review_completed"] != "false":
            raise SystemExit("template rows must not be completed")
        if row["forbidden_inputs_used"] != "false":
            raise SystemExit("template rows must not use forbidden inputs")
        if row["endpoint_replay_allowed"] != "false" or row["endpoint_validation_claimed"] != "false":
            raise SystemExit("template rows must not authorize replay or validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    if summary["verdict"] != "reviewer_attestation_template_ready_not_completed":
        raise SystemExit("unexpected reviewer-attestation template verdict")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_ATTESTATION_TEMPLATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

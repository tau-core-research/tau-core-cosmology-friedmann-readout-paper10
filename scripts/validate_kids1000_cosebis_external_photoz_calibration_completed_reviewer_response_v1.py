#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_policy_v1.csv"
HANDOFF_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_summary.csv"

EXPECTED_QUESTIONS = {
    "Q1_source_identity",
    "Q2_no_endpoint_fields",
    "Q3_route_coverage",
    "Q4_r4_decision",
}


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def norm(value: str) -> str:
    return value.strip().lower()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_response(rows: list[dict[str, str]]) -> None:
    require(len(rows) == 4, "completed reviewer response must contain exactly four rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "unexpected reviewer response question set")
    by_question = {row["question_id"]: row for row in rows}

    for row in rows:
        require(norm(row["review_completed"]) == "true", "all reviewer rows must set review_completed=true")
        require(norm(row["forbidden_inputs_used"]) == "false", "reviewer response must keep forbidden_inputs_used=false")
        require(norm(row["endpoint_replay_allowed"]) == "false", "reviewer response must not authorize endpoint replay")
        require(norm(row["endpoint_validation_claimed"]) == "false", "reviewer response must not claim endpoint validation")
        require(row["reviewer_id_or_role"].strip(), "reviewer_id_or_role must be nonempty")
        require(row["reviewer_rationale"].strip(), "reviewer_rationale must be nonempty")

    require(norm(by_question["Q1_source_identity"]["reviewer_response"]) == "yes", "Q1 must be answered yes")
    require(norm(by_question["Q2_no_endpoint_fields"]["reviewer_response"]) == "yes", "Q2 must be answered yes")
    require(
        norm(by_question["Q3_route_coverage"]["reviewer_response"]) in {"yes", "caveated_yes", "yes_caveated"},
        "Q3 must be answered yes or caveated_yes",
    )
    require(
        by_question["Q4_r4_decision"]["reviewer_response"].strip() == "ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW",
        "Q4 must accept the source-side R4 review as caveated",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a completed source-side KiDS photo-z independent reviewer response."
    )
    parser.add_argument("response_csv", type=Path)
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1_summary.csv",
    )
    args = parser.parse_args()

    response_path = args.response_csv.resolve()
    if not response_path.exists():
        raise SystemExit(f"missing completed reviewer response: {response_path}")

    policy = read_one(POLICY)
    handoff = read_one(HANDOFF_SUMMARY)
    rows = read_rows(response_path)
    require(policy["status"] == "EXTERNAL_PHOTOZ_CALIBRATION_COMPLETED_REVIEWER_RESPONSE_POLICY_FROZEN", "unexpected completed-response policy status")
    require(handoff["verdict"] == "reviewer_handoff_package_ready_not_completed", "completed response must derive from a ready handoff package")
    require(handoff["endpoint_replay_allowed"] == "false", "handoff package must not authorize endpoint replay")
    validate_response(rows)

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "EXTERNAL_PHOTOZ_CALIBRATION_COMPLETED_REVIEWER_RESPONSE_ACCEPTED_SOURCE_SIDE_ONLY",
            "response_path": display_path(response_path),
            "response_sha256": sha256(response_path),
            "review_completed": "true",
            "independent_reviewer_attestation_complete": "true",
            "r4_leakage_review_complete": "true",
            "h1_independent_evidence_complete": "true",
            "computes_new_scores": "false",
            "contains_endpoint_data": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "completed_reviewer_response_accepted_source_side_only_endpoint_replay_still_forbidden",
            "recommended_next_action": "human_review_before_any_separate_endpoint_replay_gate",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(args.summary_out, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_COMPLETED_REVIEWER_RESPONSE_V1_VALIDATED "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

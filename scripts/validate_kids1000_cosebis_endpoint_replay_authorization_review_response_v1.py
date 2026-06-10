#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_replay_authorization_review_policy_v1.csv"
CLOSURE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv"

EXPECTED_QUESTIONS = {
    "Q1_package_integrity",
    "Q2_source_side_closure",
    "Q3_no_leakage",
    "Q4_replay_authorization",
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
    require(len(rows) == 4, "authorization response must contain exactly four rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "unexpected authorization response question set")
    by_question = {row["question_id"]: row for row in rows}

    for row in rows:
        require(norm(row["review_completed"]) == "true", "all authorization rows must set review_completed=true")
        require(norm(row["forbidden_inputs_used"]) == "false", "authorization response must keep forbidden_inputs_used=false")
        require(norm(row["endpoint_validation_claimed"]) == "false", "authorization response must not claim endpoint validation")
        require(row["reviewer_id_or_role"].strip(), "reviewer_id_or_role must be nonempty")
        require(row["reviewer_rationale"].strip(), "reviewer_rationale must be nonempty")
        require(
            row["authorization_scope"].strip()
            == "single_predeclared_endpoint_replay_under_existing_frozen_source_side_state_permission_only_not_validation",
            "authorization_scope must remain limited to one predeclared replay and not validation",
        )
        require(
            row["claim_boundary"].strip() == "endpoint_replay_permission_review_not_validation",
            "unexpected claim boundary",
        )

    require(norm(by_question["Q1_package_integrity"]["reviewer_response"]) == "yes", "Q1 must be answered yes")
    require(
        norm(by_question["Q2_source_side_closure"]["reviewer_response"]) in {"yes", "caveated_yes", "yes_caveated"},
        "Q2 must be answered yes or caveated_yes",
    )
    require(norm(by_question["Q3_no_leakage"]["reviewer_response"]) == "yes", "Q3 must be answered yes")
    require(
        by_question["Q4_replay_authorization"]["reviewer_response"].strip()
        == "GO_SOURCE_SIDE_REPLAY_PERMISSION_ONLY",
        "Q4 must explicitly authorize replay permission only",
    )
    require(
        all(norm(row["endpoint_replay_allowed"]) == "true" for row in rows),
        "accepted authorization response must set endpoint_replay_allowed=true in every row",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate the KiDS-1000 COSEBIs endpoint replay authorization review response."
    )
    parser.add_argument("response_csv", type=Path)
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=ROOT
        / "data"
        / "derived"
        / "kids1000_cosebis_endpoint_replay_authorization_review_response_v1_summary.csv",
    )
    args = parser.parse_args()

    response_path = args.response_csv.resolve()
    if not response_path.exists():
        raise SystemExit(f"missing authorization response: {response_path}")

    policy_rows = read_rows(POLICY)
    closure = read_one(CLOSURE_SUMMARY)
    rows = read_rows(response_path)

    require(len(policy_rows) == 4, "authorization policy must contain four rows")
    require(closure["verdict"] == "external_photoz_calibration_source_side_closed_endpoint_replay_still_forbidden", "source-side closure must precede replay authorization")
    require(closure["r4_leakage_review_complete"] == "true", "R4 must be source-side complete before replay authorization")
    require(closure["h1_independent_evidence_complete"] == "true", "H1 must be source-side complete before replay authorization")
    require(closure["endpoint_validation_claimed"] == "false", "closure ledger must not claim endpoint validation")
    validate_response(rows)

    summary = [
        {
            "policy_id": "KIDS1000_COSEBIS_ENDPOINT_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "ENDPOINT_REPLAY_AUTHORIZATION_REVIEW_ACCEPTED_PERMISSION_ONLY",
            "response_path": display_path(response_path),
            "response_sha256": sha256(response_path),
            "review_completed": "true",
            "source_side_closure_confirmed": "true",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "authorization_scope": "single_predeclared_endpoint_replay_under_existing_frozen_source_side_state_permission_only_not_validation",
            "verdict": "endpoint_replay_authorized_permission_only_not_validation",
            "recommended_next_action": "run_only_the_separate_predeclared_endpoint_replay_without_validation_claim",
            "claim_boundary": "endpoint_replay_permission_review_not_validation",
        }
    ]
    write_csv(args.summary_out, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_REPLAY_AUTHORIZATION_REVIEW_RESPONSE_V1_VALIDATED "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

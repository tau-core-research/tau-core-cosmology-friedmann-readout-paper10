#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_package_v1_summary.csv"
REVIEW_RESPONSE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_response_v1_summary.csv"
ENDPOINT_PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_package_v1_summary.csv"
CONTROL_SUITE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_endpoint_scoring_authorization_blocker_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    review_package = read_one(REVIEW_PACKAGE)
    control_suite = read_one(CONTROL_SUITE)
    if review_package["status"] != "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("control-suite review package is not ready-not-completed")
    if control_suite["verdict"] != "NUMERIC_T_JOINT_CONTROL_SUITE_BUILT_PREVALIDATION_NOT_ENDPOINT_SCORING":
        raise SystemExit("numeric control suite is not in expected prevalidation state")
    if control_suite["controls_beating_or_equal_candidate"] != "0":
        raise SystemExit("unexpected control-suite result; expected 0 controls beating/equal candidate")

    review_response_exists = REVIEW_RESPONSE.exists()
    endpoint_package_exists = ENDPOINT_PACKAGE.exists()
    if review_response_exists:
        review_response = read_one(REVIEW_RESPONSE)
        review_completed = review_response.get("review_completed", "false")
        prep_allowed = review_response.get("endpoint_scoring_authorization_package_preparation_allowed", "false")
        if review_completed == "true" and prep_allowed == "true" and endpoint_package_exists:
            current_blocker = "endpoint_scoring_authorization_response_missing"
            next_action = "send_endpoint_authorization_zip_to_reviewer_then_import_completed_response"
            verdict = "endpoint_authorization_package_ready_waiting_for_response"
        elif review_completed == "true" and prep_allowed == "true":
            current_blocker = "endpoint_scoring_authorization_package_missing"
            next_action = "build_endpoint_scoring_authorization_package_without_running_scoring"
            verdict = "endpoint_authorization_package_preparation_allowed_not_built"
        elif review_completed == "true":
            current_blocker = "control_suite_review_rejected_or_did_not_authorize_endpoint_package_preparation"
            next_action = "keep_endpoint_scoring_blocked_or_revise_control_suite_review"
            verdict = "endpoint_authorization_preparation_not_allowed"
        else:
            current_blocker = "control_suite_review_response_incomplete"
            next_action = "obtain_completed_control_suite_review_response"
            verdict = "endpoint_authorization_blocked_waiting_completed_review"
    else:
        review_completed = "false"
        prep_allowed = "false"
        current_blocker = "control_suite_review_response_missing"
        next_action = "send_control_suite_review_zip_to_reviewer_then_import_completed_response"
        verdict = "endpoint_authorization_blocked_waiting_control_suite_review_response"

    row = {
        "status_id": "JOINT_NUMERIC_T_JOINT_ENDPOINT_SCORING_AUTHORIZATION_BLOCKER_STATUS_V1",
        "status": "JOINT_NUMERIC_T_JOINT_ENDPOINT_SCORING_AUTHORIZATION_BLOCKED_NOT_SCORING_NOT_VALIDATION",
        "review_package_exists": "true",
        "review_response_exists": str(review_response_exists).lower(),
        "endpoint_authorization_package_exists": str(endpoint_package_exists).lower(),
        "review_completed": review_completed,
        "endpoint_scoring_authorization_package_preparation_allowed": prep_allowed,
        "candidate_numeric_t_joint": control_suite["candidate_numeric_t_joint"],
        "numeric_control_count": control_suite["numeric_control_count"],
        "controls_beating_or_equal_candidate": control_suite["controls_beating_or_equal_candidate"],
        "current_blocker": current_blocker,
        "next_required_action": next_action,
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "verdict": verdict,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, [row])
    write_csv(SUMMARY, [row])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint endpoint-scoring authorization blocker status v1",
                "",
                "**Doc class:** blocker ledger.",
                "**Status:** blocked; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"Candidate numeric `T_joint`: `{row['candidate_numeric_t_joint']}`.",
                f"Control-suite result: `{row['controls_beating_or_equal_candidate']}/{row['numeric_control_count']}` controls beat or equal the candidate.",
                f"Current blocker: `{row['current_blocker']}`.",
                f"Next required action: `{row['next_required_action']}`.",
                "",
                "This artifact does not authorize endpoint scoring, endpoint validation,",
                "cosmological validation, or physical validation.",
                "",
            ]
        )
    )
    print(f"JOINT_NUMERIC_T_JOINT_ENDPOINT_SCORING_AUTHORIZATION_BLOCKER_STATUS_V1_BUILT blocker={current_blocker}")


if __name__ == "__main__":
    main()

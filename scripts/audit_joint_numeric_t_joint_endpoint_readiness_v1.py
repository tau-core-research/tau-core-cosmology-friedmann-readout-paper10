#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_SUITE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1_summary.csv"
REVIEW_PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_package_v1_summary.csv"
REVIEW_RESPONSE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_response_v1_summary.csv"
BLOCKER = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_endpoint_readiness_audit_v1.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_endpoint_readiness_audit_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_endpoint_readiness_audit_not_scoring_not_validation"


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


def write_csv(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    control = read_one(CONTROL_SUITE)
    package = read_one(REVIEW_PACKAGE)
    blocker = read_one(BLOCKER)
    response_exists = REVIEW_RESPONSE.exists()
    response = read_one(REVIEW_RESPONSE) if response_exists else {}

    control_suite_valid = control["verdict"] == "NUMERIC_T_JOINT_CONTROL_SUITE_BUILT_PREVALIDATION_NOT_ENDPOINT_SCORING"
    zero_control_result = control["controls_beating_or_equal_candidate"] == "0"
    review_package_ready = package["status"] == "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_PACKAGE_READY_NOT_COMPLETED"
    response_accepts_prep = (
        response_exists
        and response.get("decision") == "AUTHORIZE_PREPARE_ENDPOINT_SCORING_AUTHORIZATION_PACKAGE_NOT_SCORING"
        and response.get("endpoint_scoring_authorization_package_preparation_allowed") == "true"
    )
    blocker_consistent = blocker["current_blocker"] in {
        "control_suite_review_response_missing",
        "endpoint_scoring_authorization_package_missing",
        "endpoint_scoring_authorization_response_missing",
    }

    endpoint_authorization_package_build_ready = (
        control_suite_valid
        and zero_control_result
        and review_package_ready
        and response_accepts_prep
        and blocker_consistent
    )
    if endpoint_authorization_package_build_ready:
        readiness = "READY_TO_BUILD_ENDPOINT_AUTHORIZATION_PACKAGE_NOT_SCORING"
        next_action = "build_endpoint_scoring_authorization_package_without_running_scoring"
    else:
        readiness = "BLOCKED_BEFORE_ENDPOINT_AUTHORIZATION_PACKAGE"
        next_action = blocker["next_required_action"]

    row = {
        "audit_id": "JOINT_NUMERIC_T_JOINT_ENDPOINT_READINESS_AUDIT_V1",
        "candidate_numeric_t_joint": control["candidate_numeric_t_joint"],
        "numeric_control_count": control["numeric_control_count"],
        "controls_beating_or_equal_candidate": control["controls_beating_or_equal_candidate"],
        "control_suite_valid": str(control_suite_valid).lower(),
        "zero_control_result": str(zero_control_result).lower(),
        "review_package_ready": str(review_package_ready).lower(),
        "review_response_exists": str(response_exists).lower(),
        "review_response_accepts_endpoint_package_preparation": str(response_accepts_prep).lower(),
        "current_blocker": blocker["current_blocker"],
        "endpoint_authorization_package_build_ready": str(endpoint_authorization_package_build_ready).lower(),
        "readiness": readiness,
        "next_required_action": next_action,
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, row)
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint endpoint readiness audit v1",
                "",
                "**Doc class:** readiness audit.",
                "**Status:** not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"Candidate numeric `T_joint`: `{row['candidate_numeric_t_joint']}`.",
                f"Control-suite result: `{row['controls_beating_or_equal_candidate']}/{row['numeric_control_count']}` controls beat or equal the candidate.",
                f"Review response exists: `{row['review_response_exists']}`.",
                f"Current blocker: `{row['current_blocker']}`.",
                f"Readiness: `{row['readiness']}`.",
                f"Next required action: `{row['next_required_action']}`.",
                "",
                "This audit does not authorize endpoint scoring, endpoint validation,",
                "cosmological validation, or physical validation.",
                "",
            ]
        )
    )
    print(f"JOINT_NUMERIC_T_JOINT_ENDPOINT_READINESS_AUDIT_V1 {readiness}")
    if not endpoint_authorization_package_build_ready:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

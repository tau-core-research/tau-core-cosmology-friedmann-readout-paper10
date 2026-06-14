#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1_summary.csv"
RESPONSE_SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_response_v1_summary.csv"
PROMOTION = ROOT / "data/derived/joint_numeric_t_joint_promotion_gate_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_control_suite_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_control_suite_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_control_suite_blocker_status_not_scoring_not_validation"


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
    package = read_one(PACKAGE_SUMMARY)
    promotion = read_one(PROMOTION)
    if package["status"] != "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("control-suite authorization package must be ready-not-completed")
    if promotion["verdict"] != "NUMERIC_T_JOINT_LEDGER_BUILT_PROMOTION_STILL_BLOCKED_FOR_ENDPOINT_SCORING":
        raise SystemExit("numeric T_joint promotion gate is not in expected blocked state")
    for field in [
        "control_suite_authorization_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        if package[field] != "false":
            raise SystemExit(f"unsafe package field: {field}")

    response_exists = RESPONSE_SUMMARY.exists()
    if response_exists:
        response = read_one(RESPONSE_SUMMARY)
        review_completed = response.get("review_completed", "false")
        control_suite_allowed = response.get("control_suite_authorization_allowed", "false")
        if review_completed == "true" and control_suite_allowed == "true":
            current_blocker = "control_suite_authorized_numeric_control_build_missing"
            next_action = "build_numeric_same_t_joint_control_suite_without_endpoint_scoring"
        elif review_completed == "true":
            current_blocker = "control_suite_authorization_rejected_or_incomplete"
            next_action = "keep_control_suite_blocked_or_revise_authorization_package"
        else:
            current_blocker = "control_suite_authorization_response_incomplete"
            next_action = "obtain_completed_reviewer_response_then_import_and_validate"
    else:
        review_completed = "false"
        control_suite_allowed = "false"
        current_blocker = "control_suite_authorization_response_missing"
        next_action = "send_zip_to_reviewer_then_import_completed_response"

    row = {
        "status_id": "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_BLOCKER_STATUS_V1",
        "status": "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_BLOCKED_NOT_SCORING_NOT_VALIDATION",
        "authorization_package_status": package["status"],
        "authorization_response_exists": str(response_exists).lower(),
        "review_completed": review_completed,
        "control_suite_authorization_allowed": control_suite_allowed,
        "frozen_numeric_t_joint": package["frozen_numeric_t_joint"],
        "current_blocker": current_blocker,
        "next_required_action": next_action,
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, [row])
    write_csv(
        SUMMARY,
        [
            {
                "status_id": row["status_id"],
                "status": row["status"],
                "authorization_response_exists": row["authorization_response_exists"],
                "review_completed": row["review_completed"],
                "control_suite_authorization_allowed": row["control_suite_authorization_allowed"],
                "frozen_numeric_t_joint": row["frozen_numeric_t_joint"],
                "current_blocker": row["current_blocker"],
                "next_required_action": row["next_required_action"],
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "verdict": (
                    "control_suite_blocked_waiting_for_reviewer_response"
                    if not response_exists
                    else (
                        "control_suite_authorized_waiting_for_numeric_control_build"
                        if control_suite_allowed == "true"
                        else "control_suite_response_present_requires_followup"
                    )
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint control-suite blocker status v1",
                "",
                "**Doc class:** blocker ledger",
                "**Status:** blocked; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                f"Frozen numeric `T_joint`: `{row['frozen_numeric_t_joint']}`.",
                f"Current blocker: `{row['current_blocker']}`.",
                f"Next required action: `{row['next_required_action']}`.",
                "",
                "No endpoint scoring, cosmological validation, or physical validation",
                "is authorized by this artifact.",
                "",
            ]
        )
    )
    print(f"JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_BLOCKER_STATUS_V1_BUILT blocker={current_blocker}")


if __name__ == "__main__":
    main()

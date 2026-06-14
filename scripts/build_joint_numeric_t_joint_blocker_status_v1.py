#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_authorization_package_v1_summary.csv"
RESPONSE_SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_authorization_response_v1_summary.csv"
TJOINT_LEDGER = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_blocker_status_not_endpoint_scoring_not_validation"


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
    if package["status"] != "JOINT_NUMERIC_T_JOINT_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("numeric T_joint authorization package must be ready-not-completed")
    for field in [
        "numeric_t_joint_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        if package[field] != "false":
            raise SystemExit(f"unsafe package field: {field}")

    response_exists = RESPONSE_SUMMARY.exists()
    ledger_exists = TJOINT_LEDGER.exists()
    if response_exists:
        response = read_one(RESPONSE_SUMMARY)
        review_completed = response.get("review_completed", "false")
        numeric_t_joint_allowed = response.get("numeric_t_joint_allowed", "false")
        if review_completed == "true" and numeric_t_joint_allowed == "true" and ledger_exists:
            current_blocker = "numeric_t_joint_ledger_built_endpoint_scoring_authorization_missing"
            next_action = "prepare_separate_endpoint_scoring_or_validation_authorization_before_any_claim"
        elif review_completed == "true" and numeric_t_joint_allowed == "true":
            current_blocker = "numeric_t_joint_authorized_but_not_run"
            next_action = "run_numeric_t_joint_ledger_only_after_separate_script_and_validation_guard"
        else:
            current_blocker = "numeric_t_joint_authorization_rejected_or_incomplete"
            next_action = "keep_numeric_t_joint_blocked_or_revise_authorization_package"
    else:
        review_completed = "false"
        numeric_t_joint_allowed = "false"
        current_blocker = "numeric_t_joint_authorization_response_missing"
        next_action = "obtain_completed_reviewer_response_then_import_and_validate"

    row = {
        "status_id": "JOINT_NUMERIC_T_JOINT_BLOCKER_STATUS_V1",
        "status": "JOINT_NUMERIC_T_JOINT_BLOCKED_NOT_ENDPOINT_SCORING_NOT_VALIDATION",
        "authorization_package_status": package["status"],
        "authorization_response_exists": str(response_exists).lower(),
        "numeric_t_joint_ledger_exists": str(ledger_exists).lower(),
        "review_completed": review_completed,
        "numeric_t_joint_allowed": numeric_t_joint_allowed,
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
                "numeric_t_joint_ledger_exists": row["numeric_t_joint_ledger_exists"],
                "review_completed": row["review_completed"],
                "numeric_t_joint_allowed": row["numeric_t_joint_allowed"],
                "current_blocker": row["current_blocker"],
                "next_required_action": row["next_required_action"],
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "verdict": "numeric_t_joint_blocked_waiting_for_reviewer_response"
                if not response_exists
                else (
                    "numeric_t_joint_ledger_built_waiting_for_endpoint_authorization"
                    if ledger_exists and numeric_t_joint_allowed == "true"
                    else "numeric_t_joint_response_present_requires_followup"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint blocker status v1",
                "",
                "**Doc class:** blocker ledger",
                "**Status:** blocked; not endpoint scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                f"Current blocker: `{row['current_blocker']}`.",
                f"Next required action: `{row['next_required_action']}`.",
                "",
                "No endpoint scoring, cosmological validation, or physical validation",
                "is authorized by this artifact.",
                "",
            ]
        )
    )
    print(f"JOINT_NUMERIC_T_JOINT_BLOCKER_STATUS_V1_BUILT blocker={current_blocker}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_package_v1_summary.csv"
RESPONSE_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_response_v1_summary.csv"
LEDGER_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_zi_distribution_build_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_build_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_zi_distribution_build_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_numeric_zi_distribution_build_blocker_status_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def read_ledger_aggregate(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    matches = [row for row in rows if row.get("channel_id") == "all_channels"]
    if len(matches) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one all_channels row")
    return matches[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    package = read_one(PACKAGE_SUMMARY)
    if package["status"] != "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("numeric z_i authorization package must be ready-not-completed")
    if package["review_completed"] != "false":
        raise SystemExit("package summary unexpectedly says review completed")
    for field in [
        "numeric_zi_build_allowed",
        "numeric_t_joint_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        if package[field] != "false":
            raise SystemExit(f"unsafe package field: {field}")

    response_exists = RESPONSE_SUMMARY.exists()
    ledger_exists = LEDGER_SUMMARY.exists()
    if response_exists:
        response = read_one(RESPONSE_SUMMARY)
        review_completed = response.get("review_completed", "false")
        numeric_zi_allowed = response.get("numeric_zi_build_allowed", "false")
        if review_completed == "true" and numeric_zi_allowed == "true" and ledger_exists:
            ledger = read_ledger_aggregate(LEDGER_SUMMARY)
            if ledger["numeric_z_i_defined"] != "true":
                raise SystemExit("ledger summary exists but numeric z_i is not fully defined")
            current_blocker = "numeric_zi_distribution_ledger_built_numeric_t_joint_authorization_missing"
            next_action = "prepare_separate_numeric_t_joint_authorization_package_before_any_joint_scoring"
        elif review_completed == "true" and numeric_zi_allowed == "true":
            current_blocker = "numeric_zi_distribution_build_authorized_but_not_run"
            next_action = "run_numeric_zi_distribution_build_only_after_separate_script_and_validation_guard"
        else:
            current_blocker = "numeric_zi_distribution_build_authorization_rejected_or_incomplete"
            next_action = "keep_numeric_zi_build_blocked_or_revise_authorization_package"
    else:
        review_completed = "false"
        numeric_zi_allowed = "false"
        current_blocker = "numeric_zi_distribution_build_authorization_response_missing"
        next_action = "obtain_completed_reviewer_response_then_import_and_validate"

    row = {
        "status_id": "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_BLOCKER_STATUS_V1",
        "status": "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_BLOCKED_NOT_SCORING_NOT_VALIDATION",
        "authorization_package_status": package["status"],
        "authorization_response_exists": str(response_exists).lower(),
        "numeric_zi_distribution_ledger_exists": str(ledger_exists).lower(),
        "review_completed": review_completed,
        "numeric_zi_build_allowed": numeric_zi_allowed,
        "numeric_t_joint_allowed": "false",
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
                "numeric_zi_distribution_ledger_exists": row["numeric_zi_distribution_ledger_exists"],
                "review_completed": row["review_completed"],
                "numeric_zi_build_allowed": row["numeric_zi_build_allowed"],
                "numeric_t_joint_allowed": row["numeric_t_joint_allowed"],
                "current_blocker": row["current_blocker"],
                "next_required_action": row["next_required_action"],
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "verdict": "numeric_zi_distribution_build_blocked_waiting_for_reviewer_response"
                if not response_exists
                else (
                    "numeric_zi_distribution_ledger_built_waiting_for_t_joint_authorization"
                    if ledger_exists and numeric_zi_allowed == "true"
                    else "numeric_zi_distribution_build_response_present_requires_followup"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric z_i distribution build blocker status v1",
                "",
                "**Doc class:** blocker ledger",
                "**Status:** blocked; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This ledger records whether the numeric channel-level `z_i`",
                "distribution build is authorized. At this stage, the authorization",
                "package is ready but no completed reviewer response is present.",
                "",
                f"Current blocker: `{row['current_blocker']}`.",
                f"Next required action: `{row['next_required_action']}`.",
                "",
                "No `z_i`, `T_joint`, endpoint scoring, cosmological validation, or",
                "physical validation is authorized by this artifact.",
                "",
            ]
        )
    )
    print(f"JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_BLOCKER_STATUS_V1_BUILT blocker={current_blocker}")


if __name__ == "__main__":
    main()

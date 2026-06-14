#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_same_statistic_execution_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_same_statistic_execution_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_same_statistic_execution_blocker_status_v1.md"
PERM_SUMMARY = ROOT / "data/derived/joint_same_statistic_guarded_permission_replay_package_v1_summary.csv"
AUTH_PACKAGE = ROOT / "data/derived/joint_same_statistic_execution_authorization_package_v1_summary.csv"
AUTH_RESPONSE = ROOT / "data/derived/joint_same_statistic_execution_authorization_response_v1_summary.csv"
REPLAY_SUMMARY = ROOT / "data/derived/joint_guarded_replay_permission_only_summary_v1.csv"
CLAIM_BOUNDARY = "joint_same_statistic_execution_blocker_status_not_execution_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
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
    perm = read_one(PERM_SUMMARY)
    package = read_one(AUTH_PACKAGE)
    if perm["status"] != "JOINT_SAME_STATISTIC_GUARDED_PERMISSION_REPLAY_PACKAGE_READY_NOT_EXECUTED":
        raise SystemExit("same-statistic permission package is not ready-not-executed")
    if package["status"] != "JOINT_SAME_STATISTIC_EXECUTION_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("same-statistic execution authorization package is not ready-not-completed")
    for row, label in [(perm, "permission_package"), (package, "execution_authorization_package")]:
        for field in [
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
            "contains_endpoint_residuals",
            "contains_new_endpoint_scores",
            "contains_fit_statistics",
        ]:
            if row[field] != "false":
                raise SystemExit(f"{label}: unsafe field {field}")

    response_exists = AUTH_RESPONSE.exists()
    response_decision = "missing"
    permission_only_execution_allowed = "false"
    current_blocker = "same_statistic_execution_authorization_response_missing"
    next_action = "obtain_completed_execution_reviewer_response_then_import_and_validate"
    replay_exists = "true" if REPLAY_SUMMARY.exists() else "false"

    if response_exists:
        response = read_one(AUTH_RESPONSE)
        response_decision = response["decision"]
        permission_only_execution_allowed = response["permission_only_execution_allowed"]
        if response_decision == "AUTHORIZE_SAME_STATISTIC_PERMISSION_ONLY_EXECUTION_NOT_VALIDATION":
            current_blocker = "same_statistic_execution_authorized_but_replay_not_run"
            next_action = "run_permission_only_replay_once_and_validate_outputs"
            if REPLAY_SUMMARY.exists():
                replay = read_one(REPLAY_SUMMARY)
                if replay.get("status") == "JOINT_GUARDED_REPLAY_PERMISSION_ONLY_COMPLETE_NOT_VALIDATION":
                    current_blocker = "permission_only_replay_completed_not_validation"
                    next_action = "preserve_outputs_and_do_not_promote_without_separate_validation_protocol"
        else:
            current_blocker = "same_statistic_execution_authorization_rejected_or_not_accepted"
            next_action = "keep_replay_blocked_or_revise_authorization_package"

    row = {
        "run_id": "JOINT_SAME_STATISTIC_EXECUTION_BLOCKER_STATUS_V1",
        "status": "JOINT_SAME_STATISTIC_EXECUTION_BLOCKED_NOT_SCORING_NOT_VALIDATION",
        "same_statistic_permission_package_status": perm["status"],
        "execution_authorization_package_status": package["status"],
        "execution_authorization_response_exists": "true" if response_exists else "false",
        "execution_authorization_decision": response_decision,
        "permission_only_execution_allowed": permission_only_execution_allowed,
        "permission_only_replay_summary_exists": replay_exists,
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
                "run_id": row["run_id"],
                "status": row["status"],
                "execution_authorization_response_exists": row["execution_authorization_response_exists"],
                "permission_only_execution_allowed": row["permission_only_execution_allowed"],
                "current_blocker": row["current_blocker"],
                "next_required_action": row["next_required_action"],
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "verdict": "same_statistic_permission_only_replay_complete_not_validation"
                if row["current_blocker"] == "permission_only_replay_completed_not_validation"
                else "same_statistic_execution_blocked_until_completed_authorization_response",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint same-statistic execution blocker status v1",
                "",
                "This ledger records the current blocker for the same-statistic execution path.",
                "It is not a replay, not endpoint scoring, not cosmological validation,",
                "and not physical validation.",
                "",
                f"Current blocker: `{row['current_blocker']}`.",
                f"Next required action: `{row['next_required_action']}`.",
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )
    print(f"JOINT_SAME_STATISTIC_EXECUTION_BLOCKER_STATUS_V1_BUILT blocker={current_blocker}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_guarded_replay_execution_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_execution_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_guarded_replay_execution_blocker_status_v1.md"
RUN_TEMPLATE_SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_v1_summary.csv"
AUTH_PACKAGE_SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1_summary.csv"
AUTH_RESPONSE_SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_response_v1_summary.csv"
EXECUTION_PLAN_SUMMARY = ROOT / "data/derived/joint_guarded_replay_execution_plan_v1_summary.csv"
EXECUTION_AUTH_RESPONSE = ROOT / "data/derived/joint_guarded_replay_execution_authorization_response_v1_summary.csv"
CLAIM_BOUNDARY = "joint_guarded_replay_execution_blocker_status_not_execution_not_scoring_not_validation"


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
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    run_template = read_one(RUN_TEMPLATE_SUMMARY)
    auth_package = read_one(AUTH_PACKAGE_SUMMARY)
    if run_template["status"] != "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_READY_NOT_EXECUTED":
        raise SystemExit("run-template must be frozen and not executed")
    if auth_package["status"] != "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("authorization package must be ready-not-completed")
    for row, label in [(run_template, "run_template"), (auth_package, "authorization_package")]:
        for key in [
            "direct_execution_allowed",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"{label}: unsafe field {key}")

    response_exists = AUTH_RESPONSE_SUMMARY.exists()
    response_decision = "missing"
    response_status = "missing"
    response_allows_next = "false"
    execution_response_exists = "false"
    blocker = "completed_run_template_authorization_response_missing"
    next_action = "obtain_completed_external_reviewer_response_then_import_and_validate"

    if response_exists:
        response = read_one(AUTH_RESPONSE_SUMMARY)
        response_decision = response["decision"]
        response_status = response["response_status"]
        response_allows_next = response["template_authorized_for_later_permission_replay"]
        if response_decision == "AUTHORIZE_JOINT_GUARDED_REPLAY_EXECUTION_PLAN_PREPARATION_ONLY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION":
            blocker = "execution_plan_builder_not_yet_prepared"
            next_action = "build_separate_executable_replay_plan_and_validator_without_running"
            if EXECUTION_PLAN_SUMMARY.exists():
                plan = read_one(EXECUTION_PLAN_SUMMARY)
                if plan["status"] == "JOINT_GUARDED_REPLAY_EXECUTION_PLAN_READY_NOT_RUN":
                    blocker = "guarded_runner_and_execution_authorization_not_yet_prepared"
                    next_action = "build_guarded_permission_only_runner_and_validator_then_get_separate_execution_authorization"
                    if plan["runner_exists"] == "true":
                        blocker = "execution_authorization_response_missing"
                        next_action = "obtain_completed_external_execution_authorization_response_then_import_and_validate"
                    if EXECUTION_AUTH_RESPONSE.exists():
                        execution_response_exists = "true"
                        exec_auth = read_one(EXECUTION_AUTH_RESPONSE)
                        if exec_auth.get("decision") == "AUTHORIZE_JOINT_GUARDED_REPLAY_PERMISSION_ONLY_EXECUTION_NOT_VALIDATION":
                            blocker = "execution_authorized_but_runner_not_yet_run"
                            next_action = "run_guarded_permission_only_replay_once_and_validate_outputs"
        elif response_decision == "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_REJECTED_NOT_EXECUTION_NOT_SCORING":
            blocker = "reviewer_rejected_run_template_authorization"
            next_action = "revise_template_or_keep_joint_guarded_replay_blocked"

    row = {
        "run_id": "JOINT_GUARDED_REPLAY_EXECUTION_BLOCKER_STATUS_V1",
        "status": "JOINT_GUARDED_REPLAY_EXECUTION_BLOCKED_NOT_SCORING_NOT_VALIDATION",
        "run_template_status": run_template["status"],
        "authorization_package_status": auth_package["status"],
        "authorization_response_exists": "true" if response_exists else "false",
        "execution_authorization_response_exists": execution_response_exists,
        "authorization_response_decision": response_decision,
        "authorization_response_status": response_status,
        "template_authorized_for_later_permission_replay": response_allows_next,
        "current_blocker": blocker,
        "next_required_action": next_action,
        "direct_execution_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, [row])
    write_csv(
        SUMMARY,
        [
            {
                "run_id": row["run_id"],
                "status": row["status"],
                "authorization_response_exists": row["authorization_response_exists"],
                "execution_authorization_response_exists": row["execution_authorization_response_exists"],
                "current_blocker": row["current_blocker"],
                "next_required_action": row["next_required_action"],
                "direct_execution_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "verdict": "joint_guarded_replay_execution_blocked_until_completed_authorization_response",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint guarded replay execution blocker status v1",
                "",
                "This ledger records the current execution blocker for the joint guarded replay path.",
                "It is not a replay, not endpoint scoring, and not cosmological validation.",
                "",
                f"Current blocker: `{row['current_blocker']}`.",
                f"Next required action: `{row['next_required_action']}`.",
                "",
                "The replay remains blocked unless a completed external reviewer response is imported",
                "and validates the execution authorization gate.",
                "",
                f"Claim boundary: `{CLAIM_BOUNDARY}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_GUARDED_REPLAY_EXECUTION_BLOCKER_STATUS_V1_BUILT "
        f"blocker={row['current_blocker']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1_summary.csv"
RUN_TEMPLATE_SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_v1_summary.csv"
PACKAGE_ID = "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_guarded_replay_run_template_authorization_not_execution_not_scoring_not_validation"

EXPECTED_RESPONSES = {
    "JGRT_Q1_TEMPLATE_SCOPE": {
        "authorize_template_for_separate_permission_only_replay",
        "reject",
    },
    "JGRT_Q2_IDENTICAL_STATISTIC": {
        "accept_identical_statistic_and_weights",
        "reject",
    },
    "JGRT_Q3_COVARIANCE_CAVEATS": {
        "accept_caveated_block_diagonal_conditions",
        "reject",
    },
    "JGRT_Q4_NO_VALIDATION_CLAIM": {
        "accept_permission_only_no_validation",
        "reject",
    },
}
ACCEPTED = {
    "JGRT_Q1_TEMPLATE_SCOPE": "authorize_template_for_separate_permission_only_replay",
    "JGRT_Q2_IDENTICAL_STATISTIC": "accept_identical_statistic_and_weights",
    "JGRT_Q3_COVARIANCE_CAVEATS": "accept_caveated_block_diagonal_conditions",
    "JGRT_Q4_NO_VALIDATION_CLAIM": "accept_permission_only_no_validation",
}
FORBIDDEN_INPUTS = {
    "endpoint_residuals",
    "new_endpoint_scores",
    "fit_improvements",
    "posterior_chains",
    "post_score_control_ranks",
    "posthoc_channel_selection",
    "posthoc_block_weight_tuning",
    "posthoc_covariance_reweighting",
    "cosmological_validation_claims",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed joint guarded run-template authorization response."
    )
    parser.add_argument("response", nargs="?", default=str(DEFAULT_RESPONSE))
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY))
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path


def rel_or_abs(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {rel_or_abs(path)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{rel_or_abs(path)} must contain exactly one row")
    return rows[0]


def write_one(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value: str) -> str:
    return value.strip().lower()


def is_false(value: str) -> bool:
    return norm(value) == "false"


def is_true(value: str) -> bool:
    return norm(value) == "true"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response)
    summary_out = resolve(args.summary_out)
    package = read_one(PACKAGE_SUMMARY)
    run_template = read_one(RUN_TEMPLATE_SUMMARY)
    rows = read_rows(response_path)

    require(
        package["status"] == "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
        "unexpected package status",
    )
    require(package["review_completed"] == "false", "upstream package must be uncompleted handoff")
    require(package["template_authorized_for_later_permission_replay"] == "false", "upstream package cannot pre-authorize")
    require(package["separate_execution_step_required"] == "true", "separate execution step must remain required")
    require(run_template["status"] == "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_READY_NOT_EXECUTED", "run-template dependency not frozen")
    for field in [
        "direct_execution_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "contains_endpoint_residuals",
        "contains_new_endpoint_scores",
        "contains_fit_statistics",
    ]:
        require(is_false(package[field]), f"upstream package unsafe field: {field}")

    require(len(rows) == len(EXPECTED_RESPONSES), "response must contain four rows")
    require({row["question_id"] for row in rows} == set(EXPECTED_RESPONSES), "question ids mismatch")

    completed_count = 0
    accepted_count = 0
    rejected_count = 0
    forbidden_used = False
    response_values: dict[str, str] = {}
    template_authorized_rows = 0

    for row in rows:
        qid = row["question_id"]
        require(row["review_id"] == PACKAGE_ID, f"{qid}: bad review_id")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{qid}: claim boundary mismatch")
        require(set(row["forbidden_inputs"].split(";")) == FORBIDDEN_INPUTS, f"{qid}: forbidden input list mismatch")
        for field in [
            "direct_execution_allowed",
            "direct_execution_allowed_by_this_package",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ]:
            require(is_false(row[field]), f"{qid}: unsafe field {field}")
        require(is_true(row["separate_execution_step_required"]), f"{qid}: separate execution step must remain required")
        if is_true(row["forbidden_inputs_used"]):
            forbidden_used = True
        if is_true(row["template_authorized_for_later_permission_replay"]):
            template_authorized_rows += 1

        completed = is_true(row["review_completed"])
        value = norm(row["reviewer_response"])
        response_values[qid] = value
        if completed:
            completed_count += 1
            require(value in EXPECTED_RESPONSES[qid], f"{qid}: unsupported reviewer_response {value}")
            require(row["reviewer_id_or_role"].strip(), f"{qid}: reviewer id/role required")
            require(row["reviewer_rationale"].strip(), f"{qid}: reviewer rationale required")
            if value == "reject":
                rejected_count += 1
            else:
                accepted_count += 1
        else:
            require(value == "", f"{qid}: incomplete response must leave reviewer_response blank")
            require(row["reviewer_id_or_role"].strip() == "", f"{qid}: incomplete response must leave reviewer id blank")
            require(row["reviewer_rationale"].strip() == "", f"{qid}: incomplete response must leave rationale blank")
            require(
                is_false(row["template_authorized_for_later_permission_replay"]),
                f"{qid}: incomplete response cannot authorize template",
            )

    require(completed_count in {0, len(EXPECTED_RESPONSES)}, "response must be blank or fully completed")
    require(not forbidden_used, "refusing response with forbidden_inputs_used=true")

    if completed_count == 0:
        decision = "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_RESPONSE_TEMPLATE_READY_NOT_COMPLETED"
        response_status = "not_completed"
        template_authorized = "false"
        next_action = "send_package_to_reviewer"
    elif rejected_count:
        decision = "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_REJECTED_NOT_EXECUTION_NOT_SCORING"
        response_status = "rejected"
        template_authorized = "false"
        next_action = "keep_joint_guarded_replay_blocked_or_revise_template"
    else:
        for qid, accepted_value in ACCEPTED.items():
            require(response_values[qid] == accepted_value, f"{qid}: required accepted response not present")
        require(template_authorized_rows == len(EXPECTED_RESPONSES), "all accepted rows must authorize template for later permission replay")
        decision = "AUTHORIZE_JOINT_GUARDED_REPLAY_EXECUTION_PLAN_PREPARATION_ONLY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION"
        response_status = "completed_template_authorization_for_later_permission_replay_plan"
        template_authorized = "true"
        next_action = "build_separate_executable_replay_plan_and_validator_before_any_run"

    summary = {
        "run_id": "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "completed_response_rows": str(completed_count),
        "accepted_rows": str(accepted_count),
        "rejected_rows": str(rejected_count),
        "forbidden_inputs_used": "false",
        "template_authorized_for_later_permission_replay": template_authorized,
        "direct_execution_allowed": "false",
        "separate_execution_step_required": "true",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "decision": decision,
        "response_status": response_status,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(
        "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_RESPONSE_V1_VALIDATED "
        f"decision={decision}"
    )


if __name__ == "__main__":
    main()

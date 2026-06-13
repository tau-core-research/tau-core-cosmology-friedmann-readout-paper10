#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_guarded_permission_replay_authorization_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_guarded_permission_replay_authorization_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1_summary.csv"
DOC = ROOT / "docs/joint_guarded_permission_replay_authorization_package_v1.md"
PACKAGE_ID = "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_guarded_permission_replay_authorization_not_scoring_not_validation"

EXPECTED_QUESTIONS = {
    "JGPR_Q1_PERMISSION_SCOPE": {
        "authorize_guarded_replay_package",
        "authorize_guarded_replay_package_preparation_only",
        "reject",
    },
    "JGPR_Q2_SAME_STATISTIC": {
        "accept_same_statistic_binding",
        "accept_same_frozen_block_diagonal_statistic_and_block_weights_required",
        "reject",
    },
    "JGPR_Q3_CAVEATS": {
        "accept_caveats",
        "accept_caveats_must_remain_attached",
        "reject",
    },
    "JGPR_Q4_NEXT_ACTION": {
        "accept_run_template_first",
        "accept_guarded_run_template_first_no_direct_execution",
        "reject",
    },
}
ACCEPTED_Q1 = {
    "authorize_guarded_replay_package",
    "authorize_guarded_replay_package_preparation_only",
}
ACCEPTED_Q2 = {
    "accept_same_statistic_binding",
    "accept_same_frozen_block_diagonal_statistic_and_block_weights_required",
}
ACCEPTED_Q3 = {"accept_caveats", "accept_caveats_must_remain_attached"}
ACCEPTED_Q4 = {"accept_run_template_first", "accept_guarded_run_template_first_no_direct_execution"}
FORBIDDEN_INPUTS = {
    "endpoint_residuals",
    "new_endpoint_scores",
    "fit_improvements",
    "posterior_chains",
    "post_score_control_ranks",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed guarded permission replay authorization response."
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

    package_summary = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)
    require(DOC.exists(), f"missing {DOC.relative_to(ROOT)}")
    require(
        package_summary["status"] == "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
        "unexpected package status",
    )
    for field in [
        "review_completed",
        "guarded_replay_package_authorized",
        "direct_execution_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "contains_endpoint_residuals",
        "contains_new_endpoint_scores",
        "contains_fit_statistics",
    ]:
        require(is_false(package_summary[field]), f"upstream package unsafe field: {field}")
    require(package_summary["separate_run_template_required"] == "true", "upstream package must require a separate run template")
    require(len(rows) == len(EXPECTED_QUESTIONS), "response must contain four rows")
    require({row["question_id"] for row in rows} == set(EXPECTED_QUESTIONS), "question ids mismatch")

    completed_flags: list[bool] = []
    accepted_rows = 0
    rejected_rows = 0
    guarded_rows = 0
    separate_template_rows = 0
    forbidden_used = False
    responses: dict[str, str] = {}

    for row in rows:
        qid = row["question_id"]
        require(row["review_id"] == PACKAGE_ID, f"{qid}: bad review_id")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{qid}: claim boundary mismatch")
        require(set(row["forbidden_inputs"].split(";")) == FORBIDDEN_INPUTS, f"{qid}: forbidden input list mismatch")
        for field in [
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "direct_execution_allowed",
        ]:
            require(is_false(row[field]), f"{qid}: unsafe field {field}")
        require(is_true(row["separate_run_template_required"]), f"{qid}: separate run template must remain required")

        completed = is_true(row["review_completed"])
        completed_flags.append(completed)
        value = norm(row["reviewer_response"])
        responses[qid] = value
        if is_true(row["forbidden_inputs_used"]):
            forbidden_used = True
        if is_true(row["guarded_replay_package_authorized"]):
            guarded_rows += 1
        if is_true(row["separate_run_template_required"]):
            separate_template_rows += 1
        if completed:
            require(value in EXPECTED_QUESTIONS[qid], f"{qid}: unsupported reviewer_response {value}")
            require(row["reviewer_id_or_role"].strip(), f"{qid}: reviewer id/role required")
            require(row["reviewer_rationale"].strip(), f"{qid}: reviewer rationale required")
            if value == "reject":
                rejected_rows += 1
            else:
                accepted_rows += 1
        else:
            require(value == "", f"{qid}: incomplete response must leave reviewer_response blank")
            require(row["reviewer_id_or_role"].strip() == "", f"{qid}: incomplete response must leave reviewer id blank")
            require(row["reviewer_rationale"].strip() == "", f"{qid}: incomplete response must leave rationale blank")
            require(is_false(row["guarded_replay_package_authorized"]), f"{qid}: incomplete response cannot authorize package")

    completed_count = sum(completed_flags)
    require(completed_count in {0, len(EXPECTED_QUESTIONS)}, "response must be either blank or fully completed")
    require(not forbidden_used, "refusing response with forbidden_inputs_used=true")

    if completed_count == 0:
        decision = "JOINT_GUARDED_PERMISSION_REPLAY_RESPONSE_TEMPLATE_READY_NOT_COMPLETED"
        response_status = "not_completed"
        guarded_package_authorized = "false"
        next_action = "send_package_to_reviewer"
    elif rejected_rows:
        decision = "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_REJECTED_NOT_SCORING"
        response_status = "rejected"
        guarded_package_authorized = "false"
        next_action = "keep_joint_replay_blocked_or_revise_guarded_package"
    else:
        require(guarded_rows == len(EXPECTED_QUESTIONS), "all completed rows must authorize guarded package preparation")
        require(separate_template_rows == len(EXPECTED_QUESTIONS), "all rows must require separate run template")
        require(responses["JGPR_Q1_PERMISSION_SCOPE"] in ACCEPTED_Q1, "Q1 must authorize guarded package preparation")
        require(responses["JGPR_Q2_SAME_STATISTIC"] in ACCEPTED_Q2, "Q2 must bind same statistic and weights")
        require(responses["JGPR_Q3_CAVEATS"] in ACCEPTED_Q3, "Q3 must keep caveats attached")
        require(responses["JGPR_Q4_NEXT_ACTION"] in ACCEPTED_Q4, "Q4 must require run template first")
        decision = "AUTHORIZE_GUARDED_PERMISSION_REPLAY_PACKAGE_PREPARATION_ONLY_NOT_EXECUTION_NOT_SCORING_NOT_VALIDATION"
        response_status = "completed_permission_only_package_preparation_authorization"
        guarded_package_authorized = "true"
        next_action = "build_separate_guarded_replay_run_template_and_validator_before_any_executable_replay"

    doc_text = DOC.read_text()
    for marker in ["not scoring", "guarded", "same block-diagonal statistic", CLAIM_BOUNDARY]:
        require(marker in doc_text, f"doc missing marker: {marker}")

    summary = {
        "run_id": "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "completed_response_rows": str(completed_count),
        "accepted_rows": str(accepted_rows),
        "rejected_rows": str(rejected_rows),
        "forbidden_inputs_used": "false",
        "guarded_replay_package_authorized": guarded_package_authorized,
        "direct_execution_allowed": "false",
        "separate_run_template_required": "true",
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
        "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_RESPONSE_V1_VALIDATED "
        f"decision={decision}"
    )


if __name__ == "__main__":
    main()

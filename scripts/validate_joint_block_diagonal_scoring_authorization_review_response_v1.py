#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_block_diagonal_scoring_authorization_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_block_diagonal_scoring_authorization_review_package_v1.md"
PACKAGE_ID = "JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_block_diagonal_scoring_authorization_review_not_scoring_not_validation"

EXPECTED_QUESTIONS = {
    "BDSA_Q1_CAVEATED_PRECONDITION": {"accept", "reject"},
    "BDSA_Q2_CAVEATS": {"accept_with_caveats", "reject"},
    "BDSA_Q3_SAME_STATISTIC_CONTROLS": {"accept_protocol_authorization", "reject"},
    "BDSA_Q4_NEXT_ACTION": {"accept", "reject"},
}
FORBIDDEN_INPUTS = {
    "endpoint_residuals",
    "new_endpoint_scores",
    "fit_improvements",
    "posterior_chains",
    "post_score_control_ranks",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed joint block-diagonal scoring authorization review response."
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
        package_summary["status"] == "JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_REVIEW_PACKAGE_READY_NOT_COMPLETED",
        "unexpected package status",
    )
    for field in [
        "review_completed",
        "permission_only_replay_authorization_allowed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "contains_endpoint_residuals",
        "contains_new_endpoint_scores",
        "contains_fit_statistics",
    ]:
        require(is_false(package_summary[field]), f"upstream package unsafe field: {field}")
    require(len(rows) == len(EXPECTED_QUESTIONS), "response must contain four rows")
    require({row["question_id"] for row in rows} == set(EXPECTED_QUESTIONS), "question ids mismatch")

    completed_flags: list[bool] = []
    accepted_rows = 0
    permission_rows = 0
    separate_replay_rows = 0
    reject_count = 0
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
        ]:
            require(is_false(row[field]), f"{qid}: unsafe field {field}")
        require(is_true(row["separate_replay_package_required"]), f"{qid}: separate replay package must remain required")

        completed = is_true(row["review_completed"])
        completed_flags.append(completed)
        value = norm(row["reviewer_response"])
        responses[qid] = value
        if is_true(row["forbidden_inputs_used"]):
            forbidden_used = True
        if is_true(row["permission_only_replay_authorization_allowed"]):
            permission_rows += 1
        if is_true(row["separate_replay_package_required"]):
            separate_replay_rows += 1
        if completed:
            require(value in EXPECTED_QUESTIONS[qid], f"{qid}: unsupported reviewer_response {value}")
            require(row["reviewer_id_or_role"].strip(), f"{qid}: reviewer id/role required")
            require(row["reviewer_rationale"].strip(), f"{qid}: reviewer rationale required")
            if value == "reject":
                reject_count += 1
            else:
                accepted_rows += 1
        else:
            require(value == "", f"{qid}: incomplete response must leave reviewer_response blank")
            require(row["reviewer_id_or_role"].strip() == "", f"{qid}: incomplete response must leave reviewer id blank")
            require(row["reviewer_rationale"].strip() == "", f"{qid}: incomplete response must leave rationale blank")
            require(is_false(row["permission_only_replay_authorization_allowed"]), f"{qid}: incomplete response cannot authorize replay")

    completed_count = sum(completed_flags)
    require(completed_count in {0, len(EXPECTED_QUESTIONS)}, "response must be either blank or fully completed")
    require(not forbidden_used, "refusing response with forbidden_inputs_used=true")

    if completed_count == 0:
        decision = "JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_RESPONSE_TEMPLATE_READY_NOT_COMPLETED"
        response_status = "not_completed"
        next_action = "send_package_to_reviewer"
        permission_allowed = "false"
        same_statistic_controls_required = "false"
        direct_scoring_allowed = "false"
    elif reject_count:
        decision = "JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_REJECTED_NOT_SCORING"
        response_status = "rejected"
        next_action = "revise_scoring_authorization_or_keep_joint_scoring_blocked"
        permission_allowed = "false"
        same_statistic_controls_required = "false"
        direct_scoring_allowed = "false"
    else:
        require(permission_rows == len(EXPECTED_QUESTIONS), "all completed rows must allow permission-only replay authorization")
        require(separate_replay_rows == len(EXPECTED_QUESTIONS), "all completed rows must require a separate replay package")
        require(responses["BDSA_Q2_CAVEATS"] == "accept_with_caveats", "caveat row must accept with caveats")
        require(
            responses["BDSA_Q3_SAME_STATISTIC_CONTROLS"] == "accept_protocol_authorization",
            "same-statistic controls row must authorize protocol only",
        )
        decision = "AUTHORIZE_SEPARATE_GUARDED_JOINT_PERMISSION_REPLAY_PACKAGE_NOT_SCORING_NOT_VALIDATION"
        response_status = "completed_permission_only_authorization"
        next_action = "build_separate_guarded_permission_only_joint_replay_authorization_package_with_same_statistic_covariance_and_controls"
        permission_allowed = "true"
        same_statistic_controls_required = "true"
        direct_scoring_allowed = "false"

    doc_text = DOC.read_text()
    for marker in ["not scoring", "permission-only", "caveats", CLAIM_BOUNDARY]:
        require(marker in doc_text, f"doc missing marker: {marker}")

    summary = {
        "run_id": "JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_REVIEW_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "completed_response_rows": str(completed_count),
        "accepted_rows": str(accepted_rows),
        "permission_only_replay_authorization_allowed_rows": str(permission_rows),
        "separate_replay_package_required_rows": str(separate_replay_rows),
        "forbidden_inputs_used": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "cross_probe_covariance_product_available": "false",
        "block_diagonal_independence_precondition_closed": "true" if permission_allowed == "true" else "false",
        "same_statistic_controls_required": same_statistic_controls_required,
        "direct_scoring_allowed": direct_scoring_allowed,
        "decision": decision,
        "response_status": response_status,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(
        "JOINT_BLOCK_DIAGONAL_SCORING_AUTHORIZATION_REVIEW_RESPONSE_V1_VALIDATED "
        f"decision={decision}"
    )


if __name__ == "__main__":
    main()

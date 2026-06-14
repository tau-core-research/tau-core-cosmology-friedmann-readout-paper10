#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_package_v1_summary.csv"
VALUES_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv"
PACKAGE_ID = "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_value_review_not_rescoring_not_validation"
EXPECTED_QUESTIONS = {"NPV_Q1_REPRODUCIBILITY", "NPV_Q2_CONTROL_SCOPE", "NPV_Q3_BOUNDARY"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate completed row-level numeric penalty value review response.")
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


def is_true(value: str) -> bool:
    return norm(value) == "true"


def is_false(value: str) -> bool:
    return norm(value) == "false"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response)
    summary_out = resolve(args.summary_out)
    package = read_one(PACKAGE_SUMMARY)
    values = read_one(VALUES_SUMMARY)
    rows = read_rows(response_path)

    require(package["status"] == "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_PACKAGE_READY_NOT_COMPLETED", "unexpected package status")
    require(values["verdict"] == "NUMERIC_PENALTY_VALUES_COMPUTED_NOT_RESCORING", "unexpected values verdict")
    require(len(rows) == 3, "response must contain three rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "question ids mismatch")

    accepted = 0
    completed = 0
    numeric_accept_rows = 0
    cross_channel_rows = 0
    lambda_rows = 0
    rescoring_rows = 0
    forbidden_used = False
    for row in rows:
        qid = row["question_id"]
        require(row["review_id"] == PACKAGE_ID, f"{qid}: review_id mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{qid}: claim boundary mismatch")
        require(is_false(row["endpoint_scoring_allowed"]), f"{qid}: endpoint scoring must remain false")
        require(is_false(row["endpoint_validation_claimed"]), f"{qid}: endpoint validation must remain false")
        if is_true(row["review_completed"]):
            completed += 1
        require(norm(row["reviewer_response"]) in {"accept", "reject"}, f"{qid}: reviewer_response must be accept or reject")
        require(row["reviewer_id_or_role"].strip(), f"{qid}: reviewer id required")
        require(row["reviewer_rationale"].strip(), f"{qid}: rationale required")
        if norm(row["reviewer_response"]) == "accept":
            accepted += 1
        if is_true(row["forbidden_inputs_used"]):
            forbidden_used = True
        if is_true(row["numeric_penalty_values_accepted"]):
            numeric_accept_rows += 1
        if is_true(row["cross_channel_control_alignment_authorized"]):
            cross_channel_rows += 1
        if is_true(row["lambda_row_numeric_value_authorized"]):
            lambda_rows += 1
        if is_true(row["t_joint_rescoring_authorized"]):
            rescoring_rows += 1

    require(completed == 3, "all response rows must be completed")
    require(not forbidden_used, "forbidden inputs used")
    require(cross_channel_rows == 0, "cross-channel control alignment must not be authorized here")
    require(lambda_rows == 0, "lambda_row numeric value must not be authorized here")
    require(rescoring_rows == 0, "T_joint rescoring must not be authorized here")

    if accepted == 3:
        require(numeric_accept_rows == 3, "all accepted rows must accept numeric values")
        decision = "ACCEPT_NUMERIC_PENALTY_VALUES_NOT_LAMBDA_NOT_T_JOINT_RESCORING_NOT_VALIDATION"
        response_status = "completed_numeric_penalty_value_review"
        next_action = "review_lambda_row_or_separate_rescoring_authorization_before_any_penalty_use"
        numeric_values_accepted = "true"
    else:
        decision = "NUMERIC_PENALTY_VALUES_REJECTED_NOT_RESCORING"
        response_status = "rejected_numeric_penalty_value_review"
        next_action = "revise_numeric_penalty_values_or_keep_penalty_use_blocked"
        numeric_values_accepted = "false"

    summary = {
        "run_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "completed_response_rows": str(completed),
        "accepted_rows": str(accepted),
        "numeric_penalty_values_accepted": numeric_values_accepted,
        "cross_channel_control_alignment_authorized": "false",
        "lambda_row_numeric_value_authorized": "false",
        "t_joint_rescoring_authorized": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "forbidden_inputs_used": "false",
        "candidate_P_row_reported": values["P_row_candidate"],
        "decision": decision,
        "response_status": response_status,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(f"JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_RESPONSE_VALIDATED decision={decision}")


if __name__ == "__main__":
    main()

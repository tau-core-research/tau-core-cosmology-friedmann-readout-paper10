#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_row_level_numeric_lambda_review_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1_summary.csv"
PACKAGE_ID = "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_numeric_lambda_review_not_rescoring_not_validation"
EXPECTED_QUESTIONS = {"NL_Q1_POLICY_COMPATIBILITY", "NL_Q2_NUMERIC_VALUE_AUTHORIZATION", "NL_Q3_BOUNDARY"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate completed numeric lambda review response.")
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
    rows = read_rows(response_path)

    require(package["status"] == "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_REVIEW_PACKAGE_READY_NOT_COMPLETED", "unexpected package status")
    require(len(rows) == 3, "response must contain three rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "question ids mismatch")

    accepted = 0
    completed = 0
    compatible_rows = 0
    lambda_authorized_rows = 0
    rescoring_authorized_rows = 0
    endpoint_authorized_rows = 0
    forbidden_used = False

    for row in rows:
        qid = row["question_id"]
        require(row["review_id"] == PACKAGE_ID, f"{qid}: review_id mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{qid}: claim boundary mismatch")
        require(is_false(row["endpoint_scoring_allowed"]), f"{qid}: endpoint scoring must remain false")
        require(is_false(row["endpoint_validation_claimed"]), f"{qid}: endpoint validation must remain false")
        require(is_true(row["review_completed"]), f"{qid}: response row must be completed")
        require(row["reviewer_id_or_role"].strip(), f"{qid}: reviewer id required")
        require(row["reviewer_rationale"].strip(), f"{qid}: reviewer rationale required")
        if norm(row["reviewer_response"]) in {
            "accept",
            "accept_with_caveats",
            "authorize_numeric_lambda_record_only",
        }:
            accepted += 1
        else:
            require(norm(row["reviewer_response"]) in {"reject", "no_go"}, f"{qid}: unsupported reviewer response")
        completed += 1
        if is_true(row["forbidden_inputs_used"]):
            forbidden_used = True
        if is_true(row["lambda_policy_compatible"]):
            compatible_rows += 1
        if is_true(row["lambda_row_numeric_value_authorized"]):
            lambda_authorized_rows += 1
        if is_true(row["t_joint_rescoring_authorized"]):
            rescoring_authorized_rows += 1
        if is_true(row["endpoint_scoring_authorized"]):
            endpoint_authorized_rows += 1

    require(completed == 3, "all rows must be completed")
    require(not forbidden_used, "forbidden inputs used")
    require(rescoring_authorized_rows == 0, "T_joint rescoring must not be authorized")
    require(endpoint_authorized_rows == 0, "endpoint scoring must not be authorized")

    if accepted == 3:
        require(compatible_rows >= 1, "lambda policy compatibility must be accepted")
        require(lambda_authorized_rows >= 1, "numeric lambda record-only authorization must be accepted")
        decision = "AUTHORIZE_NUMERIC_LAMBDA_RECORD_ONLY_NOT_RESCORING_NOT_VALIDATION"
        response_status = "completed_numeric_lambda_review"
        next_action = "record_numeric_lambda_then_prepare_separate_rescoring_authorization_after_aligned_values"
        compatible = "true"
        lambda_authorized = "true"
    else:
        decision = "NUMERIC_LAMBDA_REJECTED_NOT_RESCORING"
        response_status = "rejected_numeric_lambda_review"
        next_action = "keep_numeric_lambda_and_rescoring_blocked"
        compatible = "false"
        lambda_authorized = "false"

    summary = {
        "run_id": "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_REVIEW_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "completed_response_rows": str(completed),
        "accepted_rows": str(accepted),
        "lambda_policy_compatible": compatible,
        "lambda_row_numeric_value": "1.0" if lambda_authorized == "true" else "",
        "lambda_row_numeric_value_authorized": lambda_authorized,
        "t_joint_rescoring_authorized": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "forbidden_inputs_used": "false",
        "decision": decision,
        "response_status": response_status,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(f"JOINT_ROW_LEVEL_NUMERIC_LAMBDA_REVIEW_RESPONSE_VALIDATED decision={decision}")


if __name__ == "__main__":
    main()

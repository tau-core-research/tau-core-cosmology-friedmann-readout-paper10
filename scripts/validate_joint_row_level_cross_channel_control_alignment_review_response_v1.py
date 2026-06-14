#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1_summary.csv"
PACKAGE_ID = "JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_row_level_cross_channel_control_alignment_review_not_scoring_not_validation"
EXPECTED_QUESTIONS = {"CCA_Q1_NEED", "CCA_Q2_RULE", "CCA_Q3_BOUNDARY"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate completed cross-channel control alignment review response.")
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

    require(
        package["status"] == "JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_REVIEW_PACKAGE_READY_NOT_COMPLETED",
        "unexpected package status",
    )
    require(len(rows) == 3, "response must contain three rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "question ids mismatch")

    accepted = 0
    completed = 0
    alignment_required_rows = 0
    design_accepted_rows = 0
    aligned_values_rows = 0
    lambda_authorized_rows = 0
    rescoring_authorized_rows = 0
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
        if norm(row["reviewer_response"]) in {"accept", "accept_with_caveats"}:
            accepted += 1
        else:
            require(norm(row["reviewer_response"]) == "reject", f"{qid}: unsupported reviewer response")
        completed += 1
        if is_true(row["forbidden_inputs_used"]):
            forbidden_used = True
        if is_true(row["cross_channel_control_alignment_required"]):
            alignment_required_rows += 1
        if is_true(row["alignment_design_accepted"]):
            design_accepted_rows += 1
        if is_true(row["aligned_joint_control_values_authorized"]):
            aligned_values_rows += 1
        if is_true(row["lambda_row_numeric_value_authorized"]):
            lambda_authorized_rows += 1
        if is_true(row["t_joint_rescoring_authorized"]):
            rescoring_authorized_rows += 1

    require(completed == 3, "all rows must be completed")
    require(not forbidden_used, "forbidden inputs used")
    require(aligned_values_rows == 0, "aligned joint control values must not be authorized here")
    require(lambda_authorized_rows == 0, "lambda_row numeric value must not be authorized")
    require(rescoring_authorized_rows == 0, "T_joint rescoring must not be authorized")

    if accepted == 3:
        require(alignment_required_rows >= 1, "cross-channel alignment requirement must be accepted")
        require(design_accepted_rows >= 1, "alignment design must be accepted")
        decision = "ACCEPT_CROSS_CHANNEL_CONTROL_ALIGNMENT_DESIGN_NOT_VALUES_NOT_RESCORING_NOT_VALIDATION"
        response_status = "completed_cross_channel_control_alignment_review"
        next_action = "prepare_separate_aligned_control_value_package_before_any_rescoring"
        alignment_required = "true"
        design_accepted = "true"
    else:
        decision = "CROSS_CHANNEL_CONTROL_ALIGNMENT_DESIGN_REJECTED_NOT_SCORING"
        response_status = "rejected_cross_channel_control_alignment_review"
        next_action = "keep_cross_channel_alignment_blocked"
        alignment_required = "false"
        design_accepted = "false"

    summary = {
        "run_id": "JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_REVIEW_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "completed_response_rows": str(completed),
        "accepted_rows": str(accepted),
        "cross_channel_control_alignment_required": alignment_required,
        "alignment_design_accepted": design_accepted,
        "aligned_joint_control_values_authorized": "false",
        "lambda_row_numeric_value_authorized": "false",
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
    print(f"JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_REVIEW_RESPONSE_VALIDATED decision={decision}")


if __name__ == "__main__":
    main()

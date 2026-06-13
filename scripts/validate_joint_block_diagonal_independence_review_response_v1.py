#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_block_diagonal_independence_review_response_template_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_block_diagonal_independence_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_block_diagonal_independence_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_block_diagonal_independence_review_package_v1.md"
PACKAGE_ID = "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_block_diagonal_independence_review_not_scoring_not_validation"

EXPECTED_QUESTIONS = {
    "BDI_Q1_BLOCK_SCOPE": {"accept", "caveated_accept", "reject"},
    "BDI_Q2_BLOCK_DIAGONAL_SURROGATE": {"accept_future_review_only", "reject"},
    "BDI_Q3_CROSS_PROBE_INDEPENDENCE": {"keep_open", "source_rationale_provided"},
    "BDI_Q4_NEXT_GATE": {"accept_protocol_shell", "reject"},
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
        description="Validate a Paper10 joint block-diagonal independence review response."
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
    require(package_summary["status"] == "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_PACKAGE_READY_NOT_COMPLETED", "unexpected package status")
    require(package_summary["endpoint_scoring_allowed"] == "false", "upstream package must not allow scoring")
    require(package_summary["endpoint_validation_claimed"] == "false", "upstream package must not claim validation")
    require(package_summary["cosmological_validation_claimed"] == "false", "upstream package must not claim cosmological validation")
    require(len(rows) == len(EXPECTED_QUESTIONS), "response must contain four rows")
    require({row["question_id"] for row in rows} == set(EXPECTED_QUESTIONS), "question ids mismatch")

    completed_flags: list[bool] = []
    responses: dict[str, str] = {}
    caveated_count = 0
    reject_count = 0
    for row in rows:
        qid = row["question_id"]
        require(row["review_id"] == PACKAGE_ID, f"{qid}: bad review_id")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{qid}: claim boundary mismatch")
        require(set(row["forbidden_inputs"].split(";")) == FORBIDDEN_INPUTS, f"{qid}: forbidden input list mismatch")
        for field in [
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "forbidden_inputs_used",
            "block_diagonal_surrogate_allowed_for_scoring_now",
            "cross_probe_covariance_defined",
        ]:
            require(is_false(row[field]), f"{qid}: unsafe field {field}")
        require(is_true(row["block_diagonal_surrogate_allowed_for_future_review"]), f"{qid}: future review flag should remain true")
        require(int(row["hard_blockers_open"]) >= 1, f"{qid}: hard blockers should remain open")

        completed = is_true(row["review_completed"])
        completed_flags.append(completed)
        value = norm(row["reviewer_response"])
        responses[qid] = value
        if completed:
            require(value in EXPECTED_QUESTIONS[qid], f"{qid}: unsupported reviewer_response {value}")
            require(row["reviewer_id_or_role"].strip(), f"{qid}: reviewer id/role required")
            require(row["reviewer_rationale"].strip(), f"{qid}: reviewer rationale required")
            if value == "caveated_accept":
                caveated_count += 1
            if value == "reject":
                reject_count += 1
        else:
            require(value == "", f"{qid}: incomplete response must leave reviewer_response blank")
            require(row["reviewer_id_or_role"].strip() == "", f"{qid}: incomplete response must leave reviewer id blank")
            require(row["reviewer_rationale"].strip() == "", f"{qid}: incomplete response must leave rationale blank")

    completed_count = sum(completed_flags)
    require(completed_count in {0, len(EXPECTED_QUESTIONS)}, "response must be either blank or fully completed")

    if completed_count == 0:
        decision = "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_RESPONSE_TEMPLATE_READY_NOT_COMPLETED"
        response_status = "not_completed"
        future_protocol_shell_allowed = "false"
        cross_probe_independence_status = "not_reviewed"
        next_action = "send_package_to_reviewer"
    elif reject_count:
        decision = "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_REJECTED_NOT_SCORING"
        response_status = "rejected"
        future_protocol_shell_allowed = "false"
        cross_probe_independence_status = "not_closed"
        next_action = "revise_or_seek_source_native_cross_probe_covariance"
    elif responses["BDI_Q3_CROSS_PROBE_INDEPENDENCE"] == "source_rationale_provided":
        decision = "JOINT_BLOCK_DIAGONAL_SOURCE_RATIONALE_PROVIDED_REQUIRES_MANUAL_FOLLOWUP_NOT_SCORING"
        response_status = "completed_source_rationale_requires_followup"
        future_protocol_shell_allowed = "true"
        cross_probe_independence_status = "manual_followup_required"
        next_action = "review_source_rationale_before_any_scoring_protocol"
    else:
        decision = "JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_ALLOWED_CROSS_PROBE_OPEN_NOT_SCORING"
        response_status = "completed_caveated_protocol_shell_allowed"
        future_protocol_shell_allowed = "true"
        cross_probe_independence_status = "kept_open"
        next_action = "build_block_diagonal_likelihood_surrogate_protocol_shell_without_scoring"

    doc_text = DOC.read_text()
    for marker in ["not scoring", "block-diagonal", "cross-probe", CLAIM_BOUNDARY]:
        require(marker in doc_text, f"doc missing marker: {marker}")

    summary = {
        "run_id": "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "completed_response_rows": str(completed_count),
        "caveated_accept_count": str(caveated_count),
        "reject_count": str(reject_count),
        "forbidden_inputs_used": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "future_protocol_shell_allowed": future_protocol_shell_allowed,
        "block_diagonal_surrogate_allowed_for_scoring_now": "false",
        "cross_probe_covariance_defined": "false",
        "cross_probe_independence_status": cross_probe_independence_status,
        "hard_blockers_open": package_summary["hard_blockers_open"],
        "response_status": response_status,
        "decision": decision,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(
        "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_RESPONSE_V1_VALIDATED "
        f"decision={decision}"
    )


if __name__ == "__main__":
    main()

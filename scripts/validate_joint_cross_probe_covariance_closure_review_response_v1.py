#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1_summary.csv"
DOC = ROOT / "docs/joint_cross_probe_covariance_closure_review_package_v1.md"
PACKAGE_ID = "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_cross_probe_covariance_closure_review_not_scoring_not_validation"

EXPECTED_QUESTIONS = {
    "CPC_Q1_SCOPE": {"accept", "caveated_accept", "reject"},
    "CPC_Q2_COVARIANCE_ROUTE": {"available_now", "not_available", "caveated_candidate"},
    "CPC_Q3_INDEPENDENCE_ROUTE": {"accept_future_scoring_precondition", "keep_open"},
    "CPC_Q4_LIMITS": {"list_required_caveats", "reject"},
    "CPC_Q5_NEXT_ACTION": {
        "keep_blocker_open",
        "acquire_covariance_product",
        "freeze_caveated_block_diagonal_preconditions",
    },
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
        description="Validate a Paper10 joint cross-probe covariance closure review response."
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
        package_summary["status"] == "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_PACKAGE_READY_NOT_COMPLETED",
        "unexpected package status",
    )
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "contains_endpoint_residuals",
        "contains_new_endpoint_scores",
        "contains_fit_statistics",
    ]:
        require(package_summary[field] == "false", f"upstream package unsafe field: {field}")
    require(len(rows) == len(EXPECTED_QUESTIONS), "response must contain five rows")
    require({row["question_id"] for row in rows} == set(EXPECTED_QUESTIONS), "question ids mismatch")

    completed_flags: list[bool] = []
    responses: dict[str, str] = {}
    caveated_count = 0
    reject_count = 0
    forbidden_used = False
    covariance_product_available = False
    independence_justified = False
    future_precondition_closure_allowed = False
    hard_blocker_open = True

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
        require(is_true(row["separate_scoring_authorization_required"]), f"{qid}: separate scoring authorization must remain required")

        completed = is_true(row["review_completed"])
        completed_flags.append(completed)
        value = norm(row["reviewer_response"])
        responses[qid] = value
        if is_true(row["forbidden_inputs_used"]):
            forbidden_used = True
        if is_true(row["cross_probe_covariance_product_available"]):
            covariance_product_available = True
        if is_true(row["block_diagonal_independence_source_justified"]):
            independence_justified = True
        if is_true(row["future_scoring_precondition_closure_allowed"]):
            future_precondition_closure_allowed = True
        if is_false(row["hard_blocker_remains_open"]):
            hard_blocker_open = False

        if completed:
            require(value in EXPECTED_QUESTIONS[qid], f"{qid}: unsupported reviewer_response {value}")
            require(row["reviewer_id_or_role"].strip(), f"{qid}: reviewer id/role required")
            require(row["reviewer_rationale"].strip(), f"{qid}: reviewer rationale required")
            if qid in {"CPC_Q2_COVARIANCE_ROUTE", "CPC_Q3_INDEPENDENCE_ROUTE"} and value in {
                "available_now",
                "caveated_candidate",
                "accept_future_scoring_precondition",
            }:
                require(row["source_reference_or_url"].strip(), f"{qid}: source reference required for a positive route")
            if value in {"caveated_accept", "caveated_candidate"}:
                caveated_count += 1
            if value == "reject":
                reject_count += 1
        else:
            require(value == "", f"{qid}: incomplete response must leave reviewer_response blank")
            require(row["reviewer_id_or_role"].strip() == "", f"{qid}: incomplete response must leave reviewer id blank")
            require(row["reviewer_rationale"].strip() == "", f"{qid}: incomplete response must leave rationale blank")

    completed_count = sum(completed_flags)
    require(completed_count in {0, len(EXPECTED_QUESTIONS)}, "response must be either blank or fully completed")
    require(not forbidden_used, "refusing response with forbidden_inputs_used=true")

    if completed_count == 0:
        decision = "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_RESPONSE_TEMPLATE_READY_NOT_COMPLETED"
        response_status = "not_completed"
        closure_route = "not_reviewed"
        next_action = "send_package_to_reviewer"
        hard_blocker_open = True
        future_precondition_closure_allowed = False
        covariance_product_available = False
        independence_justified = False
    elif reject_count:
        decision = "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_REJECTED_NOT_SCORING"
        response_status = "rejected"
        closure_route = "rejected"
        next_action = "revise_covariance_closure_package"
        hard_blocker_open = True
        future_precondition_closure_allowed = False
    elif responses["CPC_Q2_COVARIANCE_ROUTE"] == "available_now" and covariance_product_available:
        decision = "JOINT_CROSS_PROBE_COVARIANCE_PRODUCT_AVAILABLE_SOURCE_SIDE_NOT_SCORING"
        response_status = "completed_covariance_product_route"
        closure_route = "source_covariance_product"
        next_action = "build_covariance_product_binding_gate_before_scoring_authorization"
        hard_blocker_open = False
        future_precondition_closure_allowed = True
    elif (
        responses["CPC_Q3_INDEPENDENCE_ROUTE"] == "accept_future_scoring_precondition"
        and independence_justified
        and future_precondition_closure_allowed
    ):
        decision = "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_PRECONDITION_CAVEATED_CLOSED_NOT_SCORING"
        response_status = "completed_caveated_independence_route"
        closure_route = "caveated_block_diagonal_independence"
        next_action = "build_separate_scoring_authorization_package_with_caveats"
        hard_blocker_open = False
    else:
        decision = "JOINT_CROSS_PROBE_COVARIANCE_INDEPENDENCE_REMAINS_OPEN_NOT_SCORING"
        response_status = "completed_blocker_kept_open"
        closure_route = "kept_open"
        next_action = "acquire_source_covariance_or_stronger_independence_rationale"
        hard_blocker_open = True
        future_precondition_closure_allowed = False

    if future_precondition_closure_allowed:
        require(
            covariance_product_available or independence_justified,
            "future precondition closure requires covariance product or independence justification",
        )
        require(not hard_blocker_open, "hard blocker cannot remain open if future precondition closure is allowed")

    doc_text = DOC.read_text()
    for marker in ["not scoring", "cross-probe covariance/independence", "Covariance-product route", CLAIM_BOUNDARY]:
        require(marker in doc_text, f"doc missing marker: {marker}")

    summary = {
        "run_id": "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "completed_response_rows": str(completed_count),
        "caveated_count": str(caveated_count),
        "reject_count": str(reject_count),
        "forbidden_inputs_used": "false",
        "cross_probe_covariance_product_available": str(covariance_product_available).lower(),
        "block_diagonal_independence_source_justified": str(independence_justified).lower(),
        "future_scoring_precondition_closure_allowed": str(future_precondition_closure_allowed).lower(),
        "separate_scoring_authorization_required": "true",
        "hard_blocker_remains_open": str(hard_blocker_open).lower(),
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "closure_route": closure_route,
        "response_status": response_status,
        "decision": decision,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(
        "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_RESPONSE_V1_VALIDATED "
        f"decision={decision}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1_summary.csv"
)
CLAIM_BOUNDARY = "paper10_desi_shape_row2_source_native_shape_support_review_not_validation"
EXPECTED_RESPONSES = {
    "Q1_SOURCE_IDENTITY": {"accept", "accept_source_identity", "reject", "needs_more_context"},
    "Q2_COVARIANCE_STATUS": {"accept", "accept_covariance_context", "reject", "needs_more_context"},
    "Q3_SHAPE_VECTOR_STATUS": {
        "accept",
        "accept_as_caveat_reducing_source_support",
        "reject",
        "needs_more_context",
    },
    "Q4_NEXT_GATE": {
        "accept_source_context_only",
        "needs_separate_promotion_review",
        "needs_more_context",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed DESI shape row2 source-native shape-support review response."
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def nonempty(value: str) -> bool:
    return bool(value.strip())


def norm(value: str) -> str:
    return value.strip().lower()


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response)
    summary_out = resolve(args.summary_out)

    package = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)

    require(
        package["status"] == "DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package["review_completed"] == "false", "package must be uncompleted before response import")
    require(package["row2_interval"] == "0.934-1.321", "row2 interval mismatch")
    require(package["source_native_row_count"] == "4", "source-native row count mismatch")
    require(package["row2_covariance_positive_definite"] == "true", "package covariance status mismatch")
    require(package["row2_source_caveat_reduced"] == "false", "package must not pre-reduce caveat")
    require(package["row2_endpoint_ready"] == "false", "package must not mark row2 endpoint-ready")
    require(package["row2_promotion_ready"] == "false", "package must not promote row2")
    require(package["endpoint_replay_allowed"] == "false", "package must not authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(package["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(package["contains_endpoint_residuals"] == "false", "package must not contain residuals")
    require(package["contains_endpoint_scores"] == "false", "package must not contain scores")
    require(package["contains_fit_statistics"] == "false", "package must not contain fit statistics")
    require(package["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")

    require(len(rows) == len(EXPECTED_RESPONSES), "completed response must contain exactly four rows")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")

    for question_id, allowed in EXPECTED_RESPONSES.items():
        row = by_id[question_id]
        response = norm(row.get("reviewer_response", ""))
        require(norm(row.get("review_completed", "")) == "true", f"{question_id}: review_completed must be true")
        require(nonempty(row.get("reviewer_id_or_role", "")), f"{question_id}: reviewer_id_or_role required")
        require(response in allowed, f"{question_id}: bad reviewer_response")
        require(nonempty(row.get("reviewer_rationale", "")), f"{question_id}: reviewer_rationale required")
        require(norm(row["forbidden_inputs_used"]) == "false", f"{question_id}: forbidden inputs must remain false")
        require(row["row2_interval"] == "0.934-1.321", f"{question_id}: row2 interval changed")
        require(row["source_native_row_count"] == "4", f"{question_id}: source-native row count changed")
        require(norm(row["row2_covariance_positive_definite"]) == "true", f"{question_id}: covariance status changed")
        require(norm(row["uses_endpoint_scores"]) == "false", f"{question_id}: endpoint scores forbidden")
        require(norm(row["uses_endpoint_residuals"]) == "false", f"{question_id}: endpoint residuals forbidden")
        require(norm(row["row2_endpoint_ready"]) == "false", f"{question_id}: row2 endpoint-ready forbidden")
        require(norm(row["row2_promotion_ready"]) == "false", f"{question_id}: row2 promotion forbidden")
        require(norm(row["endpoint_replay_allowed"]) == "false", f"{question_id}: replay must remain disabled")
        require(norm(row["endpoint_validation_claimed"]) == "false", f"{question_id}: endpoint validation must remain false")
        require(norm(row["physical_validation_claimed"]) == "false", f"{question_id}: physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    q1 = norm(by_id["Q1_SOURCE_IDENTITY"]["reviewer_response"])
    q2 = norm(by_id["Q2_COVARIANCE_STATUS"]["reviewer_response"])
    q3 = norm(by_id["Q3_SHAPE_VECTOR_STATUS"]["reviewer_response"])
    q4 = norm(by_id["Q4_NEXT_GATE"]["reviewer_response"])

    q1_accept = q1 in {"accept", "accept_source_identity"}
    q2_accept = q2 in {"accept", "accept_covariance_context"}
    q3_accept = q3 in {"accept", "accept_as_caveat_reducing_source_support"}
    q4_context_only = q4 == "accept_source_context_only"
    q4_promotion_review = q4 == "needs_separate_promotion_review"
    rejected = "reject" in {q1, q2, q3}
    needs_more_context = "needs_more_context" in {q1, q2, q3, q4}
    accepted = q1_accept and q2_accept and q3_accept and (q4_context_only or q4_promotion_review)

    require(not (accepted and rejected), "response cannot be both accepted and rejected")
    if q3_accept:
        require(q1_accept and q2_accept, "shape-vector acceptance requires source identity and covariance acceptance")
    if q4_promotion_review:
        require(q3_accept, "separate promotion-review request requires accepted source support")

    if accepted:
        status = "DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_REVIEW_ACCEPTED_CAVEAT_REDUCTION_NOT_REPLAY"
        verdict = "row2_source_native_shape_support_accepted_as_caveat_reducing_not_endpoint_ready"
        row2_source_caveat_reduced = "true"
        promotion_review_required = "true" if q4_promotion_review else "false"
        recommended_next_action = (
            "prepare_separate_row2_promotion_authorization_handoff_only_if_needed"
            if q4_promotion_review
            else "record_source_native_shape_support_as_caveat_reduction_without_replay"
        )
    elif rejected:
        status = "DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_REVIEW_REJECTED_NOT_REPLAY"
        verdict = "row2_source_native_shape_support_rejected_or_source_identity_failed"
        row2_source_caveat_reduced = "false"
        promotion_review_required = "false"
        recommended_next_action = "keep_row2_source_caveat_and_seek_alternative_source_native_support"
    else:
        require(needs_more_context, "non-accepted non-rejected response must request more context")
        status = "DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_REVIEW_NEEDS_MORE_CONTEXT_NOT_REPLAY"
        verdict = "row2_source_native_shape_support_needs_more_context_before_caveat_reduction"
        row2_source_caveat_reduced = "false"
        promotion_review_required = "false"
        recommended_next_action = "provide_additional_source_native_context_or_seek_alternative_support"

    write_csv(
        summary_out,
        [
            {
                "policy_id": "PAPER10_DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_REVIEW_V1",
                "status": status,
                "response_path": rel_or_abs(response_path),
                "response_sha256": sha256(response_path),
                "reviewed_package_sha256": package["zip_sha256"],
                "review_completed": "true",
                "question_count": str(len(rows)),
                "source_identity_decision": q1,
                "covariance_status_decision": q2,
                "shape_vector_status_decision": q3,
                "next_gate_decision": q4,
                "forbidden_inputs_used": "false",
                "row2_interval": "0.934-1.321",
                "source_native_row_count": "4",
                "row2_covariance_positive_definite": "true",
                "row2_source_caveat_reduced": row2_source_caveat_reduced,
                "promotion_review_required_before_endpoint": promotion_review_required,
                "row2_endpoint_ready": "false",
                "row2_promotion_ready": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
                "recommended_next_action": recommended_next_action,
            }
        ],
    )
    print(f"PAPER10_DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_REVIEW_RESPONSE_VALIDATED verdict={verdict}")


if __name__ == "__main__":
    main()

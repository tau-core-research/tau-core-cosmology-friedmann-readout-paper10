#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_row1_confirmatory_source_review_not_validation"
EXPECTED_RESPONSES = {
    "Q1_source_identity": {"accept", "accept_source_identity", "reject", "needs_more_context"},
    "Q2_interval_support": {
        "accept",
        "accept_as_confirmatory_in_interval_support_not_endpoint_replacement",
        "reject",
        "needs_more_context",
    },
    "Q3_core_support_status": {
        "accept",
        "accept_row1_source_side_confirmatory_supported_not_route_promotion",
        "reject",
        "needs_more_context",
    },
    "Q4_next_gate": {"accept", "accept_separate_core_support_synthesis_or_route_level_gate_still_required"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed DESI shape Row1 confirmatory source review response."
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
        package["status"] == "DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package["review_completed"] == "false", "package must be uncompleted before response import")
    require(package["row1_confirmatory_source_count"] == "2", "package support count mismatch")
    require(package["attached_z_values"] == "0.75;0.88", "package z-values mismatch")
    require(package["row1_endpoint_ready"] == "false", "package must not mark Row1 endpoint-ready")
    require(package["row1_promotion_ready"] == "false", "package must not promote Row1")
    require(package["endpoint_replay_allowed"] == "false", "package must not authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(package["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(package["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")

    require(len(rows) == len(EXPECTED_RESPONSES), "completed response must contain exactly four rows")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")

    for question_id, allowed in EXPECTED_RESPONSES.items():
        row = by_id[question_id]
        response = norm(row.get("reviewer_response", ""))
        require(row["review_completed"] == "true", f"{question_id}: review_completed must be true")
        require(nonempty(row.get("reviewer_id_or_role", "")), f"{question_id}: reviewer_id_or_role required")
        require(response in allowed, f"{question_id}: bad reviewer_response {response}")
        require(nonempty(row.get("reviewer_rationale", "")), f"{question_id}: reviewer_rationale required")
        require(row["forbidden_inputs_used"] == "false", f"{question_id}: forbidden inputs must remain false")
        require(row["attached_source_references"] == "Borghi et al. (2022);Stern et al. (2010)", f"{question_id}: references changed")
        require(row["attached_z_values"] == "0.75;0.88", f"{question_id}: z values changed")
        require(row["row1_confirmatory_source_count"] == "2", f"{question_id}: support count changed")
        require(row["row1_endpoint_ready"] == "false", f"{question_id}: Row1 endpoint-ready forbidden")
        require(row["row1_promotion_ready"] == "false", f"{question_id}: Row1 promotion forbidden")
        require(row["endpoint_replay_allowed"] == "false", f"{question_id}: replay must remain disabled")
        require(row["endpoint_validation_claimed"] == "false", f"{question_id}: endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", f"{question_id}: physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    q1 = norm(by_id["Q1_source_identity"]["reviewer_response"])
    q2 = norm(by_id["Q2_interval_support"]["reviewer_response"])
    q3 = norm(by_id["Q3_core_support_status"]["reviewer_response"])
    q4 = norm(by_id["Q4_next_gate"]["reviewer_response"])

    q1_accept = q1 in {"accept", "accept_source_identity"}
    q2_accept = q2 in {"accept", "accept_as_confirmatory_in_interval_support_not_endpoint_replacement"}
    q3_accept = q3 in {"accept", "accept_row1_source_side_confirmatory_supported_not_route_promotion"}
    q4_accept = q4 in {"accept", "accept_separate_core_support_synthesis_or_route_level_gate_still_required"}
    accepted = q1_accept and q2_accept and q3_accept and q4_accept
    rejected = "reject" in {q1, q2, q3}
    needs_more_context = "needs_more_context" in {q1, q2, q3}
    require(not (accepted and rejected), "response cannot be both accepted and rejected")

    if accepted:
        status = "DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_REVIEW_ACCEPTED_NOT_REPLAY_NOT_VALIDATION"
        verdict = "row1_confirmatory_source_review_accepted_not_endpoint_ready"
        row1_confirmatory_source_accepted = "true"
        recommended_next_action = "record_row1_confirmatory_source_support_then_use_core_synthesis_gate_for_stronger_claims"
    elif rejected:
        status = "DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_REVIEW_REJECTED_NOT_REPLAY"
        verdict = "row1_confirmatory_source_review_rejected"
        row1_confirmatory_source_accepted = "false"
        recommended_next_action = "seek_alternative_row1_confirmatory_source_support"
    else:
        require(needs_more_context, "non-accepted non-rejected response must request more context")
        status = "DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_REVIEW_NEEDS_MORE_CONTEXT_NOT_REPLAY"
        verdict = "row1_confirmatory_source_review_needs_more_context"
        row1_confirmatory_source_accepted = "false"
        recommended_next_action = "provide_additional_source_context_or_seek_alternative_row1_support"

    write_csv(
        summary_out,
        [
            {
                "policy_id": "PAPER10_DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_REVIEW_V1",
                "status": status,
                "response_path": rel_or_abs(response_path),
                "response_sha256": sha256(response_path),
                "reviewed_package_sha256": package["zip_sha256"],
                "review_completed": "true",
                "question_count": str(len(rows)),
                "source_identity_decision": q1,
                "interval_support_decision": q2,
                "core_support_status_decision": q3,
                "next_gate_decision": q4,
                "forbidden_inputs_used": "false",
                "attached_source_references": "Borghi et al. (2022);Stern et al. (2010)",
                "attached_z_values": "0.75;0.88",
                "row1_confirmatory_source_count": "2",
                "row1_confirmatory_source_accepted": row1_confirmatory_source_accepted,
                "row1_endpoint_ready": "false",
                "row1_promotion_ready": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
                "recommended_next_action": recommended_next_action,
            }
        ],
    )
    print(f"PAPER10_DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_REVIEW_RESPONSE_VALIDATED verdict={verdict}")


if __name__ == "__main__":
    main()

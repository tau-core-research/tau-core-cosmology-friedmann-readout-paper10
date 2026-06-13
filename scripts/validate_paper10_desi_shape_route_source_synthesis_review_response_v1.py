#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_route_source_synthesis_review_not_replay_not_validation"
EXPECTED_POLICY_ID = "PAPER10_DESI_SHAPE_ROUTE_SOURCE_SYNTHESIS_REVIEW_POLICY_V1"
EXPECTED_RESPONSES = {
    "Q1": {
        "accept",
        "accept_source_synthesis_support_for_future_gate_preparation_not_endpoint_ready",
        "reject",
        "needs_more_context",
    },
    "Q2": {
        "accept",
        "accept_multi_row_interpretation_row2_negative_not_route_falsification",
        "reject",
        "needs_more_context",
    },
    "Q3": {
        "accept",
        "accept_future_validation_gate_preparation_only_no_current_replay_or_validation",
        "reject",
        "needs_more_context",
    },
    "Q4": {
        "accept",
        "accept_remaining_caveats_listed_no_blocker_to_future_gate_preparation",
        "no_source_acquisition_blocker_to_future_gate_preparation_but_validation_blockers_remain",
        "accept_with_caveats",
        "reject",
        "needs_more_context",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed DESI shape-route source-synthesis review response."
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


def one_row(path: Path) -> dict[str, str]:
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


def norm(value: str) -> str:
    return value.strip().lower()


def is_false(value: str) -> bool:
    return norm(value) == "false"


def is_true(value: str) -> bool:
    return norm(value) == "true"


def nonempty(value: str) -> bool:
    return bool(value.strip())


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response)
    summary_out = resolve(args.summary_out)
    package = one_row(PACKAGE_SUMMARY)
    rows = read_rows(response_path)

    require(
        package["status"] == "DESI_SHAPE_ROUTE_SOURCE_SYNTHESIS_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package["review_completed"] == "false", "package must be uncompleted before response import")
    require(package["core_rows"] == "1;2", "package core rows mismatch")
    require(package["most_required_row"] == "1", "package most required row mismatch")
    require(package["endpoint_replay_allowed"] == "false", "package must not authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim endpoint validation")
    require(package["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(package["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")

    require(len(rows) == len(EXPECTED_RESPONSES), "completed response must contain exactly four rows")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")

    for question_id, allowed in EXPECTED_RESPONSES.items():
        row = by_id[question_id]
        response = norm(row.get("reviewer_response", ""))
        require(row["policy_id"] == EXPECTED_POLICY_ID, f"{question_id}: policy id mismatch")
        require(is_true(row["review_completed"]), f"{question_id}: review_completed must be true")
        require(nonempty(row.get("reviewer_id_or_role", "")), f"{question_id}: reviewer_id_or_role required")
        require(response in allowed, f"{question_id}: bad reviewer_response {response}")
        require(nonempty(row.get("reviewer_rationale", "")), f"{question_id}: reviewer_rationale required")
        require(is_false(row["forbidden_inputs_used"]), f"{question_id}: forbidden inputs must remain false")
        require(row["core_rows"] == "1;2", f"{question_id}: core rows changed")
        require(row["most_required_row"] == "1", f"{question_id}: most required row changed")
        require(
            row["row1_status"] == "most_required_confirmatory_independent_support_review_accepted_not_endpoint_ready",
            f"{question_id}: Row1 status changed",
        )
        require(
            row["row2_status"] == "caveat_reduced_but_permission_replay_not_control_resistant_not_promotion_ready",
            f"{question_id}: Row2 status changed",
        )
        require(
            row["route_interpretation"] == "multi_row_narrow_margin_source_sensitive_signal_not_row2_only",
            f"{question_id}: route interpretation changed",
        )
        require(is_false(row["shape_route_promotion_allowed"]), f"{question_id}: route promotion forbidden")
        require(is_false(row["endpoint_replay_allowed"]), f"{question_id}: replay must remain disabled")
        require(is_false(row["endpoint_validation_claimed"]), f"{question_id}: endpoint validation must remain false")
        require(is_false(row["physical_validation_claimed"]), f"{question_id}: physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    q1 = norm(by_id["Q1"]["reviewer_response"])
    q2 = norm(by_id["Q2"]["reviewer_response"])
    q3 = norm(by_id["Q3"]["reviewer_response"])
    q4 = norm(by_id["Q4"]["reviewer_response"])
    q1_accept = q1 in {"accept", "accept_source_synthesis_support_for_future_gate_preparation_not_endpoint_ready"}
    q2_accept = q2 in {"accept", "accept_multi_row_interpretation_row2_negative_not_route_falsification"}
    q3_accept = q3 in {"accept", "accept_future_validation_gate_preparation_only_no_current_replay_or_validation"}
    q4_accept = q4 in {
        "accept",
        "accept_with_caveats",
        "accept_remaining_caveats_listed_no_blocker_to_future_gate_preparation",
        "no_source_acquisition_blocker_to_future_gate_preparation_but_validation_blockers_remain",
    }
    rejected = "reject" in {q1, q2, q3, q4}
    needs_more_context = "needs_more_context" in {q1, q2, q3, q4}
    accepted = q1_accept and q2_accept and q3_accept and q4_accept
    require(not (accepted and rejected), "response cannot be both accepted and rejected")

    if accepted:
        status = "DESI_SHAPE_ROUTE_SOURCE_SYNTHESIS_REVIEW_ACCEPTED_FOR_FUTURE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION"
        decision = "ACCEPT_AS_SOURCE_SYNTHESIS_SUPPORT_FOR_FUTURE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION"
        future_gate_preparation_allowed = "true"
        verdict = "source_synthesis_supports_future_gate_preparation_not_replay_not_validation"
        recommended_next_action = "prepare_separate_validation_or_replay_gate_package_with_explicit_authorization_if_needed_no_current_validation_claim"
    elif rejected:
        status = "DESI_SHAPE_ROUTE_SOURCE_SYNTHESIS_REVIEW_REJECTED_NOT_REPLAY"
        decision = "REJECT_SOURCE_SYNTHESIS_SUPPORT"
        future_gate_preparation_allowed = "false"
        verdict = "source_synthesis_review_rejected"
        recommended_next_action = "return_to_source_acquisition_before_any_gate_preparation"
    else:
        require(needs_more_context, "non-accepted non-rejected response must request more context")
        status = "DESI_SHAPE_ROUTE_SOURCE_SYNTHESIS_REVIEW_NEEDS_MORE_CONTEXT_NOT_REPLAY"
        decision = "NEEDS_MORE_CONTEXT"
        future_gate_preparation_allowed = "false"
        verdict = "source_synthesis_review_needs_more_context"
        recommended_next_action = "provide_additional_source_context_before_gate_preparation"

    write_csv(
        summary_out,
        [
            {
                "policy_id": EXPECTED_POLICY_ID,
                "status": status,
                "decision": decision,
                "response_path": rel_or_abs(response_path),
                "response_sha256": sha256(response_path),
                "reviewed_package_sha256": package["zip_sha256"],
                "review_completed": "true",
                "question_count": str(len(rows)),
                "accepted_question_count": str(sum([q1_accept, q2_accept, q3_accept, q4_accept])),
                "core_rows": "1;2",
                "most_required_row": "1",
                "row1_status": "most_required_confirmatory_independent_support_review_accepted_not_endpoint_ready",
                "row2_status": "caveat_reduced_but_permission_replay_not_control_resistant_not_promotion_ready",
                "route_interpretation": "multi_row_narrow_margin_source_sensitive_signal_not_row2_only",
                "future_gate_preparation_allowed": future_gate_preparation_allowed,
                "shape_route_promotion_allowed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "forbidden_inputs_used": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
                "recommended_next_action": recommended_next_action,
            }
        ],
    )
    print(f"PAPER10_DESI_SHAPE_ROUTE_SOURCE_SYNTHESIS_REVIEW_RESPONSE_VALIDATED verdict={verdict}")


if __name__ == "__main__":
    main()

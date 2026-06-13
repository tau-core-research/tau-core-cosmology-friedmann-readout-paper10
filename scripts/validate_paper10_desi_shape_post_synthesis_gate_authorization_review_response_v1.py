#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_shape_post_synthesis_gate_authorization_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_post_synthesis_gate_authorization_review_not_replay_not_validation"
EXPECTED_POLICY_ID = "PAPER10_DESI_SHAPE_POST_SYNTHESIS_GATE_AUTHORIZATION_REVIEW_POLICY_V1"
EXPECTED_RESPONSES = {
    "Q1": {
        "accept",
        "accept_prepare_separate_validation_oriented_gate_package",
        "reject",
        "needs_more_context",
    },
    "Q2": {
        "accept",
        "accept_caveat_retention",
        "reject",
        "needs_more_context",
    },
    "Q3": {
        "accept",
        "accept_later_authorization_package_preparation_only",
        "reject",
        "needs_more_context",
    },
    "Q4": {
        "accept",
        "accept_no_source_blocker_but_validation_blockers_remain",
        "no_return_to_source_acquisition_required_for_package_preparation_but_validation_blockers_remain",
        "accept_with_caveats",
        "reject",
        "needs_more_context",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed DESI shape post-synthesis gate authorization review response."
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
    package = one_row(PACKAGE_SUMMARY)
    rows = read_rows(response_path)

    require(package["status"] == "DESI_SHAPE_POST_SYNTHESIS_GATE_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED", "bad package status")
    require(package["review_completed"] == "false", "package must be uncompleted before response import")
    require(package["source_synthesis_future_gate_preparation_allowed"] == "true", "source synthesis gate preparation must be allowed")
    require(package["route_margin"] == "0.01485705264", "route margin mismatch")
    require(package["robustness_verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation", "robustness verdict mismatch")
    require(package["prepare_later_authorization_package_allowed"] == "false", "package must not pre-allow later package")
    require(package["endpoint_replay_allowed"] == "false", "package must not authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim endpoint validation")
    require(package["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(package["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")

    require(len(rows) == 4, "completed response must contain exactly four rows")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")

    for qid, allowed in EXPECTED_RESPONSES.items():
        row = by_id[qid]
        response = norm(row.get("reviewer_response", ""))
        require(row["policy_id"] == EXPECTED_POLICY_ID, f"{qid}: policy id mismatch")
        require(is_true(row["review_completed"]), f"{qid}: review_completed must be true")
        require(row.get("reviewer_id_or_role", "").strip(), f"{qid}: reviewer id required")
        require(response in allowed, f"{qid}: bad reviewer_response {response}")
        require(row.get("reviewer_rationale", "").strip(), f"{qid}: reviewer rationale required")
        require(is_false(row["forbidden_inputs_used"]), f"{qid}: forbidden inputs must remain false")
        require(is_true(row["source_synthesis_future_gate_preparation_allowed"]), f"{qid}: source synthesis flag changed")
        require(row["route_candidate_score"] == "5.52425578108", f"{qid}: route candidate score changed")
        require(row["route_best_control_score"] == "5.50939872844", f"{qid}: route best control score changed")
        require(row["route_margin"] == "0.01485705264", f"{qid}: route margin changed")
        require(row["robustness_verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation", f"{qid}: robustness changed")
        require(row["route_interpretation"] == "multi_row_narrow_margin_source_sensitive_signal_not_row2_only", f"{qid}: route interpretation changed")
        require(is_false(row["endpoint_replay_allowed"]), f"{qid}: immediate replay must remain false")
        require(is_false(row["endpoint_validation_claimed"]), f"{qid}: endpoint validation must remain false")
        require(is_false(row["physical_validation_claimed"]), f"{qid}: physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{qid}: claim boundary mismatch")

    q1 = norm(by_id["Q1"]["reviewer_response"])
    q2 = norm(by_id["Q2"]["reviewer_response"])
    q3 = norm(by_id["Q3"]["reviewer_response"])
    q4 = norm(by_id["Q4"]["reviewer_response"])
    q1_accept = q1 in {"accept", "accept_prepare_separate_validation_oriented_gate_package"}
    q2_accept = q2 in {"accept", "accept_caveat_retention"}
    q3_accept = q3 in {"accept", "accept_later_authorization_package_preparation_only"}
    q4_accept = q4 in {"accept", "accept_with_caveats", "accept_no_source_blocker_but_validation_blockers_remain"}
    q4_accept = q4_accept or q4 == "no_return_to_source_acquisition_required_for_package_preparation_but_validation_blockers_remain"
    accepted = q1_accept and q2_accept and q3_accept and q4_accept
    rejected = "reject" in {q1, q2, q3, q4}
    needs_more_context = "needs_more_context" in {q1, q2, q3, q4}
    require(not (accepted and rejected), "response cannot be both accepted and rejected")

    # A positive response may allow preparation of a later package. It still
    # must not authorize immediate replay or validation.
    prep_allowed_values = {norm(row["prepare_later_authorization_package_allowed"]) for row in rows}
    if accepted:
        require(prep_allowed_values == {"true"}, "accepted response must consistently allow later package preparation")
        status = "DESI_SHAPE_POST_SYNTHESIS_GATE_AUTHORIZATION_REVIEW_ACCEPTED_FOR_SEPARATE_GATE_PREPARATION_NOT_REPLAY_NOT_VALIDATION"
        decision = "ACCEPT_PREPARE_SEPARATE_VALIDATION_ORIENTED_GATE_PACKAGE_NOT_REPLAY_NOT_VALIDATION"
        prepare_later_authorization_package_allowed = "true"
        verdict = "gate_preparation_authorized_only_current_route_not_validated"
        recommended_next_action = "prepare_separate_validation_oriented_gate_package_with_explicit_future_authorization_no_current_replay_or_validation_claim"
    elif rejected:
        require(prep_allowed_values == {"false"}, "rejected response cannot allow later package preparation")
        status = "DESI_SHAPE_POST_SYNTHESIS_GATE_AUTHORIZATION_REVIEW_REJECTED_NOT_REPLAY"
        decision = "REJECT_PREPARING_SEPARATE_GATE_PACKAGE"
        prepare_later_authorization_package_allowed = "false"
        verdict = "post_synthesis_gate_authorization_rejected"
        recommended_next_action = "return_to_source_or_protocol_work_before_gate_preparation"
    else:
        require(needs_more_context, "non-accepted non-rejected response must request more context")
        require(prep_allowed_values == {"false"}, "needs-more-context response cannot allow later package preparation")
        status = "DESI_SHAPE_POST_SYNTHESIS_GATE_AUTHORIZATION_REVIEW_NEEDS_MORE_CONTEXT_NOT_REPLAY"
        decision = "NEEDS_MORE_CONTEXT"
        prepare_later_authorization_package_allowed = "false"
        verdict = "post_synthesis_gate_authorization_needs_more_context"
        recommended_next_action = "provide_additional_context_before_gate_preparation"

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
                "source_synthesis_future_gate_preparation_allowed": "true",
                "prepare_later_authorization_package_allowed": prepare_later_authorization_package_allowed,
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "forbidden_inputs_used": "false",
                "route_candidate_score": "5.52425578108",
                "route_best_control_score": "5.50939872844",
                "route_margin": "0.01485705264",
                "robustness_verdict": "positive_but_narrow_margin_and_row_sensitive_not_validation",
                "route_interpretation": "multi_row_narrow_margin_source_sensitive_signal_not_row2_only",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
                "recommended_next_action": recommended_next_action,
            }
        ],
    )
    print(f"PAPER10_DESI_SHAPE_POST_SYNTHESIS_GATE_AUTHORIZATION_RESPONSE_VALIDATED verdict={verdict}")


if __name__ == "__main__":
    main()

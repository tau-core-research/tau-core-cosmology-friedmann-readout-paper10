#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1.csv"
DEFAULT_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_replay_authorization_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_replay_authorization_review_not_validation"
EXPECTED_RESPONSES = {
    "Q1_SCOPE": {"accept", "reject"},
    "Q2_SOURCE_STATUS": {"accept", "reject", "needs_more_context"},
    "Q3_ENDPOINT_PAIR_BLOCKER": {"accept_blocker_remains", "reject"},
    "Q4_AUTHORIZATION_DECISION": {"authorize_row2_permission_only_replay", "reject"},
    "Q5_CLAIM_BOUNDARY": {"accept"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a completed Row2 replay-authorization response.")
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


def norm(value: str) -> str:
    return value.strip().lower()


def nonempty(value: str) -> bool:
    return bool(value.strip())


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response)
    summary_out = resolve(args.summary_out)

    package = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)

    require(
        package["status"] == "DESI_SHAPE_ROW2_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package["review_completed"] == "false", "package must be uncompleted before response import")
    require(package["moresco_caveat_reduced"] == "true", "package Moresco caveat mismatch")
    require(package["source_native_shape_caveat_reduced"] == "true", "package source-native caveat mismatch")
    require(package["row2_source_caveat_reduced"] == "true", "package Row2 caveat mismatch")
    require(package["endpoint_pair_independence_satisfied"] == "false", "package endpoint-pair mismatch")
    require(package["row2_promotion_ready"] == "false", "package must not mark Row2 promotion-ready")
    require(package["shape_route_promotion_allowed"] == "false", "package must not allow shape-route promotion")
    require(package["separate_replay_authorization_review_allowed"] == "true", "package separate review flag mismatch")
    require(package["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim endpoint validation")
    require(package["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(package["contains_endpoint_residuals"] == "false", "package must not contain residuals")
    require(package["contains_endpoint_scores"] == "false", "package must not contain scores")
    require(package["contains_fit_statistics"] == "false", "package must not contain fit stats")
    require(package["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")

    require(len(rows) == len(EXPECTED_RESPONSES), "completed response must contain exactly five rows")
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
        require(norm(row["moresco_caveat_reduced"]) == "true", f"{question_id}: Moresco caveat changed")
        require(norm(row["source_native_shape_caveat_reduced"]) == "true", f"{question_id}: source-native caveat changed")
        require(norm(row["row2_source_caveat_reduced"]) == "true", f"{question_id}: Row2 caveat changed")
        require(norm(row["endpoint_pair_independence_satisfied"]) == "false", f"{question_id}: endpoint-pair blocker changed")
        require(norm(row["row2_promotion_ready"]) == "false", f"{question_id}: Row2 promotion-ready forbidden")
        require(norm(row["shape_route_promotion_allowed"]) == "false", f"{question_id}: shape-route promotion forbidden")
        require(norm(row["separate_replay_authorization_review_allowed"]) == "true", f"{question_id}: separate review flag changed")
        require(norm(row["endpoint_validation_claimed"]) == "false", f"{question_id}: endpoint validation forbidden")
        require(norm(row["physical_validation_claimed"]) == "false", f"{question_id}: physical validation forbidden")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    q1 = norm(by_id["Q1_SCOPE"]["reviewer_response"])
    q2 = norm(by_id["Q2_SOURCE_STATUS"]["reviewer_response"])
    q3 = norm(by_id["Q3_ENDPOINT_PAIR_BLOCKER"]["reviewer_response"])
    q4 = norm(by_id["Q4_AUTHORIZATION_DECISION"]["reviewer_response"])
    q5 = norm(by_id["Q5_CLAIM_BOUNDARY"]["reviewer_response"])

    rejected = q1 == "reject" or q2 == "reject" or q3 == "reject" or q4 == "reject"
    needs_more_context = q2 == "needs_more_context"
    authorized = (
        q1 == "accept"
        and q2 == "accept"
        and q3 == "accept_blocker_remains"
        and q4 == "authorize_row2_permission_only_replay"
        and q5 == "accept"
    )
    require(q5 == "accept", "Q5 must accept claim boundary")

    endpoint_replay_allowed = "true" if authorized else "false"
    if authorized:
        # The response may turn on replay permission only at this final
        # authorization gate; validation and promotion remain false.
        for row in rows:
            require(norm(row["endpoint_replay_allowed"]) == "true", "authorized response rows must mark replay true")
        status = "DESI_SHAPE_ROW2_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY_NOT_VALIDATION"
        verdict = "GO_DESI_SHAPE_ROW2_REPLAY_PERMISSION_ONLY"
        recommended_next_action = "run_one_frozen_Row2_permission_only_replay_later_without_validation_or_route_promotion_claims"
    elif rejected:
        for row in rows:
            require(norm(row["endpoint_replay_allowed"]) == "false", "rejected response rows must keep replay false")
        status = "DESI_SHAPE_ROW2_REPLAY_AUTHORIZATION_REJECTED_NOT_REPLAY"
        verdict = "NO_GO_ROW2_REPLAY_AUTHORIZATION"
        recommended_next_action = "keep_row2_blocked_and_seek_stronger_source_or_endpoint_pair_independence"
    else:
        require(needs_more_context, "non-accepted non-rejected response must request more context")
        for row in rows:
            require(norm(row["endpoint_replay_allowed"]) == "false", "needs-more-context rows must keep replay false")
        status = "DESI_SHAPE_ROW2_REPLAY_AUTHORIZATION_NEEDS_MORE_CONTEXT_NOT_REPLAY"
        verdict = "ROW2_REPLAY_AUTHORIZATION_NEEDS_MORE_CONTEXT"
        recommended_next_action = "provide_more_context_before_any_replay"

    write_csv(
        summary_out,
        [
            {
                "policy_id": "PAPER10_DESI_SHAPE_ROW2_REPLAY_AUTHORIZATION_REVIEW_V1",
                "status": status,
                "response_path": rel_or_abs(response_path),
                "response_sha256": sha256(response_path),
                "reviewed_package_sha256": package["zip_sha256"],
                "review_completed": "true",
                "question_count": str(len(rows)),
                "scope_decision": q1,
                "source_status_decision": q2,
                "endpoint_pair_blocker_decision": q3,
                "authorization_decision": q4,
                "claim_boundary_decision": q5,
                "forbidden_inputs_used": "false",
                "moresco_caveat_reduced": "true",
                "source_native_shape_caveat_reduced": "true",
                "row2_source_caveat_reduced": "true",
                "endpoint_pair_independence_satisfied": "false",
                "row2_promotion_ready": "false",
                "shape_route_promotion_allowed": "false",
                "separate_replay_authorization_review_allowed": "true",
                "endpoint_replay_allowed": endpoint_replay_allowed,
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "authorization_scope": "single_permission_only_DESI_shape_row2_replay_later_not_validation_not_promotion",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
                "recommended_next_action": recommended_next_action,
            }
        ],
    )
    print(f"PAPER10_DESI_SHAPE_ROW2_REPLAY_AUTHORIZATION_RESPONSE_VALIDATED verdict={verdict}")


if __name__ == "__main__":
    main()

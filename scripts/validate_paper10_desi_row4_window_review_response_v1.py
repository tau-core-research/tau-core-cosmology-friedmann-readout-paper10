#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/paper10_desi_row4_window_review_response_v1.csv"
DEFAULT_SUMMARY_OUT = ROOT / "data/derived/paper10_desi_row4_window_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_row4_window_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row4_window_review_not_validation"
EXPECTED_QUESTIONS = {
    "Q1_STRICT_WINDOW_STATUS",
    "Q2_MORESCO_2015_ELIGIBILITY",
    "Q3_RELEASE_POLICY",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed DESI row-4 source-window review response."
    )
    parser.add_argument("response", nargs="?", default=str(DEFAULT_RESPONSE))
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY_OUT))
    return parser.parse_args()


def resolve_path(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path


def rel_or_abs(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
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


def main() -> None:
    args = parse_args()
    response_path = resolve_path(args.response)
    summary_out = resolve_path(args.summary_out)

    package_summary = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)

    require(package_summary["status"] == "DESI_ROW4_WINDOW_REVIEW_PACKAGE_BUILT_NOT_COMPLETED", "bad package status")
    require(package_summary["review_completed"] == "false", "source package must have been blank before response")
    require(package_summary["row4_can_enter_replay"] == "false", "source package must not have released row4")
    require(package_summary["endpoint_replay_allowed"] == "false", "source package must not authorize replay")
    require(package_summary["endpoint_validation_claimed"] == "false", "source package must not claim validation")
    require(package_summary["physical_validation_claimed"] == "false", "source package must not claim physical validation")
    require(package_summary["contains_endpoint_residuals"] == "false", "source package must not contain residuals")
    require(package_summary["contains_endpoint_scores"] == "false", "source package must not contain scores")
    require(package_summary["contains_fit_statistics"] == "false", "source package must not contain fit statistics")
    require(package_summary["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")

    require(len(rows) == len(EXPECTED_QUESTIONS), "completed response must contain exactly three rows")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == EXPECTED_QUESTIONS, "completed response question ids mismatch")
    for row in rows:
        require(row["review_completed"] == "true", f"{row['question_id']}: review_completed must be true")
        require(nonempty(row.get("reviewer_id_or_role", "")), f"{row['question_id']}: reviewer_id_or_role required")
        require(nonempty(row.get("reviewer_response", "")), f"{row['question_id']}: reviewer_response required")
        require(nonempty(row.get("reviewer_rationale", "")), f"{row['question_id']}: reviewer_rationale required")
        require(row["forbidden_inputs_used"] == "false", f"{row['question_id']}: forbidden inputs must remain false")
        require(row["endpoint_replay_allowed"] == "false", f"{row['question_id']}: replay must remain disabled")
        require(row["endpoint_validation_claimed"] == "false", f"{row['question_id']}: endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", f"{row['question_id']}: physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{row['question_id']}: claim boundary mismatch")

    q1 = by_id["Q1_STRICT_WINDOW_STATUS"]["reviewer_response"]
    q2 = by_id["Q2_MORESCO_2015_ELIGIBILITY"]["reviewer_response"]
    q3 = by_id["Q3_RELEASE_POLICY"]["reviewer_response"]

    require(q1 in {"KEEP_STRICT_WINDOW", "ALLOW_CAVEATED_WINDOW_EXTENSION", "REJECT_REOPEN"}, "Q1 decision invalid")
    require(q2 in {"ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE", "RETAIN_AS_CONTEXT_ONLY", "REJECT_SOURCE"}, "Q2 decision invalid")
    require(q3 in {"SOURCE_REOPEN_ONLY_NO_REPLAY", "AUTHORIZE_REPLAY_REVIEW_REQUIRED", "NO_RELEASE"}, "Q3 decision invalid")

    if q1 == "KEEP_STRICT_WINDOW":
        require(q2 != "ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE", "strict window cannot accept the near-window source")
        require(q3 == "NO_RELEASE", "strict window must keep no-release consequence")
    if q1 == "REJECT_REOPEN":
        require(q2 == "REJECT_SOURCE", "reject-reopen requires source rejection")
        require(q3 == "NO_RELEASE", "reject-reopen requires no release")
    if q2 == "ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE":
        require(q1 == "ALLOW_CAVEATED_WINDOW_EXTENSION", "accepting Moresco 2015 requires caveated window extension")
        require(q3 in {"SOURCE_REOPEN_ONLY_NO_REPLAY", "AUTHORIZE_REPLAY_REVIEW_REQUIRED"}, "accepted source cannot map to NO_RELEASE")
        require(
            nonempty(by_id["Q2_MORESCO_2015_ELIGIBILITY"].get("source_reference_or_url", "")),
            "accepted Moresco 2015 source requires source_reference_or_url",
        )
    if q3 == "AUTHORIZE_REPLAY_REVIEW_REQUIRED":
        require(q2 == "ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE", "replay-review request requires accepted caveated source")

    source_reopen = q1 == "ALLOW_CAVEATED_WINDOW_EXTENSION" and q2 == "ACCEPT_AS_CAVEATED_NEAR_WINDOW_SOURCE"
    replay_review_required = source_reopen and q3 == "AUTHORIZE_REPLAY_REVIEW_REQUIRED"
    blocker_status = "ROW4_SOURCE_REOPEN_CAVEATED_NO_REPLAY" if source_reopen else "ROW4_WINDOW_BLOCKER_REMAINS"
    status = (
        "DESI_ROW4_WINDOW_REVIEW_IMPORTED_CAVEATED_SOURCE_REOPEN_NOT_REPLAY"
        if source_reopen
        else "DESI_ROW4_WINDOW_REVIEW_IMPORTED_BLOCKER_REMAINS_NOT_REPLAY"
    )
    verdict = (
        "row4_window_review_caveated_source_reopen_no_replay"
        if source_reopen
        else "row4_window_review_keeps_blocker_no_replay"
    )

    output = [
        {
            "policy_id": "PAPER10_DESI_ROW4_WINDOW_REVIEW_POLICY_V1",
            "status": status,
            "response_path": rel_or_abs(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package_summary["zip_sha256"],
            "review_completed": "true",
            "strict_window_decision": q1,
            "moresco_2015_eligibility": q2,
            "release_policy": q3,
            "source_reopen_caveated": "true" if source_reopen else "false",
            "row4_blocker_status": blocker_status,
            "replay_review_required_before_endpoint": "true" if replay_review_required else "false",
            "row4_can_enter_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": verdict,
            "recommended_next_action": (
                "prepare_separate_row4_replay_authorization_handoff_only_if_needed"
                if replay_review_required
                else "keep_row4_blocked_or_record_caveated_source_reopen_without_replay"
            ),
        }
    ]
    write_csv(summary_out, output)
    print(f"PAPER10_DESI_ROW4_WINDOW_REVIEW_RESPONSE_VALIDATED verdict={verdict}")


if __name__ == "__main__":
    main()

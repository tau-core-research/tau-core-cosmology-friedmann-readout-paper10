#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/paper10_desi_row5_high_z_review_response_v1.csv"
DEFAULT_SUMMARY_OUT = ROOT / "data/derived/paper10_desi_row5_high_z_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_row5_high_z_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row5_high_z_review_not_validation"
EXPECTED_QUESTIONS = {
    "Q1_HIGH_Z_CLOCK_SOURCE",
    "Q2_SOURCE_NATIVE_TIME_READOUT",
    "Q3_RELEASE_POLICY",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed DESI row-5 high-z source review response."
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

    require(package_summary["status"] == "DESI_ROW5_HIGH_Z_REVIEW_PACKAGE_BUILT_NOT_COMPLETED", "bad package status")
    require(package_summary["review_completed"] == "false", "source package must have been blank before response")
    require(package_summary["desi_time_route_endpoint_ready"] == "false", "source package must not be endpoint-ready")
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

    q1 = by_id["Q1_HIGH_Z_CLOCK_SOURCE"]["reviewer_response"]
    q2 = by_id["Q2_SOURCE_NATIVE_TIME_READOUT"]["reviewer_response"]
    q3 = by_id["Q3_RELEASE_POLICY"]["reviewer_response"]

    require(q1 in {"ACCEPT_HIGH_Z_CLOCK_SOURCE", "NO_HIGH_Z_CLOCK_SOURCE", "CAVEATED_CONTEXT_ONLY"}, "Q1 decision invalid")
    require(
        q2 in {
            "ACCEPT_SOURCE_NATIVE_TIME_READOUT_CANDIDATE",
            "RETAIN_AS_CROSS_PROBE_CONTEXT_ONLY",
            "REJECT_ROUTE",
        },
        "Q2 decision invalid",
    )
    require(q3 in {"SOURCE_REOPEN_ONLY_NO_REPLAY", "AUTHORIZE_REPLAY_REVIEW_REQUIRED", "NO_RELEASE"}, "Q3 decision invalid")

    clock_accepted = q1 == "ACCEPT_HIGH_Z_CLOCK_SOURCE"
    time_readout_accepted = q2 == "ACCEPT_SOURCE_NATIVE_TIME_READOUT_CANDIDATE"
    source_reopen = clock_accepted or time_readout_accepted
    replay_review_required = source_reopen and q3 == "AUTHORIZE_REPLAY_REVIEW_REQUIRED"

    if q1 in {"NO_HIGH_Z_CLOCK_SOURCE", "CAVEATED_CONTEXT_ONLY"} and q2 != "ACCEPT_SOURCE_NATIVE_TIME_READOUT_CANDIDATE":
        require(q3 == "NO_RELEASE", "no accepted source route must map to NO_RELEASE")
    if clock_accepted:
        require(nonempty(by_id["Q1_HIGH_Z_CLOCK_SOURCE"].get("source_reference_or_url", "")), "accepted high-z clock requires source reference")
        require(nonempty(by_id["Q1_HIGH_Z_CLOCK_SOURCE"].get("source_redshift_or_range", "")), "accepted high-z clock requires redshift/range")
        require(q3 in {"SOURCE_REOPEN_ONLY_NO_REPLAY", "AUTHORIZE_REPLAY_REVIEW_REQUIRED"}, "accepted clock cannot map to NO_RELEASE")
    if time_readout_accepted:
        require(nonempty(by_id["Q2_SOURCE_NATIVE_TIME_READOUT"].get("source_reference_or_url", "")), "accepted time/readout route requires source reference")
        require(nonempty(by_id["Q2_SOURCE_NATIVE_TIME_READOUT"].get("source_redshift_or_range", "")), "accepted time/readout route requires redshift/range")
        require(q3 in {"SOURCE_REOPEN_ONLY_NO_REPLAY", "AUTHORIZE_REPLAY_REVIEW_REQUIRED"}, "accepted time/readout cannot map to NO_RELEASE")
    if q3 == "AUTHORIZE_REPLAY_REVIEW_REQUIRED":
        require(source_reopen, "replay-review request requires accepted source route")

    status = (
        "DESI_ROW5_HIGH_Z_REVIEW_IMPORTED_SOURCE_REOPEN_NOT_REPLAY"
        if source_reopen
        else "DESI_ROW5_HIGH_Z_REVIEW_IMPORTED_BLOCKER_REMAINS_NOT_REPLAY"
    )
    row5_blocker_status = "ROW5_SOURCE_REOPENED_REPLAY_REVIEW_REQUIRED" if source_reopen else "ROW5_HIGH_Z_BLOCKER_REMAINS"
    verdict = (
        "row5_high_z_review_source_reopen_no_replay"
        if source_reopen
        else "row5_high_z_review_keeps_blocker_no_replay"
    )

    output = [
        {
            "policy_id": "PAPER10_DESI_ROW5_HIGH_Z_REVIEW_POLICY_V1",
            "status": status,
            "response_path": rel_or_abs(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package_summary["zip_sha256"],
            "review_completed": "true",
            "high_z_clock_source_decision": q1,
            "source_native_time_readout_decision": q2,
            "release_policy": q3,
            "source_reopen": "true" if source_reopen else "false",
            "accepted_clock_source": "true" if clock_accepted else "false",
            "accepted_source_native_time_readout": "true" if time_readout_accepted else "false",
            "row5_blocker_status": row5_blocker_status,
            "replay_review_required_before_endpoint": "true" if replay_review_required else "false",
            "row5_can_enter_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": verdict,
            "recommended_next_action": (
                "prepare_separate_row5_replay_authorization_handoff_only_if_needed"
                if replay_review_required
                else "keep_row5_blocked_or_record_source_reopen_without_replay"
            ),
        }
    ]
    write_csv(summary_out, output)
    print(f"PAPER10_DESI_ROW5_HIGH_Z_REVIEW_RESPONSE_VALIDATED verdict={verdict}")


if __name__ == "__main__":
    main()

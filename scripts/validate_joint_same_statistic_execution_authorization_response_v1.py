#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_same_statistic_execution_authorization_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_same_statistic_execution_authorization_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_same_statistic_execution_authorization_package_v1_summary.csv"
PACKAGE_ID = "JOINT_SAME_STATISTIC_EXECUTION_AUTHORIZATION_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_same_statistic_execution_authorization_not_validation"
EXPECTED = {
    "JSSE_Q1_EXECUTION_SCOPE": "authorize_one_permission_only_execution",
    "JSSE_Q2_SAME_STATISTIC_BINDING": "accept_same_statistic_execution_binding",
    "JSSE_Q3_CAVEATS": "accept_caveated_output_boundary",
    "JSSE_Q4_NO_VALIDATION": "accept_permission_only_no_validation",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate completed same-statistic execution authorization response.")
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


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response)
    summary_out = resolve(args.summary_out)
    package = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)
    if package["status"] != "JOINT_SAME_STATISTIC_EXECUTION_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("unexpected package status")
    if package["review_completed"] != "false":
        raise SystemExit("upstream package must be an uncompleted handoff")
    if len(rows) != len(EXPECTED):
        raise SystemExit("response must contain four rows")
    if {row["question_id"] for row in rows} != set(EXPECTED):
        raise SystemExit("question ids mismatch")

    accepted = True
    rejected = 0
    for row in rows:
        qid = row["question_id"]
        if row["review_id"] != PACKAGE_ID:
            raise SystemExit(f"{qid}: bad review_id")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{qid}: claim boundary mismatch")
        if row["review_completed"] != "true":
            raise SystemExit(f"{qid}: review must be completed")
        if not row["reviewer_id_or_role"].strip() or not row["reviewer_rationale"].strip():
            raise SystemExit(f"{qid}: reviewer id and rationale required")
        if norm(row["forbidden_inputs_used"]) != "false":
            raise SystemExit(f"{qid}: forbidden inputs used")
        for field in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
            if norm(row[field]) != "false":
                raise SystemExit(f"{qid}: unsafe field {field}")
        value = row["reviewer_response"].strip()
        if value == "reject":
            accepted = False
            rejected += 1
        elif value != EXPECTED[qid]:
            raise SystemExit(f"{qid}: unsupported reviewer_response {value}")

    if accepted:
        if {norm(row["permission_only_execution_allowed"]) for row in rows} != {"true"}:
            raise SystemExit("accepted response must set permission_only_execution_allowed=true on all rows")
        decision = "AUTHORIZE_SAME_STATISTIC_PERMISSION_ONLY_EXECUTION_NOT_VALIDATION"
        next_action = "run_same_statistic_permission_only_replay_once_and_validate_outputs"
    else:
        decision = "SAME_STATISTIC_EXECUTION_AUTHORIZATION_REJECTED_NOT_RUN"
        next_action = "keep_same_statistic_execution_blocked_or_revise_authorization_package"

    summary = {
        "run_id": "JOINT_SAME_STATISTIC_EXECUTION_AUTHORIZATION_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "accepted_rows": str(len(rows) - rejected),
        "rejected_rows": str(rejected),
        "forbidden_inputs_used": "false",
        "permission_only_execution_allowed": "true" if accepted else "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "decision": decision,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(f"JOINT_SAME_STATISTIC_EXECUTION_AUTHORIZATION_RESPONSE_V1_VALIDATED decision={decision}")


if __name__ == "__main__":
    main()

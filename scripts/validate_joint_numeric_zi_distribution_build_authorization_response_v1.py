#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_response_v1.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_build_authorization_package_v1_summary.csv"
PACKAGE_ID = "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_numeric_zi_distribution_build_authorization_not_scoring_not_validation"
EXPECTED = {
    "NZD_Q1_SCOPE": {
        "authorize_distribution_build",
        "AUTHORIZE_NUMERIC_ZI_DISTRIBUTION_BUILD_ONLY_NOT_TJOINT",
    },
    "NZD_Q2_CAVEATS": {
        "accept_caveated_distribution_boundary",
        "ACCEPT_CAVEATED_DISTRIBUTION_BOUNDARY",
    },
    "NZD_Q3_FROZEN_RULE": {
        "accept_frozen_center_scale_rule",
        "ACCEPT_FROZEN_MEDIAN_MAD_CONTROL_ONLY_RULE",
    },
    "NZD_Q4_NO_PROMOTION": {
        "accept_no_t_joint_promotion",
        "ACCEPT_NO_TJOINT_PROMOTION_DISTRIBUTION_LEDGER_ONLY",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate completed numeric z_i distribution-build authorization response."
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


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response)
    summary_out = resolve(args.summary_out)
    package = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)

    if package["status"] != "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("unexpected numeric z_i authorization package status")
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
        if norm(row["review_completed"]) != "true":
            raise SystemExit(f"{qid}: review must be completed")
        if not row["reviewer_id_or_role"].strip() or not row["reviewer_rationale"].strip():
            raise SystemExit(f"{qid}: reviewer id and rationale required")
        if norm(row["forbidden_inputs_used"]) != "false":
            raise SystemExit(f"{qid}: forbidden inputs used")
        for field in [
            "numeric_t_joint_allowed",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            if norm(row[field]) != "false":
                raise SystemExit(f"{qid}: unsafe field {field}")
        value = row["reviewer_response"].strip()
        if value == "reject":
            accepted = False
            rejected += 1
        elif value not in EXPECTED[qid]:
            raise SystemExit(f"{qid}: unsupported reviewer_response {value}")

    if accepted:
        if {norm(row["numeric_zi_build_allowed"]) for row in rows} != {"true"}:
            raise SystemExit("accepted response must set numeric_zi_build_allowed=true on all rows")
        decision = "AUTHORIZE_NUMERIC_ZI_DISTRIBUTION_BUILD_NOT_TJOINT_NOT_VALIDATION"
        next_action = "build_numeric_zi_distribution_ledger_without_t_joint_scoring"
        verdict = "numeric_zi_distribution_build_authorized_not_tjoint_not_validation"
    else:
        decision = "REJECT_OR_INCOMPLETE_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION"
        next_action = "keep_numeric_zi_build_blocked_or_revise_authorization_package"
        verdict = "numeric_zi_distribution_build_not_authorized"

    summary = {
        "run_id": "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION_RESPONSE_V1",
        "response_path": rel_or_abs(response_path),
        "response_sha256": sha256(response_path),
        "question_count": str(len(rows)),
        "accepted_rows": str(len(rows) - rejected),
        "rejected_rows": str(rejected),
        "review_completed": "true",
        "forbidden_inputs_used": "false",
        "numeric_zi_build_allowed": "true" if accepted else "false",
        "numeric_t_joint_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "decision": decision,
        "next_action": next_action,
        "verdict": verdict,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(summary_out, summary)
    print(f"JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_AUTHORIZATION_RESPONSE_V1_VALIDATED decision={decision}")


if __name__ == "__main__":
    main()

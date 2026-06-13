#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_authorization_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_authorization_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_authorization_review_package_v1_summary.csv"
)
PACKAGE_ID = "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_replay_authorization_review_not_validation"
EXPECTED = {
    "Q1_source_product": {"accept", "accept_with_caveat", "reject"},
    "Q2_sampling_and_mask": {"accept", "accept_with_caveat", "reject"},
    "Q3_normalization_rule": {"accept", "accept_with_caveat", "reject"},
    "Q4_null_controls": {"accept", "accept_with_caveat", "reject"},
    "Q5_replay_permission": {"authorize_replay_as_caveated_candidate", "do_not_authorize_replay"},
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value: str) -> str:
    return str(value).strip().lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed ACT DR6 lensing path-weight replay authorization response."
    )
    parser.add_argument("response", nargs="?", default=str(DEFAULT_RESPONSE))
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    response_path = Path(args.response)
    if not response_path.is_absolute():
        response_path = ROOT / response_path
    summary_out = Path(args.summary_out)
    if not summary_out.is_absolute():
        summary_out = ROOT / summary_out

    package = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)
    if package["package_id"] != PACKAGE_ID:
        raise SystemExit("package id mismatch")
    if package["status"] != "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED":
        raise SystemExit("bad package status")
    if package["review_completed"] != "false":
        raise SystemExit("package must be uncompleted handoff")
    for key in (
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "contains_endpoint_residuals",
        "contains_endpoint_scores",
        "contains_fit_statistics",
        "physical_lensing_path_weight_claimed",
    ):
        if package[key] != "false":
            raise SystemExit(f"package must keep {key}=false")
    if package["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("package claim boundary mismatch")

    if len(rows) != len(EXPECTED):
        raise SystemExit("completed response must contain exactly five rows")
    by_id = {row["question_id"]: row for row in rows}
    if set(by_id) != set(EXPECTED):
        raise SystemExit("completed response question ids mismatch")

    forbidden_inputs_used = False
    rejected = []
    caveated = []
    for question_id, allowed in EXPECTED.items():
        row = by_id[question_id]
        answer = norm(row["reviewer_answer"])
        if answer not in allowed:
            raise SystemExit(f"{question_id}: invalid reviewer_answer={row['reviewer_answer']!r}")
        if not row["reviewer_notes"].strip():
            raise SystemExit(f"{question_id}: reviewer_notes must be filled")
        if norm(row["forbidden_inputs_used"]) != "false":
            forbidden_inputs_used = True
        for key in ("endpoint_replay_allowed", "endpoint_validation_claimed", "physical_lensing_path_weight_claimed"):
            if norm(row[key]) != "false":
                raise SystemExit(f"{question_id}: {key} must remain false in the review response")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{question_id}: claim boundary mismatch")
        if answer == "reject":
            rejected.append(question_id)
        if answer == "accept_with_caveat":
            caveated.append(question_id)

    authorized = (
        not forbidden_inputs_used
        and not rejected
        and norm(by_id["Q5_replay_permission"]["reviewer_answer"]) == "authorize_replay_as_caveated_candidate"
    )
    status = (
        "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_ACCEPTED_CAVEATED_NOT_VALIDATION"
        if authorized
        else "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_NOT_ACCEPTED_NO_REPLAY"
    )
    summary = {
        "package_id": PACKAGE_ID,
        "status": status,
        "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
        "response_sha256": sha256(response_path),
        "reviewed_package_sha256": package["zip_sha256"],
        "review_completed": "true",
        "question_count": str(len(rows)),
        "rejected_question_count": str(len(rejected)),
        "caveated_question_count": str(len(caveated)),
        "forbidden_inputs_used": str(forbidden_inputs_used).lower(),
        "permission_only_replay_authorized": str(authorized).lower(),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "contains_endpoint_residuals": "false",
        "contains_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": (
            "act_dr6_lensing_path_weight_caveated_replay_authorized_not_validation"
            if authorized
            else "act_dr6_lensing_path_weight_replay_not_authorized"
        ),
        "recommended_next_action": (
            "run_guarded_replay_with_null_controls_do_not_claim_validation"
            if authorized
            else "do_not_run_replay_return_to_source_side_review"
        ),
    }
    write_csv(summary_out, [summary])
    print(
        "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_AUTHORIZATION_RESPONSE_VALIDATED "
        f"authorized={summary['permission_only_replay_authorized']}"
    )


if __name__ == "__main__":
    main()

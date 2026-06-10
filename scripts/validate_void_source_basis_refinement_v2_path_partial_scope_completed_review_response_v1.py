#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1.csv"
)
DEFAULT_SUMMARY_OUT = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_summary.csv"
)
PROVIDED_COMPLETED_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_completed_review_summary_v1.csv"
)

REQUIRED_RESPONSES = {
    "Q1_NO_ENDPOINT_LEAKAGE": {"yes"},
    "Q2_SCOPE_LABELS": {"yes", "caveated_yes"},
    "Q3_VALUE_RULE": {"yes", "caveated_yes"},
    "Q4_FUTURE_REPLAY_PACKAGE": {"yes", "caveated_yes"},
    "FINAL_VERDICT": {"ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE"},
}


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate completed V2 partial W_path source-side reviewer response."
    )
    parser.add_argument("response", nargs="?", default=str(DEFAULT_RESPONSE))
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY_OUT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    response_path = Path(args.response)
    if not response_path.is_absolute():
        response_path = ROOT / response_path
    summary_out = Path(args.summary_out)
    if not summary_out.is_absolute():
        summary_out = ROOT / summary_out

    package_summary = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)
    provided_summary = read_one(PROVIDED_COMPLETED_SUMMARY) if PROVIDED_COMPLETED_SUMMARY.exists() else {}
    require(package_summary["status"] == "V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_BUILT_NOT_COMPLETED", "bad package status")
    require(package_summary["endpoint_replay_allowed"] == "false", "package must not authorize replay")
    require(package_summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(len(rows) == len(REQUIRED_RESPONSES), "completed response must contain exactly the required rows")
    by_id = {row["review_item_id"]: row for row in rows}
    require(set(by_id) == set(REQUIRED_RESPONSES), "completed response question ids mismatch")
    for question_id, allowed in REQUIRED_RESPONSES.items():
        row = by_id[question_id]
        require(row["reviewer_response"] in allowed, f"bad response for {question_id}")
        require(row["forbidden_inputs_used"] == "false", f"{question_id} must keep forbidden_inputs_used=false")
        require(row["endpoint_replay_allowed"] == "false", f"{question_id} must keep endpoint_replay_allowed=false")
        require(row["endpoint_validation_claimed"] == "false", f"{question_id} must keep endpoint_validation_claimed=false")
        require(row["reviewer_notes"].strip(), f"{question_id} must include reviewer notes")

    final_verdict = by_id["FINAL_VERDICT"]["reviewer_response"]
    if provided_summary:
        require(provided_summary["review_completed"] == "true", "provided summary must mark review complete")
        require(provided_summary["final_verdict"] == final_verdict, "provided summary verdict mismatch")
        require(
            provided_summary["source_package_sha256"] == package_summary["zip_sha256"],
            "completed summary source package checksum mismatch",
        )
        for key in [
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "forbidden_inputs_used",
            "physical_lensing_path_weight_claimed",
        ]:
            require(provided_summary[key] == "false", f"provided summary must keep {key}=false")
        require(
            provided_summary["future_action_allowed"]
            == "prepare_separate_partial_scope_replay_authorization_package_only",
            "future action must remain authorization-package-only",
        )

    summary = [
        {
            "review_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_REVIEW_COMPLETED_V1",
            "source_package": package_summary["zip_path"],
            "source_package_sha256": package_summary["zip_sha256"],
            "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
            "review_completed": "true",
            "final_verdict": final_verdict,
            "acceptance_scope": "partial_scope_12_row_W_path_source_side_control_only",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "forbidden_inputs_used": "false",
            "physical_lensing_path_weight_claimed": "false",
            "future_action_allowed": "prepare_separate_partial_scope_replay_authorization_package_only",
            "verdict": "partial_path_scope_control_accepted_as_caveated_source_side_only",
            "recommended_next_action": "prepare_separate_partial_scope_replay_authorization_package_if_needed",
            "claim_boundary": "v2_path_partial_scope_review_caveated_source_side_not_endpoint",
        }
    ]
    write_csv(summary_out, summary)
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_COMPLETED_REVIEW_RESPONSE_V1_VALIDATED "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

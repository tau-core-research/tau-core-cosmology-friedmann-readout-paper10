#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_response_v1.csv"
DEFAULT_SUMMARY_IN = ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_completed_summary_v1.csv"
DEFAULT_SUMMARY_OUT = ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_response_v1_summary.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_clock_support_blocker_external_review_not_validation"
EXPECTED_QUESTIONS = {
    "Q1_ROW4_Z1P484_CLOCK_SUPPORT",
    "Q2_ROW5_Z2P33_HIGH_Z_CLOCK_SUPPORT",
    "Q3_BAO_RSD_LYA_CONTROL_STATUS",
    "Q4_SOURCE_SIDE_ONLY_NO_REPLAY",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed DESI clock-support blocker external source-side review response."
    )
    parser.add_argument("response", nargs="?", default=str(DEFAULT_RESPONSE))
    parser.add_argument("--completed-summary", default=str(DEFAULT_SUMMARY_IN))
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


def read_metric_summary(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if not rows or set(rows[0]) != {"metric", "value"}:
        raise SystemExit("completed summary must use metric,value schema")
    return {row["metric"]: row["value"] for row in rows}


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


def main() -> None:
    args = parse_args()
    response_path = resolve_path(args.response)
    completed_summary_path = resolve_path(args.completed_summary)
    summary_out = resolve_path(args.summary_out)

    package_summary = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)
    completed_summary = read_metric_summary(completed_summary_path)

    require(
        package_summary["status"] == "DESI_CLOCK_SUPPORT_BLOCKER_EXTERNAL_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package_summary["review_completed"] == "false", "source package must have been blank before response")
    require(package_summary["active_blocker_count"] == "2", "source package must preserve two blockers")
    require(package_summary["candidate_scan_accepted_count"] == "0", "source package must not already close candidates")
    require(package_summary["endpoint_replay_allowed"] == "false", "source package must not authorize replay")
    require(package_summary["endpoint_validation_claimed"] == "false", "source package must not claim validation")
    require(package_summary["physical_validation_claimed"] == "false", "source package must not claim physical validation")
    require(package_summary["contains_endpoint_residuals"] == "false", "source package must not contain residuals")
    require(package_summary["contains_endpoint_scores"] == "false", "source package must not contain scores")
    require(package_summary["contains_fit_statistics"] == "false", "source package must not contain fit statistics")
    require(package_summary["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")

    require(len(rows) == len(EXPECTED_QUESTIONS), "completed response must contain exactly four rows")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == EXPECTED_QUESTIONS, "completed response question ids mismatch")
    for row in rows:
        require(row["forbidden_inputs_used"] == "false", f"{row['question_id']}: forbidden inputs must remain false")
        require(row["endpoint_replay_authorized"] == "false", f"{row['question_id']}: replay must remain unauthorized")
        require(row["endpoint_validation_claimed"] == "false", f"{row['question_id']}: endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", f"{row['question_id']}: physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{row['question_id']}: claim boundary mismatch")

    require(
        by_id["Q1_ROW4_Z1P484_CLOCK_SUPPORT"]["decision"]
        == "CAVEATED_YES_ROW4_SOURCE_ACQUISITION_GATE_CAN_REOPEN",
        "row 4 must be caveated reopen only",
    )
    require(by_id["Q1_ROW4_Z1P484_CLOCK_SUPPORT"]["z_eff"] == "1.484", "row 4 z_eff mismatch")
    require(
        "z=1.43" in by_id["Q1_ROW4_Z1P484_CLOCK_SUPPORT"]["source_side_finding"]
        and "z=1.53" in by_id["Q1_ROW4_Z1P484_CLOCK_SUPPORT"]["source_side_finding"],
        "row 4 caveated source finding must record bracketing CC entries",
    )
    require(
        by_id["Q2_ROW5_Z2P33_HIGH_Z_CLOCK_SUPPORT"]["decision"]
        == "NO_ROW5_REMAINS_BLOCKED_CLOCK_SUPPORT_NOT_FROZEN",
        "row 5 must remain blocked",
    )
    require(by_id["Q2_ROW5_Z2P33_HIGH_Z_CLOCK_SUPPORT"]["z_eff"] == "2.33", "row 5 z_eff mismatch")
    require(
        by_id["Q3_BAO_RSD_LYA_CONTROL_STATUS"]["decision"]
        == "YES_KEEP_BAO_RSD_LYA_AS_CONTEXT_CONTROLS_UNLESS_CLOCK_ATTACHED",
        "BAO/RSD/Ly-alpha policy mismatch",
    )
    require(
        by_id["Q4_SOURCE_SIDE_ONLY_NO_REPLAY"]["decision"] == "YES_SOURCE_SIDE_ONLY_NO_ENDPOINT_REPLAY_AUTHORIZED",
        "source-side/no-replay boundary mismatch",
    )

    require(
        completed_summary["overall_decision"] == "PARTIAL_SOURCE_ACQUISITION_REOPEN_ROW4_KEEP_ROW5_BLOCKED_NO_REPLAY",
        "overall decision mismatch",
    )
    require(completed_summary["review_completed"] == "true", "review must be completed")
    require(completed_summary["questions_reviewed"] == "4", "question count mismatch")
    require(completed_summary["forbidden_inputs_used"] == "false", "summary forbidden inputs mismatch")
    require(completed_summary["endpoint_replay_authorized"] == "false", "summary replay flag mismatch")
    require(completed_summary["endpoint_validation_claimed"] == "false", "summary validation flag mismatch")
    require(completed_summary["physical_validation_claimed"] == "false", "summary physical validation flag mismatch")
    require(completed_summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")

    accepted_reopen_count = "1"
    still_blocked_count = "1"
    output = [
        {
            "policy_id": "PAPER10_DESI_CLOCK_SUPPORT_BLOCKER_EXTERNAL_REVIEW_POLICY_V1",
            "status": "DESI_CLOCK_SUPPORT_BLOCKER_EXTERNAL_REVIEW_IMPORTED_PARTIAL_REOPEN_NOT_REPLAY",
            "decision": completed_summary["overall_decision"],
            "response_path": rel_or_abs(response_path),
            "response_sha256": sha256(response_path),
            "completed_summary_path": rel_or_abs(completed_summary_path),
            "completed_summary_sha256": sha256(completed_summary_path),
            "reviewed_package_sha256": package_summary["zip_sha256"],
            "review_completed": "true",
            "row4_source_acquisition_gate_can_reopen": "true",
            "row4_reopen_basis": "independent_CC_bracket_entries_z_1p43_and_z_1p53_reported_by_reviewer",
            "row5_remains_blocked": "true",
            "bao_rsd_lya_context_only": "true",
            "accepted_reopen_count": accepted_reopen_count,
            "still_blocked_count": still_blocked_count,
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": "build_row4_source_acquisition_reopen_manifest_no_replay_keep_row5_blocked",
        }
    ]
    write_csv(summary_out, output)
    print(
        "PAPER10_DESI_CLOCK_SUPPORT_BLOCKER_EXTERNAL_REVIEW_RESPONSE_VALIDATED "
        f"decision={output[0]['decision']}"
    )


if __name__ == "__main__":
    main()

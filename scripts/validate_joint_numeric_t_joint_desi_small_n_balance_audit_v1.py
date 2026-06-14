#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_desi_small_n_balance_audit_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_desi_small_n_balance_audit_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_desi_small_n_balance_audit_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_desi_small_n_balance_audit_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(rows) == 4, "expected four small-N audit checks")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "wrong claim boundary")
    require(summary["candidate_survives_controls"] == "true", "candidate should survive local controls")
    require(summary["small_n_balance_status"] == "CAVEATED_BALANCE_ONLY_NOT_PENALTY_READY", "bad balance status")
    require(summary["penalty_admissible_now"] == "false", "penalty must remain inadmissible")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(float(summary["candidate_minus_best_control_score_fraction"]) < 0.01, "margin caveat expected")
    require(float(summary["max_leave_one_fraction_of_full_candidate"]) > 0.95, "row-sensitivity caveat expected")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["rescoring_allowed"] == "false", "row rescoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "small-N", "row-sensitive", "inadmissible"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_DESI_SMALL_N_BALANCE_AUDIT_V1_VALIDATED "
        f"open={summary['checks_open_or_caveated']}"
    )


if __name__ == "__main__":
    main()

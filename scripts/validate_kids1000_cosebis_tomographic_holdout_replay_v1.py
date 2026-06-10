#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_holdout_replay_policy_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(GRID)
    summary = read_one(SUMMARY)
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(policy["explicit_user_approval_recorded"] == "true", "policy must record explicit user approval")
    require("using_holdout_score_for_source_selection" in policy["forbidden_inputs"], "holdout score leakage must be forbidden")
    require(summary["status"] == "TOMOGRAPHIC_HOLDOUT_REPLAY_COMPLETE", "unexpected summary status")
    require(summary["fold_count"] == "5", "expected five source-bin holdout folds")
    require(summary["comparison_branch_count"] == "4", "expected candidate plus three candidate-beating controls")
    require(summary["candidate_holdout_improved_fold_count"] == "4", "candidate should improve four of five folds")
    require(summary["candidate_rank_by_total_holdout_delta_chi2"] == "2", "candidate should rank second in this caveated comparison")
    require(summary["candidate_beating_control_count"] == "1", "one tomographic control should still beat the candidate")
    require(summary["holdout_replay_refutes_endpoint_signal"] == "false", "holdout replay must not refute endpoint signal")
    require(summary["tomographic_controls_block_validation"] == "true", "tomographic control caveat must remain active")
    require(summary["computes_new_labels"] == "false", "holdout replay must not compute new labels")
    require(summary["uses_kids_data_vector_values_for_source_selection"] == "false", "source selection must not use KiDS values")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(
        summary["verdict"] == "holdout_replay_preserves_signal_but_tomographic_control_caveat_remains",
        "unexpected verdict",
    )
    require(len(rows) == 20, "expected 4 branches x 5 folds")
    candidate_rows = [row for row in rows if row["branch"] == "source_frozen_web_path_candidate"]
    require(len(candidate_rows) == 5, "candidate must have five fold rows")
    for row in rows:
        require(row["uses_kids_data_vector_values_for_source_selection"] == "false", "no source-selection leakage allowed")
        require(row["endpoint_validation_claimed"] == "false", "no row may claim validation")
        require(row["claim_boundary"] == policy["claim_boundary"], "claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_HOLDOUT_REPLAY_V1_VALIDATED "
        f"candidate_folds={summary['candidate_holdout_improved_fold_count']}/{summary['fold_count']} "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

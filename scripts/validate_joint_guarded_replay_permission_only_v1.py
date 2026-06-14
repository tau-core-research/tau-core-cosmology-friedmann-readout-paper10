#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "data/derived/joint_guarded_replay_permission_only_grid_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_permission_only_summary_v1.csv"
DOC = ROOT / "docs/joint_guarded_replay_permission_only_v1.md"
CLAIM_BOUNDARY = "joint_guarded_replay_permission_only_not_validation"
REQUIRED_BLOCKS = {
    "kids_lensing_cosebis_low_mode",
    "observer_path_basis_low_z",
    "desi_shape_time_readout",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    grid = read_rows(GRID)
    summary = read_one(SUMMARY)
    require(summary["status"] == "JOINT_GUARDED_REPLAY_PERMISSION_ONLY_COMPLETE_NOT_VALIDATION", "bad status")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require({row["block_id"] for row in grid} == REQUIRED_BLOCKS, "active block set mismatch")
    require(summary["active_block_count"] == str(len(REQUIRED_BLOCKS)), "active block count mismatch")
    for key in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
        require(summary[key] == "false", f"{key} must remain false")
    require(summary["permission_only_execution_allowed"] == "true", "permission-only execution flag missing")
    require(summary["candidate_control_same_statistic_required"] == "true", "same-statistic rule missing")
    require(summary["candidate_control_same_covariance_required"] == "true", "same-covariance rule missing")
    require(summary["block_diagonal_independence_caveated"] == "true", "block-diagonal caveat missing")
    require(summary["verdict"] == "joint_guarded_replay_permission_only_executed_not_validation", "unexpected verdict")
    text = DOC.read_text()
    for marker in ["permission-only", "not endpoint validation", "not cosmological validation", CLAIM_BOUNDARY]:
        require(marker in text, f"doc missing marker: {marker}")
    print("JOINT_GUARDED_REPLAY_PERMISSION_ONLY_V1_VALIDATED not_validation=true")


if __name__ == "__main__":
    main()

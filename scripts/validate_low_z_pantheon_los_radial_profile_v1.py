#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_los_radial_profile_policy_v1.csv"
PROFILE = ROOT / "data/derived/low_z_pantheon_los_radial_profile_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_los_radial_profile_v1_summary.csv"
CLAIM_BOUNDARY = "los_radial_profile_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(PROFILE)
    summary = read_one(SUMMARY)
    require(policy["status"] == "LOS_RADIAL_PROFILE_SOURCE_SIDE_NOT_SCORING", "bad policy status")
    require(policy["endpoint_replay_allowed"] == "false", "policy must not authorize replay")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "LOS_RADIAL_PROFILE_BUILT_SOURCE_SIDE_NOT_SCORING", "bad summary status")
    require(summary["rows"] == str(len(rows)), "row count mismatch")
    require(summary["rows"] == "424", "expected 424 low-z rows")
    require(summary["partial_path_scope_rows"] == "12", "expected 12 partial path scope rows")
    require(int(summary["shell_count"]) == 5, "expected five frozen shells")
    require(int(summary["nonempty_any_shell_rows"]) > 0, "profile should have nonempty rows")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim physical path")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    required_columns = [
        "foreground_far_count",
        "foreground_near_count",
        "near_source_count",
        "background_near_count",
        "background_far_count",
        "foreground_minus_background_density",
        "near_minus_far_density",
    ]
    for row in rows:
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["physical_lensing_path_weight_claimed"] == "false", "row must not claim physical path")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for col in required_columns:
            require(col in row, f"missing profile column: {col}")
        int(row["total_shell_count"])
        int(row["profile_nonempty_shell_count"])
    print(
        "PAPER10_LOS_RADIAL_PROFILE_VALIDATED "
        f"rows={summary['rows']} complete={summary['complete_profile_rows']} "
        f"partial_complete={summary['partial_path_scope_complete_profile_rows']}"
    )


if __name__ == "__main__":
    main()

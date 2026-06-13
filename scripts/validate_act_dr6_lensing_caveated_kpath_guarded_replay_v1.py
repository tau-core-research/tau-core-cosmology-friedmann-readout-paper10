#!/usr/bin/env python3
"""Validate the caveated ACT K_path guarded replay execution."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "data" / "derived" / "act_dr6_lensing_caveated_kpath_guarded_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_caveated_kpath_guarded_replay_v1_summary.csv"
CLAIM_BOUNDARY = "act_dr6_lensing_caveated_kpath_guarded_replay_permission_only_not_validation"
BRANCHES = {
    "baseline_only",
    "candidate",
    "off",
    "wrong_sign",
    "curl_null",
    "diff_f150_f090_null",
    "deterministic_shuffle",
    "rank_reverse",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def main() -> None:
    grid = read_rows(GRID)
    summary = read_one(SUMMARY)
    if summary["status"] != "GUARDED_REPLAY_EXECUTED_PERMISSION_ONLY_NOT_VALIDATION":
        raise SystemExit("bad guarded replay status")
    if set(row["branch"] for row in grid) != BRANCHES:
        raise SystemExit("branch set mismatch")
    if int(summary["grid_rows"]) != len(grid):
        raise SystemExit("grid row count mismatch")
    for key in (
        "permission_only_guarded_replay",
    ):
        if summary[key] != "true":
            raise SystemExit(f"summary must keep {key}=true")
    for key in (
        "endpoint_validation_claimed",
        "physical_lensing_path_weight_claimed",
        "dark_sector_inference_allowed",
        "family_verdict_allowed",
    ):
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    for row in grid:
        if row["permission_only_guarded_replay"] != "true":
            raise SystemExit("grid rows must record permission-only guarded replay")
        for key in (
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
            "dark_sector_inference_allowed",
            "family_verdict_allowed",
        ):
            if row[key] != "false":
                raise SystemExit(f"grid rows must keep {key}=false")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("grid claim boundary mismatch")
        float(row["chi2_act_path"]) if row["chi2_act_path"] != "inf" else float("inf")
        float(row["aic_act_path"]) if row["aic_act_path"] != "inf" else float("inf")
    print(f"ACT_CAVEATED_KPATH_GUARDED_REPLAY_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

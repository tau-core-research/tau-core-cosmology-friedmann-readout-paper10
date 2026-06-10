#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data" / "source_manifest" / "void_web_combined_multiblock_authorized_endpoint_run_v1.csv"
AUTH = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_response_v1_summary.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_grid.csv"
BLOCK_DROPS = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_block_drop.csv"

REQUIRED_BRANCHES = {
    "baseline_only",
    "source_native_void_web",
    "void_only",
    "web_only",
    "wrong_web_sign",
    "deterministic_shuffled_void_web",
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    run = read_one(RUN)
    auth = read_one(AUTH)
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)
    block_drops = read_rows(BLOCK_DROPS)

    require(run["endpoint_run_allowed"] == "true", "run manifest must allow endpoint run")
    require(run["physical_validation_claimed"] == "false", "run manifest must not claim validation")
    require(auth["decision"] == "GO_COMBINED_VOID_WEB_ENDPOINT_PERMISSION_ONLY", "authorization decision mismatch")
    require(auth["endpoint_run_allowed"] == "true", "authorization must allow endpoint run")
    require(auth["physical_validation_claimed"] == "false", "authorization must not claim validation")
    require(summary["status"] == "AUTHORIZED_COMBINED_VOID_WEB_ENDPOINT_COMPLETE_PERMISSION_ONLY", "summary status mismatch")
    require(summary["endpoint_run_allowed"] == "true", "summary must record endpoint run permission")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(
        summary["claim_boundary"] == "combined_void_web_endpoint_permission_only_not_validation",
        "summary claim boundary mismatch",
    )
    require(summary["cmb_safety_support_passed"] == "true", "CMB safety support must pass")
    require({row["combined_branch"] for row in grid} == REQUIRED_BRANCHES, "grid branch set mismatch")
    require({row["physical_validation_claimed"] for row in grid} == {"false"}, "grid must not claim validation")
    require(
        {row["claim_boundary"] for row in grid} == {"combined_void_web_endpoint_permission_only_not_validation"},
        "grid claim boundary mismatch",
    )
    require(len(block_drops) == len(REQUIRED_BRANCHES) * 3, "block-drop controls must cover each branch and block")
    require(
        {row["physical_validation_claimed"] for row in block_drops} == {"false"},
        "block-drop rows must not claim validation",
    )
    for key in [
        "baseline_best_chi2",
        "candidate_best_chi2",
        "candidate_delta_chi2_vs_baseline",
        "candidate_delta_aic_vs_baseline",
        "candidate_delta_bic_vs_baseline",
        "best_wrong_chi2",
    ]:
        float(summary[key])
    print(
        "PAPER10_VOID_WEB_COMBINED_MULTIBLOCK_AUTHORIZED_ENDPOINT_V1_VALIDATED "
        f"delta_aic={summary['candidate_delta_aic_vs_baseline']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()

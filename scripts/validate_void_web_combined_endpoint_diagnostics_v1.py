#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_endpoint_diagnostics_v1_summary.csv"
BRANCH = ROOT / "data" / "derived" / "void_web_combined_endpoint_diagnostics_v1_branch_summary.csv"
BLOCK = ROOT / "data" / "derived" / "void_web_combined_endpoint_diagnostics_v1_block_drop_summary.csv"


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
    summary = read_one(SUMMARY)
    branches = read_rows(BRANCH)
    blocks = read_rows(BLOCK)
    by_branch = {row["combined_branch"]: row for row in branches}
    require(summary["status"] == "DIAGNOSTIC_COMPLETE_NOT_VALIDATION", "diagnostic status mismatch")
    require(summary["physical_validation_claimed"] == "false", "diagnostic must not claim validation")
    require(summary["claim_boundary"] == "combined_endpoint_diagnostic_not_validation", "claim boundary mismatch")
    require(summary["candidate_void_channel_active_at_best"] == "false", "void channel should be inactive at best candidate")
    require(summary["candidate_web_channel_active_at_best"] == "true", "web channel should be active at best candidate")
    require(summary["candidate_equals_web_only_chi2"] == "true", "candidate should collapse to web-only at best")
    require(float(summary["candidate_delta_chi2_vs_baseline"]) < 0.0, "candidate must retain small chi2 improvement")
    require(float(summary["candidate_delta_aic_vs_baseline"]) > 0.0, "candidate must remain AIC-negative")
    require(float(summary["shuffled_minus_candidate_chi2"]) < 0.0, "shuffled control must remain marginally better")
    require(
        summary["dominant_failure_mode"] == "void_channel_inactive_and_shuffled_control_marginally_better",
        "dominant failure mode changed",
    )
    require(by_branch["source_native_void_web"]["void_channel_active_at_best"] == "false", "candidate void active flag mismatch")
    require(by_branch["source_native_void_web"]["web_channel_active_at_best"] == "true", "candidate web active flag mismatch")
    require({row["physical_validation_claimed"] for row in branches} == {"false"}, "branch rows must not claim validation")
    require({row["physical_validation_claimed"] for row in blocks} == {"false"}, "block rows must not claim validation")
    print(
        "PAPER10_VOID_WEB_COMBINED_ENDPOINT_DIAGNOSTICS_V1_VALIDATED "
        f"failure={summary['dominant_failure_mode']} "
        "claim_boundary=diagnostic_not_validation"
    )


if __name__ == "__main__":
    main()

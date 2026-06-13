#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRANCHES = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_branches.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_control_dominance_diagnostic_not_validation"
EXPECTED_BRANCHES = {
    "baseline_only",
    "candidate",
    "curl_null",
    "deterministic_shuffle",
    "diff_f150_f090_null",
    "off",
    "rank_reverse",
    "wrong_sign",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    summary_rows = read_rows(SUMMARY)
    branch_rows = read_rows(BRANCHES)
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["status"] == "CONTROL_DOMINANCE_DIAGNOSTIC_BUILT_NOT_VALIDATION", "bad status")
    require(summary["source_rows"] == "424", "unexpected source row count")
    require(summary["mask_positive_rows"] == "168", "unexpected mask-positive row count")
    require(summary["best_control_branch"] == "curl_null", "expected curl_null best control")
    require(summary["controls_better_than_candidate"] == "4", "expected four better controls")
    require(float(summary["candidate_delta_chi2_vs_baseline"]) < 0, "candidate should beat baseline in chi2")
    require(float(summary["candidate_delta_chi2_vs_best_control"]) > 0, "candidate should lose to best control")
    require(summary["endpoint_validation_claimed"] == "false", "must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "must not claim physical path weight")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    require(
        summary["verdict"] == "ACT_PATH_WEIGHT_WEAK_NON_SPECIFIC_SIGNAL_CONTROL_DOMINATED",
        "unexpected verdict",
    )
    require({row["branch"] for row in branch_rows} == EXPECTED_BRANCHES, "branch set mismatch")
    for row in branch_rows:
        require(row["endpoint_validation_claimed"] == "false", "branch row claims validation")
        require(row["physical_lensing_path_weight_claimed"] == "false", "branch row claims physical path weight")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "branch claim boundary mismatch")
        float(row["best_chi2_act_path"])
        float(row["delta_chi2_vs_candidate"])
    print(
        "ACT_DR6_LENSING_PATH_WEIGHT_CONTROL_DOMINANCE_DIAGNOSTIC_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

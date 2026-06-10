#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_grid.csv"
BLOCK_DROPS = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_block_drop.csv"
OUT_BRANCH = ROOT / "data" / "derived" / "void_web_combined_endpoint_diagnostics_v1_branch_summary.csv"
OUT_BLOCK = ROOT / "data" / "derived" / "void_web_combined_endpoint_diagnostics_v1_block_drop_summary.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "void_web_combined_endpoint_diagnostics_v1_summary.csv"


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


def f(value: str) -> float:
    return float(value)


def main() -> None:
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)
    block_drops = read_rows(BLOCK_DROPS)
    baseline = next(row for row in grid if row["combined_branch"] == "baseline_only" and row["chi2_total"] == summary["baseline_best_chi2"])
    best_by_branch: dict[str, dict[str, str]] = {}
    for row in grid:
        branch = row["combined_branch"]
        if branch not in best_by_branch or f(row["chi2_total"]) < f(best_by_branch[branch]["chi2_total"]):
            best_by_branch[branch] = row

    branch_rows: list[dict[str, str]] = []
    for branch, row in sorted(best_by_branch.items(), key=lambda item: f(item[1]["chi2_total"])):
        branch_rows.append(
            {
                "combined_branch": branch,
                "chi2_total": row["chi2_total"],
                "aic_total": row["aic_total"],
                "bic_total": row["bic_total"],
                "delta_chi2_vs_baseline": f"{f(row['chi2_total']) - f(baseline['chi2_total']):.12g}",
                "delta_aic_vs_baseline": f"{f(row['aic_total']) - f(baseline['aic_total']):.12g}",
                "omega_m": row["omega_m"],
                "omega_void": row["omega_void"],
                "mu_web": row["mu_web"],
                "chi2_distance": row["chi2_distance"],
                "chi2_growth": row["chi2_growth"],
                "chi2_multitracer": row["chi2_multitracer"],
                "void_channel_active_at_best": str(abs(f(row["omega_void"])) > 0.0).lower(),
                "web_channel_active_at_best": str(abs(f(row["mu_web"])) > 0.0).lower(),
                "physical_validation_claimed": "false",
                "claim_boundary": "combined_endpoint_diagnostic_not_validation",
            }
        )
    write_csv(OUT_BRANCH, branch_rows)

    baseline_drop = {
        row["drop_control"]: row
        for row in block_drops
        if row["combined_branch"] == "baseline_only"
    }
    block_rows: list[dict[str, str]] = []
    for row in block_drops:
        base = baseline_drop[row["drop_control"]]
        block_rows.append(
            {
                "drop_control": row["drop_control"],
                "combined_branch": row["combined_branch"],
                "kept_blocks": row["kept_blocks"],
                "chi2_kept_blocks": row["chi2_kept_blocks"],
                "delta_chi2_vs_baseline_same_drop": f"{f(row['chi2_kept_blocks']) - f(base['chi2_kept_blocks']):.12g}",
                "omega_m": row["omega_m"],
                "omega_void": row["omega_void"],
                "mu_web": row["mu_web"],
                "physical_validation_claimed": "false",
                "claim_boundary": "combined_endpoint_diagnostic_not_validation",
            }
        )
    write_csv(OUT_BLOCK, block_rows)

    candidate = next(row for row in branch_rows if row["combined_branch"] == "source_native_void_web")
    shuffled = next(row for row in branch_rows if row["combined_branch"] == "deterministic_shuffled_void_web")
    web_only = next(row for row in branch_rows if row["combined_branch"] == "web_only")
    summary_rows = [
        {
            "diagnostic_id": "VOID_WEB_COMBINED_ENDPOINT_DIAGNOSTICS_V1",
            "parent_run_id": summary["run_id"],
            "status": "DIAGNOSTIC_COMPLETE_NOT_VALIDATION",
            "candidate_delta_chi2_vs_baseline": candidate["delta_chi2_vs_baseline"],
            "candidate_delta_aic_vs_baseline": candidate["delta_aic_vs_baseline"],
            "candidate_void_channel_active_at_best": candidate["void_channel_active_at_best"],
            "candidate_web_channel_active_at_best": candidate["web_channel_active_at_best"],
            "candidate_equals_web_only_chi2": str(candidate["chi2_total"] == web_only["chi2_total"]).lower(),
            "shuffled_minus_candidate_chi2": f"{f(shuffled['chi2_total']) - f(candidate['chi2_total']):.12g}",
            "shuffled_minus_candidate_aic": f"{f(shuffled['aic_total']) - f(candidate['aic_total']):.12g}",
            "dominant_failure_mode": "void_channel_inactive_and_shuffled_control_marginally_better",
            "recommended_next_action": "diagnose_void_source_basis_or_shared_amplitude_grammar_before_any_claim_promotion",
            "physical_validation_claimed": "false",
            "claim_boundary": "combined_endpoint_diagnostic_not_validation",
        }
    ]
    write_csv(OUT_SUMMARY, summary_rows)
    print(
        "PAPER10_VOID_WEB_COMBINED_ENDPOINT_DIAGNOSTICS_V1_BUILT "
        f"failure={summary_rows[0]['dominant_failure_mode']} "
        "claim_boundary=diagnostic_not_validation"
    )


if __name__ == "__main__":
    main()

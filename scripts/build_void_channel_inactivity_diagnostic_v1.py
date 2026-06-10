#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN_SUMMARY = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1_summary.csv"
PANTHEON_GRID = ROOT / "data" / "derived" / "pantheon_void_web_source_native_full_cov_pilot_v1_grid.csv"
COMBINED_GRID = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_grid.csv"
COMBINED_DIAG = ROOT / "data" / "derived" / "void_web_combined_endpoint_diagnostics_v1_summary.csv"
OUT_PROFILE = ROOT / "data" / "derived" / "void_channel_inactivity_diagnostic_v1_profile.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "void_channel_inactivity_diagnostic_v1_summary.csv"


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


def best_profile(
    rows: list[dict[str, str]],
    branch_field: str,
    branch_name: str,
    chi2_field: str,
) -> list[dict[str, str]]:
    by_void: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row[branch_field] == branch_name:
            by_void[row["omega_void"]].append(row)
    out: list[dict[str, str]] = []
    for omega_void, items in sorted(by_void.items(), key=lambda item: f(item[0])):
        best = min(items, key=lambda row: f(row[chi2_field]))
        out.append(
            {
                "profile_source": branch_name,
                "omega_void": omega_void,
                "best_chi2": best[chi2_field],
                "best_omega_m": best["omega_m"],
                "best_mu_web": best.get("omega_web", best.get("mu_web", "")),
                "physical_validation_claimed": "false",
                "claim_boundary": "void_channel_inactivity_diagnostic_not_validation",
            }
        )
    return out


def main() -> None:
    design = read_one(DESIGN_SUMMARY)
    combined_diag = read_one(COMBINED_DIAG)
    pantheon_rows = read_rows(PANTHEON_GRID)
    combined_rows = read_rows(COMBINED_GRID)

    profiles = best_profile(pantheon_rows, "branch", "source_native_void_only", "chi2")
    profiles += best_profile(combined_rows, "combined_branch", "void_only", "chi2_total")
    baselines = {row["profile_source"]: next(item for item in profiles if item["profile_source"] == row["profile_source"] and item["omega_void"] == "0") for row in profiles}
    profile_rows: list[dict[str, str]] = []
    for row in profiles:
        baseline = baselines[row["profile_source"]]
        row = dict(row)
        row["delta_chi2_vs_omega_void_zero"] = f"{f(row['best_chi2']) - f(baseline['best_chi2']):.12g}"
        profile_rows.append(row)
    write_csv(OUT_PROFILE, profile_rows)

    rows_total = int(design["rows"])
    void_nonzero = int(design["void_nonzero_rows"])
    web_nonzero = int(design["web_nonzero_rows"])
    nonzero_void_profiles = [row for row in profile_rows if row["omega_void"] != "0"]
    nonzero_void_best = min(nonzero_void_profiles, key=lambda row: f(row["delta_chi2_vs_omega_void_zero"]))
    summary = [
        {
            "diagnostic_id": "VOID_CHANNEL_INACTIVITY_DIAGNOSTIC_V1",
            "status": "DIAGNOSTIC_COMPLETE_NOT_VALIDATION",
            "parent_combined_diagnostic": combined_diag["diagnostic_id"],
            "void_nonzero_rows": str(void_nonzero),
            "web_nonzero_rows": str(web_nonzero),
            "total_rows": str(rows_total),
            "void_nonzero_fraction": f"{void_nonzero / rows_total:.12g}",
            "web_nonzero_fraction": f"{web_nonzero / rows_total:.12g}",
            "best_nonzero_void_profile_source": nonzero_void_best["profile_source"],
            "best_nonzero_void_omega_void": nonzero_void_best["omega_void"],
            "best_nonzero_void_delta_chi2_vs_zero": nonzero_void_best["delta_chi2_vs_omega_void_zero"],
            "combined_candidate_void_channel_active_at_best": combined_diag["candidate_void_channel_active_at_best"],
            "combined_candidate_equals_web_only_chi2": combined_diag["candidate_equals_web_only_chi2"],
            "diagnostic_verdict": "void_basis_has_limited_support_and_nonzero_void_amplitudes_do_not_improve_frozen_profiles",
            "recommended_next_action": "audit_void_mapping_rule_and_void_source_basis_before_reopening_endpoint_scoring",
            "physical_validation_claimed": "false",
            "claim_boundary": "void_channel_inactivity_diagnostic_not_validation",
        }
    ]
    write_csv(OUT_SUMMARY, summary)
    print(
        "PAPER10_VOID_CHANNEL_INACTIVITY_DIAGNOSTIC_V1_BUILT "
        f"void_fraction={summary[0]['void_nonzero_fraction']} "
        f"best_nonzero_delta={summary[0]['best_nonzero_void_delta_chi2_vs_zero']} "
        "claim_boundary=diagnostic_not_validation"
    )


if __name__ == "__main__":
    main()

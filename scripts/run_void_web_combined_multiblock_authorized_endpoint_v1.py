#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data" / "source_manifest" / "void_web_combined_multiblock_authorized_endpoint_run_v1.csv"
PROTOCOL = ROOT / "data" / "source_manifest" / "void_web_combined_multiblock_endpoint_protocol_v1.csv"
AUTH = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_response_v1_summary.csv"
CMB = ROOT / "data" / "derived" / "cmb_safety_lowz_support_v1_summary.csv"
PANTHEON_GRID = ROOT / "data" / "derived" / "pantheon_void_web_source_native_full_cov_pilot_v1_grid.csv"
GROWTH_GRID = ROOT / "data" / "derived" / "growth_web_source_native_pilot_v1_grid.csv"
BAO_GRID = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_grid.csv"
BLOCK_DROPS = ROOT / "data" / "derived" / "void_web_combined_multiblock_authorized_endpoint_v1_block_drop.csv"

BRANCH_MAP = {
    "baseline_only": {
        "distance": "baseline_only",
        "growth": "baseline_only",
        "bao": "baseline_only",
        "k_shared": 4,
    },
    "source_native_void_web": {
        "distance": "source_native_void_web_shell",
        "growth": "web_growth_shell",
        "bao": "web_growth_shell",
        "k_shared": 6,
    },
    "void_only": {
        "distance": "source_native_void_only",
        "growth": "baseline_only",
        "bao": "baseline_only",
        "k_shared": 5,
    },
    "web_only": {
        "distance": "source_native_web_only",
        "growth": "web_growth_shell",
        "bao": "web_growth_shell",
        "k_shared": 5,
    },
    "wrong_web_sign": {
        "distance": "wrong_web_sign",
        "growth": "wrong_web_sign",
        "bao": "wrong_web_sign",
        "k_shared": 6,
    },
    "deterministic_shuffled_void_web": {
        "distance": "deterministic_shuffled_source_native_void_web",
        "growth": "deterministic_shuffled_web",
        "bao": "deterministic_shuffled_web",
        "k_shared": 6,
    },
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def f(value: str) -> float:
    return float(value)


def best_by_branch_and_shared_keys(
    rows: list[dict[str, str]],
    branch: str,
    key_fields: tuple[str, ...],
) -> dict[tuple[str, ...], dict[str, str]]:
    out: dict[tuple[str, ...], dict[str, str]] = {}
    for row in rows:
        if row["branch"] != branch:
            continue
        key = tuple(row[field] for field in key_fields)
        if key not in out or f(row["chi2"]) < f(out[key]["chi2"]):
            out[key] = row
    return out


def best_by_omega_m(rows: list[dict[str, str]], branch: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        if row["branch"] != branch:
            continue
        key = row["omega_m"]
        if key not in out or f(row["chi2"]) < f(out[key]["chi2"]):
            out[key] = row
    return out


def n_eff() -> int:
    p = read_one(ROOT / "data" / "derived" / "pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv")
    g = read_one(ROOT / "data" / "derived" / "growth_web_source_native_pilot_v1_summary.csv")
    b = read_one(ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv")
    return int(p["n_rows"]) + int(g["n_rows"]) + int(b["n_rows"])


def main() -> None:
    run = read_one(RUN)
    protocol = read_one(PROTOCOL)
    auth = read_one(AUTH)
    cmb = read_one(CMB)
    require(run["status"] == "AUTHORIZED_COMBINED_VOID_WEB_ENDPOINT_RUN_PERMISSION_ONLY", "run status mismatch")
    require(run["endpoint_run_allowed"] == "true", "run manifest must allow endpoint run")
    require(run["physical_validation_claimed"] == "false", "run manifest must not claim validation")
    require(protocol["status"] == "COMBINED_MULTIBLOCK_ENDPOINT_PROTOCOL_FROZEN_NOT_RUN", "protocol status mismatch")
    require(protocol["physical_validation_claimed"] == "false", "protocol must not claim validation")
    require(auth["decision"] == "GO_COMBINED_VOID_WEB_ENDPOINT_PERMISSION_ONLY", "authorization decision mismatch")
    require(auth["endpoint_run_allowed"] == "true", "authorization must allow endpoint run")
    require(auth["forbidden_inputs_used"] == "false", "authorization must not use forbidden inputs")
    require(auth["physical_validation_claimed"] == "false", "authorization must not claim validation")
    require(cmb["passes_cmb_lowz_support_check"] == "true", "CMB safety support must pass before endpoint run")
    require(cmb["contains_cmb_likelihood"] == "false", "CMB support must not be treated as likelihood")

    pantheon_rows = read_rows(PANTHEON_GRID)
    growth_rows = read_rows(GROWTH_GRID)
    bao_rows = read_rows(BAO_GRID)
    n_rows = n_eff()

    grid_rows: list[dict[str, str]] = []
    for combined_branch, block in BRANCH_MAP.items():
        distance_branch = block["distance"]
        growth_branch = block["growth"]
        bao_branch = block["bao"]
        k_shared = int(block["k_shared"])

        distance_lookup = best_by_branch_and_shared_keys(
            pantheon_rows,
            distance_branch,
            ("omega_m", "omega_void", "omega_web"),
        )
        growth_lookup = best_by_branch_and_shared_keys(growth_rows, growth_branch, ("omega_m", "mu_web"))
        bao_lookup = best_by_branch_and_shared_keys(bao_rows, bao_branch, ("omega_m", "mu_web"))
        growth_baseline = best_by_omega_m(growth_rows, "baseline_only")
        bao_baseline = best_by_omega_m(bao_rows, "baseline_only")

        for (omega_m, omega_void, omega_web), distance in distance_lookup.items():
            growth = growth_lookup.get((omega_m, omega_web))
            bao = bao_lookup.get((omega_m, omega_web))
            if growth_branch == "baseline_only":
                growth = growth_baseline.get(omega_m)
            if bao_branch == "baseline_only":
                bao = bao_baseline.get(omega_m)
            if growth is None or bao is None:
                continue
            chi2_distance = f(distance["chi2"])
            chi2_growth = f(growth["chi2"])
            chi2_multitracer = f(bao["chi2"])
            chi2_total = chi2_distance + chi2_growth + chi2_multitracer
            aic_total = chi2_total + 2.0 * k_shared
            bic_total = chi2_total + math.log(n_rows) * k_shared
            grid_rows.append(
                {
                    "run_id": run["run_id"],
                    "combined_branch": combined_branch,
                    "omega_m": omega_m,
                    "omega_void": omega_void,
                    "mu_web": omega_web,
                    "chi2_distance": f"{chi2_distance:.12g}",
                    "chi2_growth": f"{chi2_growth:.12g}",
                    "chi2_multitracer": f"{chi2_multitracer:.12g}",
                    "chi2_total": f"{chi2_total:.12g}",
                    "aic_total": f"{aic_total:.12g}",
                    "bic_total": f"{bic_total:.12g}",
                    "k_shared": str(k_shared),
                    "n_eff": str(n_rows),
                    "distance_branch": distance_branch,
                    "growth_branch": growth_branch,
                    "multitracer_branch": bao_branch,
                    "cmb_safety_support_passed": cmb["passes_cmb_lowz_support_check"],
                    "physical_validation_claimed": "false",
                    "claim_boundary": run["claim_boundary"],
                }
            )

    require(grid_rows, "combined endpoint grid must not be empty")
    write_csv(GRID, grid_rows)
    best_by_combined = {
        branch: min(
            [row for row in grid_rows if row["combined_branch"] == branch],
            key=lambda row: f(row["chi2_total"]),
        )
        for branch in BRANCH_MAP
    }
    baseline = best_by_combined["baseline_only"]
    candidate = best_by_combined["source_native_void_web"]
    wrong_rows = [
        best_by_combined["void_only"],
        best_by_combined["web_only"],
        best_by_combined["wrong_web_sign"],
        best_by_combined["deterministic_shuffled_void_web"],
    ]
    best_wrong = min(wrong_rows, key=lambda row: f(row["chi2_total"]))
    candidate_chi2 = f(candidate["chi2_total"])
    baseline_chi2 = f(baseline["chi2_total"])
    candidate_aic = f(candidate["aic_total"])
    baseline_aic = f(baseline["aic_total"])
    summary = [
        {
            "run_id": run["run_id"],
            "status": "AUTHORIZED_COMBINED_VOID_WEB_ENDPOINT_COMPLETE_PERMISSION_ONLY",
            "authorization_decision": auth["decision"],
            "n_eff": str(n_rows),
            "baseline_best_chi2": baseline["chi2_total"],
            "baseline_best_aic": baseline["aic_total"],
            "baseline_best_bic": baseline["bic_total"],
            "candidate_best_chi2": candidate["chi2_total"],
            "candidate_best_aic": candidate["aic_total"],
            "candidate_best_bic": candidate["bic_total"],
            "candidate_best_omega_m": candidate["omega_m"],
            "candidate_best_omega_void": candidate["omega_void"],
            "candidate_best_mu_web": candidate["mu_web"],
            "candidate_delta_chi2_vs_baseline": f"{candidate_chi2 - baseline_chi2:.12g}",
            "candidate_delta_aic_vs_baseline": f"{candidate_aic - baseline_aic:.12g}",
            "candidate_delta_bic_vs_baseline": f"{f(candidate['bic_total']) - f(baseline['bic_total']):.12g}",
            "candidate_rank_by_chi2": str(
                1 + sum(f(row["chi2_total"]) < candidate_chi2 for row in best_by_combined.values())
            ),
            "candidate_rank_by_aic": str(
                1 + sum(f(row["aic_total"]) < candidate_aic for row in best_by_combined.values())
            ),
            "best_wrong_branch": best_wrong["combined_branch"],
            "best_wrong_chi2": best_wrong["chi2_total"],
            "best_wrong_aic": best_wrong["aic_total"],
            "candidate_beats_best_wrong_by_chi2": str(candidate_chi2 < f(best_wrong["chi2_total"])).lower(),
            "candidate_beats_best_wrong_by_aic": str(candidate_aic < f(best_wrong["aic_total"])).lower(),
            "cmb_safety_support_passed": cmb["passes_cmb_lowz_support_check"],
            "endpoint_run_allowed": "true",
            "physical_validation_claimed": "false",
            "claim_boundary": run["claim_boundary"],
            "verdict": "combined_void_web_endpoint_executed_permission_only_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)

    block_drop_rows: list[dict[str, str]] = []
    for drop_name, keep_fields in {
        "block_drop_distance": ("chi2_growth", "chi2_multitracer"),
        "block_drop_growth": ("chi2_distance", "chi2_multitracer"),
        "block_drop_multitracer": ("chi2_distance", "chi2_growth"),
    }.items():
        for branch, row in best_by_combined.items():
            chi2 = sum(f(row[field]) for field in keep_fields)
            block_drop_rows.append(
                {
                    "run_id": run["run_id"],
                    "drop_control": drop_name,
                    "combined_branch": branch,
                    "omega_m": row["omega_m"],
                    "omega_void": row["omega_void"],
                    "mu_web": row["mu_web"],
                    "chi2_kept_blocks": f"{chi2:.12g}",
                    "kept_blocks": ";".join(field.replace("chi2_", "") for field in keep_fields),
                    "physical_validation_claimed": "false",
                    "claim_boundary": run["claim_boundary"],
                }
            )
    write_csv(BLOCK_DROPS, block_drop_rows)

    print(
        "PAPER10_VOID_WEB_COMBINED_MULTIBLOCK_AUTHORIZED_ENDPOINT_V1_COMPLETE "
        f"delta_aic={summary[0]['candidate_delta_aic_vs_baseline']} "
        f"candidate_rank_aic={summary[0]['candidate_rank_by_aic']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_summary.csv"
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "low_z_void_replay_diagnostics_v1_summary.csv"
OUT_BRANCHES = ROOT / "data" / "derived" / "low_z_void_replay_diagnostics_v1_branch_summary.csv"
OUT_PROFILE = ROOT / "data" / "derived" / "low_z_void_replay_diagnostics_v1_profile.csv"


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
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12g}"


def best_by_branch(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    branches: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row["chi2_lowz_distance"] == "inf":
            continue
        branches.setdefault(row["branch"], []).append(row)
    return {branch: min(items, key=lambda row: float(row["chi2_lowz_distance"])) for branch, items in branches.items()}


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 2 or np.std(a) == 0.0 or np.std(b) == 0.0:
        return math.nan
    return float(np.corrcoef(a, b)[0, 1])


def load_low_z_profile() -> tuple[np.ndarray, np.ndarray, np.ndarray, list[dict[str, str]]]:
    design = read_rows(DESIGN)
    mask = read_rows(MASK)
    if len(design) != len(mask):
        raise SystemExit("design/mask row-count mismatch")
    rows: list[dict[str, str]] = []
    for design_row, mask_row in zip(design, mask, strict=True):
        if design_row["CID"] != mask_row["CID"] or design_row["source_row_index"] != mask_row["source_row_index"]:
            raise SystemExit("design/mask row-order mismatch")
        if mask_row["included"] == "true":
            rows.append(
                {
                    "CID": design_row["CID"],
                    "source_row_index": design_row["source_row_index"],
                    "zHD": design_row["zHD"],
                    "W_void_source_native_basis": design_row["W_void_source_native_basis"],
                    "W_web_source_native_basis": design_row["W_web_source_native_basis"],
                }
            )
    z = np.array([float(row["zHD"]) for row in rows], dtype=float)
    source_index = np.array([float(row["source_row_index"]) for row in rows], dtype=float)
    w_void = np.array([float(row["W_void_source_native_basis"]) for row in rows], dtype=float)
    return z, source_index, w_void, rows


def edge_flag(value: str, grid_values: list[float]) -> str:
    x = float(value)
    return str(abs(x - min(grid_values)) < 1e-12 or abs(x - max(grid_values)) < 1e-12).lower()


def main() -> None:
    replay = read_one(SUMMARY)
    grid_rows = read_rows(GRID)
    best = best_by_branch(grid_rows)
    z, source_index, w_void, profile_rows = load_low_z_profile()

    omega_m_grid = sorted({float(row["omega_m"]) for row in grid_rows})
    omega_void_grid = sorted({float(row["omega_void"]) for row in grid_rows if row["branch"] != "baseline_only"})

    branch_rows: list[dict[str, str]] = []
    baseline = best["baseline_only"]
    candidate = best["void_only"]
    for branch in [
        "baseline_only",
        "void_only",
        "wrong_void_sign",
        "wrong_void_threshold",
        "deterministic_shuffled_void_within_low_z_mask",
        "zero_void_amplitude",
    ]:
        row = best[branch]
        branch_rows.append(
            {
                "diagnostic_id": "LOW_Z_VOID_REPLAY_DIAGNOSTICS_V1",
                "branch": branch,
                "best_omega_m": row["omega_m"],
                "best_omega_void": row["omega_void"],
                "best_chi2_lowz_distance": row["chi2_lowz_distance"],
                "best_aic_lowz": row["aic_lowz"],
                "delta_chi2_vs_baseline": fmt(float(row["chi2_lowz_distance"]) - float(baseline["chi2_lowz_distance"])),
                "delta_chi2_vs_candidate": fmt(float(row["chi2_lowz_distance"]) - float(candidate["chi2_lowz_distance"])),
                "omega_m_at_grid_edge": edge_flag(row["omega_m"], omega_m_grid),
                "omega_void_at_grid_edge": edge_flag(row["omega_void"], omega_void_grid),
                "claim_boundary": "low_z_void_replay_diagnostic_not_validation",
            }
        )

    unique_void_rounded = len({round(float(x), 8) for x in w_void})
    shuffled_margin = float(best["deterministic_shuffled_void_within_low_z_mask"]["chi2_lowz_distance"]) - float(candidate["chi2_lowz_distance"])
    wrong_sign_margin = float(best["wrong_void_sign"]["chi2_lowz_distance"]) - float(candidate["chi2_lowz_distance"])
    threshold_margin = float(best["wrong_void_threshold"]["chi2_lowz_distance"]) - float(candidate["chi2_lowz_distance"])
    candidate_edge_pressure = (
        edge_flag(candidate["omega_m"], omega_m_grid) == "true"
        or edge_flag(candidate["omega_void"], omega_void_grid) == "true"
    )
    diagnosis = "weak_proxy_not_control_unique"
    if shuffled_margin < 0.0:
        diagnosis = "shuffled_control_beats_candidate"
    if candidate_edge_pressure and shuffled_margin < 0.0:
        diagnosis = "grid_edge_pressure_and_shuffled_control_beats_candidate"

    summary = [
        {
            "diagnostic_id": "LOW_Z_VOID_REPLAY_DIAGNOSTICS_V1",
            "parent_run_id": replay["run_id"],
            "n_rows": replay["n_rows"],
            "delta_chi2_void_minus_baseline": replay["delta_chi2_void_minus_baseline"],
            "delta_aic_void_minus_baseline": replay["delta_aic_void_minus_baseline"],
            "candidate_rank_by_chi2_among_void_and_controls": replay["candidate_rank_by_chi2_among_void_and_controls"],
            "controls_better_than_candidate_chi2": replay["controls_better_than_candidate_chi2"],
            "shuffled_minus_candidate_chi2": fmt(shuffled_margin),
            "wrong_sign_minus_candidate_chi2": fmt(wrong_sign_margin),
            "wrong_threshold_minus_candidate_chi2": fmt(threshold_margin),
            "candidate_omega_m_at_grid_edge": edge_flag(candidate["omega_m"], omega_m_grid),
            "candidate_omega_void_at_grid_edge": edge_flag(candidate["omega_void"], omega_void_grid),
            "void_basis_min": fmt(float(w_void.min())),
            "void_basis_max": fmt(float(w_void.max())),
            "void_basis_mean": fmt(float(w_void.mean())),
            "void_basis_std": fmt(float(w_void.std())),
            "void_basis_unique_rounded_1e8": str(unique_void_rounded),
            "void_basis_pearson_r_with_zHD": fmt(pearson(w_void, z)),
            "void_basis_pearson_r_with_source_row_index": fmt(pearson(w_void, source_index)),
            "diagnosis": diagnosis,
            "recommended_next_action": "do_not_tune_amplitude;rebuild_or_refine_void_source_basis_before_any_new_void_endpoint",
            "physical_validation_claimed": "false",
            "claim_boundary": "low_z_void_replay_diagnostic_not_validation",
        }
    ]

    profile_out = []
    for row in profile_rows:
        profile_out.append(
            {
                "diagnostic_id": "LOW_Z_VOID_REPLAY_DIAGNOSTICS_V1",
                **row,
                "claim_boundary": "low_z_void_replay_diagnostic_not_validation",
            }
        )

    write_csv(OUT_BRANCHES, branch_rows)
    write_csv(OUT_SUMMARY, summary)
    write_csv(OUT_PROFILE, profile_out)
    print(
        "PAPER10_LOW_Z_VOID_REPLAY_DIAGNOSTICS_V1_BUILT "
        f"diagnosis={diagnosis} shuffled_margin={summary[0]['shuffled_minus_candidate_chi2']} "
        "claim_boundary=diagnostic_not_validation"
    )


if __name__ == "__main__":
    main()

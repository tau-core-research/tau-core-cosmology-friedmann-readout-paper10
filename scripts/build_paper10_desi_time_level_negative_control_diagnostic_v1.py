#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
BAO_COV = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
GRID = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_grid.csv"
SUMMARY_IN = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_summary.csv"
ROW_OUT = ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_rows.csv"
BRANCH_OUT = ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_branches.csv"
SUMMARY_OUT = ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_summary.csv"
FIGURE_OUT = ROOT / "paper10_submission_source/figures/fig_desi_time_level_negative_control_diagnostic.pdf"
CLAIM_BOUNDARY = "paper10_desi_time_level_negative_control_diagnostic_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def covariance_from_rows(rows: list[dict[str, str]], allowed: list[int]) -> np.ndarray:
    index = {radial: i for i, radial in enumerate(allowed)}
    cov = np.zeros((len(allowed), len(allowed)), dtype=float)
    for row in rows:
        i = int(row["row_i"])
        j = int(row["row_j"])
        if i in index and j in index:
            cov[index[i], index[j]] = float(row["cov_minus_log_DH_over_rs"])
    return cov


def fit_constant(values: np.ndarray, cov: np.ndarray) -> tuple[float, float]:
    inv = np.linalg.inv(cov)
    ones = np.ones(len(values), dtype=float)
    beta = float((ones @ inv @ values) / (ones @ inv @ ones))
    chi2 = float((values - beta) @ inv @ (values - beta))
    return beta, chi2


def main() -> None:
    replay_summary = one_row(SUMMARY_IN)
    if replay_summary["verdict"] != "desi_time_level_permission_replay_not_control_resistant_not_validation":
        raise SystemExit("diagnostic expects the preserved negative DESI replay verdict")

    allowed = [0, 1, 2, 3, 4]
    cc_rows_all = read_rows(CC_MATCH)
    cc_rows = [row for row in cc_rows_all if int(row["radial_index"]) in allowed]
    if len(cc_rows) != 5:
        raise SystemExit("DESI negative-control diagnostic requires the five authorized rows")
    if any(row["cc_support_status"] != "MATCHED_WITHIN_CC_RANGE" for row in cc_rows):
        raise SystemExit("all diagnostic rows must remain CC-matched without extrapolation")

    z = np.array([float(row["z_eff"]) for row in cc_rows], dtype=float)
    y_bao = np.array([float(row["minus_log_DH_over_rs"]) for row in cc_rows], dtype=float)
    logh_cc = np.array([float(row["nearest_cc_logH"]) for row in cc_rows], dtype=float)
    sigma_logh_cc = np.array([float(row["nearest_cc_sigma_logH"]) for row in cc_rows], dtype=float)
    values = y_bao - logh_cc
    cov = covariance_from_rows(read_rows(BAO_COV), allowed) + np.diag(sigma_logh_cc**2)
    diag_sigma = np.sqrt(np.diag(cov))

    beta_candidate, chi2_candidate = fit_constant(values, cov)
    candidate_resid = values - beta_candidate
    candidate_pull = candidate_resid / diag_sigma

    rng = np.random.default_rng(41007)
    perm = rng.permutation(len(values))
    shuffle_values = values[perm]
    beta_shuffle, chi2_shuffle = fit_constant(shuffle_values, cov)
    shuffle_resid = shuffle_values - beta_shuffle
    shuffle_pull = shuffle_resid / diag_sigma

    row_records: list[dict[str, str]] = []
    for i, row in enumerate(cc_rows):
        row_records.append(
            {
                "diagnostic_id": "PAPER10_DESI_TIME_LEVEL_NEGATIVE_CONTROL_DIAGNOSTIC_V1",
                "radial_index": row["radial_index"],
                "z_eff": row["z_eff"],
                "nearest_cc_z": row["nearest_cc_z"],
                "delta_z_to_nearest_cc": row["delta_z_to_nearest_cc"],
                "nearest_cc_reference": row["nearest_cc_reference"],
                "bao_minus_log_DH_over_rs": f"{y_bao[i]:.12g}",
                "cc_logH": f"{logh_cc[i]:.12g}",
                "time_level_base_value_y_minus_logH": f"{values[i]:.12g}",
                "total_diag_sigma": f"{diag_sigma[i]:.12g}",
                "candidate_beta_rd": f"{beta_candidate:.12g}",
                "candidate_residual": f"{candidate_resid[i]:.12g}",
                "candidate_diag_pull": f"{candidate_pull[i]:.12g}",
                "shuffle_source_position": str(int(perm[i])),
                "shuffle_source_radial_index": cc_rows[int(perm[i])]["radial_index"],
                "shuffle_base_value": f"{shuffle_values[i]:.12g}",
                "shuffle_beta_rd": f"{beta_shuffle:.12g}",
                "shuffle_residual": f"{shuffle_resid[i]:.12g}",
                "shuffle_diag_pull": f"{shuffle_pull[i]:.12g}",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ROW_OUT, row_records)

    grid = read_rows(GRID)
    branch_records: list[dict[str, str]] = []
    for rank, row in enumerate(sorted(grid, key=lambda x: float(x["chi2"])), start=1):
        if row["branch"] == "candidate_beta_free":
            role = "candidate"
        elif float(row["chi2"]) < chi2_candidate:
            role = "control_beats_candidate"
        else:
            role = "control_does_not_beat_candidate"
        branch_records.append(
            {
                "diagnostic_id": "PAPER10_DESI_TIME_LEVEL_NEGATIVE_CONTROL_DIAGNOSTIC_V1",
                "rank_by_chi2": str(rank),
                "branch": row["branch"],
                "branch_role": role,
                "transform": row["transform"],
                "covariance_rule": row["covariance_rule"],
                "n_rows": row["n_rows"],
                "chi2": row["chi2"],
                "aic": row["aic"],
                "delta_chi2_minus_candidate": f"{float(row['chi2']) - chi2_candidate:.12g}",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(BRANCH_OUT, branch_records)

    worst = int(np.argmax(np.abs(candidate_pull)))
    controls_better = sum(1 for row in grid if row["branch"] != "candidate_beta_free" and float(row["chi2"]) < chi2_candidate)
    summary = [
        {
            "diagnostic_id": "PAPER10_DESI_TIME_LEVEL_NEGATIVE_CONTROL_DIAGNOSTIC_V1",
            "status": "DESI_TIME_LEVEL_NEGATIVE_CONTROL_DIAGNOSTIC_BUILT_NOT_VALIDATION",
            "candidate_chi2": f"{chi2_candidate:.12g}",
            "candidate_chi2_per_dof": f"{chi2_candidate / 4.0:.12g}",
            "redshift_shuffle_chi2": f"{chi2_shuffle:.12g}",
            "redshift_shuffle_chi2_per_dof": f"{chi2_shuffle / 4.0:.12g}",
            "delta_chi2_candidate_minus_shuffle": f"{chi2_candidate - chi2_shuffle:.12g}",
            "controls_better_than_candidate_chi2": str(controls_better),
            "largest_candidate_diag_pull_radial_index": cc_rows[worst]["radial_index"],
            "largest_candidate_diag_pull_z_eff": cc_rows[worst]["z_eff"],
            "largest_candidate_diag_pull": f"{candidate_pull[worst]:.12g}",
            "failure_mode": "five_row_time_level_constant_beta_endpoint_is_ordering_fragile",
            "recommended_next_action": "retain_negative_control_and_require_richer_independent_clock_or_time_readout_support_before_endpoint_claim",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "desi_time_level_negative_control_diagnostic_explains_non_control_resistance_not_validation",
        }
    ]
    write_csv(SUMMARY_OUT, summary)

    FIGURE_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10.5, 4.2), constrained_layout=True)
    ax0.errorbar(z, values, yerr=diag_sigma, fmt="o", color="#1f77b4", label="DESI/CC base values")
    ax0.plot(z, np.full_like(z, beta_candidate), color="#1f77b4", lw=1.8, label="candidate beta")
    ax0.scatter(z, shuffle_values, marker="s", color="#d95f02", label="redshift-order shuffle")
    ax0.plot(z, np.full_like(z, beta_shuffle), color="#d95f02", lw=1.4, ls="--", label="shuffle beta")
    ax0.set_xlabel("effective redshift")
    ax0.set_ylabel(r"$-\log(D_H/r_d)-\log H_{\rm CC}$")
    ax0.set_title("Five-row time-level consistency")
    ax0.legend(fontsize=7, frameon=False)
    ax0.grid(True, alpha=0.25)

    sorted_branches = sorted(grid, key=lambda x: float(x["chi2"]))
    labels = [row["branch"].replace("_control", "").replace("_", "\n") for row in sorted_branches]
    chi2 = [float(row["chi2"]) for row in sorted_branches]
    colors = ["#1f77b4" if row["branch"] == "candidate_beta_free" else "#888888" for row in sorted_branches]
    ax1.bar(np.arange(len(labels)), chi2, color=colors)
    ax1.axhline(chi2_candidate, color="#1f77b4", lw=1.2, ls="--", label="candidate chi2")
    ax1.set_xticks(np.arange(len(labels)))
    ax1.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
    ax1.set_ylabel(r"$\chi^2$")
    ax1.set_title("Frozen branches ranked by chi-square")
    ax1.set_yscale("log")
    ax1.grid(True, axis="y", alpha=0.25)
    ax1.legend(fontsize=7, frameon=False)
    fig.savefig(FIGURE_OUT)


if __name__ == "__main__":
    main()

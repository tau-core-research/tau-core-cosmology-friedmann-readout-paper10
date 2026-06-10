#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import math
import tarfile
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy import linalg


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_holdout_replay_policy_v1.csv"
HOLDOUT_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1_summary.csv"
HOLDOUT_PAIRS = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_pairs_v1.csv"
AUTHORIZED = ROOT / "data" / "derived" / "kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv"
DISAMBIGUATION = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_disambiguation_v1.csv"
DISAMBIGUATION_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_disambiguation_v1_summary.csv"
ROBUSTNESS_TOP = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)

GRID = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv"


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


def fmt(value: float) -> str:
    return f"{value:.12e}"


def stable_dot(a: np.ndarray, b: np.ndarray) -> float:
    return math.fsum(float(x) * float(y) for x, y in zip(a, b, strict=True))


def load_kids_vector_and_covariance() -> tuple[np.ndarray, np.ndarray]:
    if not TARBALL.exists():
        raise SystemExit(f"missing KiDS tarball: {TARBALL}")
    with tarfile.open(TARBALL) as tf:
        member = tf.extractfile(COSEBIS_MEMBER)
        if member is None:
            raise SystemExit("selected COSEBIs FITS member missing from KiDS tarball")
        payload = member.read()
    with fits.open(io.BytesIO(payload)) as hdul:
        data = hdul["En"].data
        cov = np.asarray(hdul["COVMAT"].data, dtype=float)
        y = np.asarray(data["VALUE"], dtype=float)
        row_order = [
            (int(data["BIN1"][i]), int(data["BIN2"][i]), int(data["ANGBIN"][i]))
            for i in range(len(y))
        ]
    expected_order = [
        (bin1, bin2, mode)
        for bin1 in range(1, 6)
        for bin2 in range(bin1, 6)
        for mode in range(1, 21)
    ]
    if len(y) != 300 or cov.shape != (300, 300):
        raise SystemExit("unexpected KiDS COSEBIs data/covariance shape")
    if row_order != expected_order:
        raise SystemExit("KiDS En row order does not match frozen COSEBIs row order")
    return y, cov


def chi2(y: np.ndarray, model: np.ndarray, cov: np.ndarray) -> float:
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)
    residual = y - model
    cinv_residual = linalg.cho_solve(factor, residual, check_finite=False)
    return stable_dot(residual, cinv_residual)


def best_nonnegative_amplitude(y: np.ndarray, x: np.ndarray, cov: np.ndarray) -> float:
    if np.allclose(x, 0.0):
        return 0.0
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)
    cinv_x = linalg.cho_solve(factor, x, check_finite=False)
    cinv_y = linalg.cho_solve(factor, y, check_finite=False)
    denom = stable_dot(x, cinv_x)
    if denom <= 0.0 or not math.isfinite(denom):
        raise SystemExit("invalid calibration amplitude denominator")
    return max(0.0, stable_dot(x, cinv_y) / denom)


def mapping_from_signature(signature: str) -> dict[str, str]:
    return dict(item.split("->", 1) for item in signature.split(";"))


def build_mapped_vector(theory_rows: list[dict[str, str]], mapping: dict[str, str]) -> np.ndarray:
    by_pair_mode = {
        (row["pair_id"], int(row["mode"])): float(row["theory_value"]) for row in theory_rows
    }
    return np.asarray(
        [by_pair_mode[(mapping[row["pair_id"]], int(row["mode"]))] for row in theory_rows],
        dtype=float,
    )


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    holdout_summary = read_one(HOLDOUT_SUMMARY)
    authorized = read_one(AUTHORIZED)
    disamb_summary = read_one(DISAMBIGUATION_SUMMARY)
    disamb_rows = read_rows(DISAMBIGUATION)
    top_rows = read_rows(ROBUSTNESS_TOP)
    theory_rows = sorted(read_rows(THEORY), key=lambda row: int(row["row_index_zero_based"]))
    holdout_pairs = read_rows(HOLDOUT_PAIRS)

    require(policy["status"] == "TOMOGRAPHIC_HOLDOUT_REPLAY_POLICY_FROZEN", "unexpected policy status")
    require(policy["explicit_user_approval_recorded"] == "true", "holdout replay requires explicit user approval")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(holdout_summary["h2_holdout_partition_frozen"] == "true", "holdout partition must be frozen")
    require(authorized["verdict"] == "authorized_endpoint_replay_low_tail_signal_not_validation", "authorized replay must precede holdout replay")
    require(
        disamb_summary["verdict"] == "tomographic_controls_block_validation_but_do_not_refute_endpoint_signal",
        "control disambiguation must precede holdout replay",
    )
    require(any(row["physical_alternative_status"] == "CONDITIONAL_SOURCE_SYSTEMATIC" for row in disamb_rows), "expected conditional source-systematic control")
    require(all(row["uses_kids_data_vector_values"] == "false" for row in theory_rows), "theory vector must be source frozen")

    y, cov = load_kids_vector_and_covariance()
    pair_by_row = [row["pair_id"] for row in theory_rows]
    candidate = np.asarray([float(row["theory_value"]) for row in theory_rows], dtype=float)
    top_by_operator = {row["operator"]: row for row in top_rows}
    branches: list[tuple[str, str, np.ndarray]] = [("candidate", "source_frozen_web_path_candidate", candidate)]
    for row in disamb_rows:
        top = top_by_operator[row["operator"]]
        branches.append((row["physical_alternative_status"], row["operator"], build_mapped_vector(theory_rows, mapping_from_signature(top["mapping_signature"]))))

    grid_rows: list[dict[str, str]] = []
    fold_ids = sorted({row["holdout_fold_id"] for row in holdout_pairs})
    for branch_type, branch, vector in branches:
        for fold_id in fold_ids:
            held_pairs = {
                row["tomographic_pair"]
                for row in holdout_pairs
                if row["holdout_fold_id"] == fold_id and row["pair_role"] == "holdout_pair"
            }
            hold_idx = np.asarray([idx for idx, pair in enumerate(pair_by_row) if pair in held_pairs], dtype=int)
            cal_idx = np.asarray([idx for idx, pair in enumerate(pair_by_row) if pair not in held_pairs], dtype=int)
            calibration_cov = cov[np.ix_(cal_idx, cal_idx)]
            holdout_cov = cov[np.ix_(hold_idx, hold_idx)]
            amplitude = best_nonnegative_amplitude(y[cal_idx], vector[cal_idx], calibration_cov)
            calibration_baseline_chi2 = chi2(y[cal_idx], np.zeros_like(y[cal_idx]), calibration_cov)
            calibration_chi2 = chi2(y[cal_idx], amplitude * vector[cal_idx], calibration_cov)
            holdout_baseline_chi2 = chi2(y[hold_idx], np.zeros_like(y[hold_idx]), holdout_cov)
            holdout_chi2 = chi2(y[hold_idx], amplitude * vector[hold_idx], holdout_cov)
            grid_rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "holdout_fold_id": fold_id,
                    "branch": branch,
                    "branch_type": branch_type,
                    "calibration_row_count": str(len(cal_idx)),
                    "holdout_row_count": str(len(hold_idx)),
                    "calibration_amplitude": fmt(amplitude),
                    "calibration_delta_chi2_vs_zero": fmt(calibration_chi2 - calibration_baseline_chi2),
                    "holdout_delta_chi2_vs_zero": fmt(holdout_chi2 - holdout_baseline_chi2),
                    "holdout_improves_zero": str(holdout_chi2 < holdout_baseline_chi2).lower(),
                    "uses_kids_data_vector_values_for_scoring": "true",
                    "uses_kids_data_vector_values_for_source_selection": "false",
                    "endpoint_validation_claimed": "false",
                    "claim_boundary": policy["claim_boundary"],
                }
            )

    branch_totals: dict[str, float] = {}
    branch_improved: dict[str, int] = {}
    for branch_type, branch, _ in branches:
        rows = [row for row in grid_rows if row["branch"] == branch]
        branch_totals[branch] = sum(float(row["holdout_delta_chi2_vs_zero"]) for row in rows)
        branch_improved[branch] = sum(row["holdout_improves_zero"] == "true" for row in rows)
    candidate_total = branch_totals["source_frozen_web_path_candidate"]
    better_controls = [
        branch
        for branch_type, branch, _ in branches
        if branch != "source_frozen_web_path_candidate" and branch_totals[branch] < candidate_total
    ]
    best_branch = min(branch_totals, key=lambda name: branch_totals[name])
    summary_rows = [
        {
            "policy_id": policy["policy_id"],
            "status": "TOMOGRAPHIC_HOLDOUT_REPLAY_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "fold_count": str(len(fold_ids)),
            "comparison_branch_count": str(len(branches)),
            "candidate_total_holdout_delta_chi2_vs_zero": fmt(candidate_total),
            "candidate_holdout_improved_fold_count": str(branch_improved["source_frozen_web_path_candidate"]),
            "candidate_rank_by_total_holdout_delta_chi2": str(1 + len(better_controls)),
            "best_branch": best_branch,
            "best_branch_total_holdout_delta_chi2_vs_zero": fmt(branch_totals[best_branch]),
            "candidate_beating_control_count": str(len(better_controls)),
            "candidate_beating_controls": ";".join(better_controls) if better_controls else "none",
            "holdout_replay_refutes_endpoint_signal": "false",
            "tomographic_controls_block_validation": "true" if better_controls else "false",
            "computes_new_labels": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "holdout_replay_preserves_signal_but_tomographic_control_caveat_remains"
            if better_controls
            else "holdout_replay_preserves_signal_without_candidate_beating_control_in_comparison_set",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(GRID, grid_rows)
    write_csv(SUMMARY, summary_rows)
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_HOLDOUT_REPLAY_V1_COMPLETE "
        f"candidate_folds={summary_rows[0]['candidate_holdout_improved_fold_count']}/{summary_rows[0]['fold_count']} "
        f"candidate_rank={summary_rows[0]['candidate_rank_by_total_holdout_delta_chi2']}/{summary_rows[0]['comparison_branch_count']} "
        f"verdict={summary_rows[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run the caveated ACT K_path guarded replay.

This is a permission-only diagnostic execution.  It reuses the frozen ACT
candidate and mandatory controls, but writes separate caveated outputs so the
older control-dominated replay remains preserved.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import linalg

try:
    from run_act_dr6_lensing_path_weight_authorized_replay_v1 import (
        CONTROL_BRANCHES,
        CLAIM_BOUNDARY as OLD_CLAIM_BOUNDARY,
        covariance_for_positions,
        distance_modulus,
        load_design_and_candidate,
        vector_for_branch,
    )
    from run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from run_pantheon_pilot_scoring_v1 import parse_range
except ImportError:
    from scripts.run_act_dr6_lensing_path_weight_authorized_replay_v1 import (
        CONTROL_BRANCHES,
        covariance_for_positions,
        distance_modulus,
        load_design_and_candidate,
        vector_for_branch,
    )
    from scripts.run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from scripts.run_pantheon_pilot_scoring_v1 import parse_range


ROOT = Path(__file__).resolve().parents[1]
RUN_TEMPLATE = ROOT / "data" / "source_manifest" / "act_dr6_lensing_path_weight_replay_run_template_v1.csv"
AUTH_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_caveated_kpath_guarded_replay_package_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "act_dr6_lensing_caveated_kpath_guarded_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_caveated_kpath_guarded_replay_v1_summary.csv"
CLAIM_BOUNDARY = "act_dr6_lensing_caveated_kpath_guarded_replay_permission_only_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    run = read_one(RUN_TEMPLATE)
    auth = read_one(AUTH_SUMMARY)
    package = read_one(PACKAGE_SUMMARY)
    if run["status"] != "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION":
        raise SystemExit("bad ACT replay template status")
    if auth["permission_only_guarded_replay_package_preparation_allowed"] != "true":
        raise SystemExit("guarded replay package preparation is not authorized")
    if auth["endpoint_replay_allowed_by_this_review"] != "false":
        raise SystemExit("authorization response must not directly authorize endpoint replay")
    if package["verdict"] != "ACT_CAVEATED_KPATH_GUARDED_REPLAY_PACKAGE_READY_NOT_EXECUTED":
        raise SystemExit("guarded replay package is not ready")

    z, mu, w, curl, diff, positions = load_design_and_candidate()
    cov = covariance_for_positions(positions)
    factor, _, _ = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    omega_m_grid = parse_range(run["omega_m_grid"])
    omega_path_grid = parse_range(run["omega_path_grid"])

    rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, omega_path: float, vec: np.ndarray) -> None:
        omega_eff = 0.0 if branch in {"baseline_only", "off"} else omega_path
        model = distance_modulus(z, omega_m, omega_eff, vec, branch)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        k_eff = 2 if branch in {"baseline_only", "off"} else 3
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        rows.append(
            {
                "run_id": "ACT_DR6_LENSING_CAVEATED_KPATH_GUARDED_REPLAY_V1",
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_path": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_act_path": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_act_path": f"{aic:.12g}" if math.isfinite(aic) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "permission_only_guarded_replay": "true",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "dark_sector_inference_allowed": "false",
                "family_verdict_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for omega_m in omega_m_grid:
        add_row("baseline_only", omega_m, 0.0, np.zeros_like(w))
        add_row("off", omega_m, 0.0, np.zeros_like(w))
        for omega_path in omega_path_grid:
            for branch in ["candidate", *sorted(CONTROL_BRANCHES)]:
                add_row(branch, omega_m, omega_path, vector_for_branch(w, curl, diff, branch))

    write_csv(GRID, rows)
    finite = [row for row in rows if row["chi2_act_path"] != "inf"]
    best_by_branch = {
        branch: min([row for row in finite if row["branch"] == branch], key=lambda row: float(row["chi2_act_path"]))
        for branch in sorted({row["branch"] for row in finite})
    }
    baseline = best_by_branch["baseline_only"]
    candidate = best_by_branch["candidate"]
    controls = [best_by_branch[branch] for branch in CONTROL_BRANCHES]
    best_control = min(controls, key=lambda row: float(row["chi2_act_path"]))
    better_controls = [row for row in controls if float(row["chi2_act_path"]) < float(candidate["chi2_act_path"])]
    verdict = (
        "ACT_CAVEATED_KPATH_GUARDED_REPLAY_CONTROL_SURVIVING_PERMISSION_ONLY_NOT_VALIDATION"
        if not better_controls
        else "ACT_CAVEATED_KPATH_GUARDED_REPLAY_CONTROL_DOMINATED_PERMISSION_ONLY_NOT_VALIDATION"
    )
    write_csv(
        SUMMARY,
        [
            {
                "run_id": "ACT_DR6_LENSING_CAVEATED_KPATH_GUARDED_REPLAY_V1",
                "status": "GUARDED_REPLAY_EXECUTED_PERMISSION_ONLY_NOT_VALIDATION",
                "authorization_verdict": auth["verdict"],
                "n_rows": str(len(z)),
                "grid_rows": str(len(rows)),
                "candidate_best_chi2_act_path": candidate["chi2_act_path"],
                "candidate_best_aic_act_path": candidate["aic_act_path"],
                "candidate_best_omega_m": candidate["omega_m"],
                "candidate_best_omega_path": candidate["omega_path"],
                "baseline_best_chi2_act_path": baseline["chi2_act_path"],
                "baseline_best_aic_act_path": baseline["aic_act_path"],
                "best_control_branch": best_control["branch"],
                "best_control_chi2_act_path": best_control["chi2_act_path"],
                "best_control_aic_act_path": best_control["aic_act_path"],
                "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_act_path']) - float(baseline['chi2_act_path']):.12g}",
                "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_act_path']) - float(best_control['chi2_act_path']):.12g}",
                "controls_better_than_candidate": str(len(better_controls)),
                "family_survives_controls": "true" if not better_controls else "false",
                "permission_only_guarded_replay": "true",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "dark_sector_inference_allowed": "false",
                "family_verdict_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
            }
        ],
    )
    print(f"ACT_CAVEATED_KPATH_GUARDED_REPLAY_RUN verdict={verdict}")


if __name__ == "__main__":
    main()

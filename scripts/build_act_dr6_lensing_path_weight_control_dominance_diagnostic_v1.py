#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_candidate_v1.csv"
REPLAY_SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv"
REPLAY_GRID = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_authorized_replay_v1_grid.csv"
BRANCHES = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_branches.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def best_rows_by_branch(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    best: dict[str, dict[str, str]] = {}
    for row in rows:
        if row["chi2_act_path"] == "inf":
            continue
        branch = row["branch"]
        if branch not in best or float(row["chi2_act_path"]) < float(best[branch]["chi2_act_path"]):
            best[branch] = row
    return best


def vector(rows: list[dict[str, str]], key: str, mask_positive: np.ndarray | None = None) -> np.ndarray:
    values = np.array([float(row[key]) for row in rows], dtype=float)
    return values if mask_positive is None else values[mask_positive]


def corr(rows: list[dict[str, str]], left: str, right: str, mask_positive: np.ndarray | None = None) -> str:
    x = vector(rows, left, mask_positive)
    y = vector(rows, right, mask_positive)
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return "NA"
    return f"{float(np.corrcoef(x, y)[0, 1]):.12g}"


def main() -> None:
    candidate_rows = read_rows(CANDIDATE)
    replay_summary = read_rows(REPLAY_SUMMARY)[0]
    grid = read_rows(REPLAY_GRID)
    best = best_rows_by_branch(grid)
    candidate_chi2 = float(best["candidate"]["chi2_act_path"])
    branch_rows = []
    for branch, row in sorted(best.items(), key=lambda item: float(item[1]["chi2_act_path"])):
        branch_rows.append(
            {
                "artifact_id": "ACT_DR6_LENSING_PATH_WEIGHT_CONTROL_DOMINANCE_DIAGNOSTIC_V1",
                "branch": branch,
                "best_chi2_act_path": row["chi2_act_path"],
                "best_aic_act_path": row["aic_act_path"],
                "best_omega_m": row["omega_m"],
                "best_omega_path": row["omega_path"],
                "delta_chi2_vs_candidate": f"{float(row['chi2_act_path']) - candidate_chi2:.12g}",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": "act_dr6_lensing_path_weight_control_dominance_diagnostic_not_validation",
            }
        )
    write_csv(BRANCHES, branch_rows)

    mask = np.array([row["mask_positive"].lower() == "true" for row in candidate_rows], dtype=bool)
    better_controls = int(replay_summary["controls_better_than_candidate"])
    verdict = (
        "ACT_PATH_WEIGHT_WEAK_NON_SPECIFIC_SIGNAL_CONTROL_DOMINATED"
        if better_controls > 0 and replay_summary["family_survives_controls"] == "false"
        else "ACT_PATH_WEIGHT_CONTROL_RESISTANCE_NOT_DIAGNOSED"
    )
    summary_rows = [
        {
            "artifact_id": "ACT_DR6_LENSING_PATH_WEIGHT_CONTROL_DOMINANCE_DIAGNOSTIC_V1",
            "status": "CONTROL_DOMINANCE_DIAGNOSTIC_BUILT_NOT_VALIDATION",
            "source_rows": str(len(candidate_rows)),
            "mask_positive_rows": str(int(mask.sum())),
            "mask_zero_rows": str(int((~mask).sum())),
            "candidate_best_chi2_act_path": best["candidate"]["chi2_act_path"],
            "baseline_best_chi2_act_path": best["baseline_only"]["chi2_act_path"],
            "best_control_branch": replay_summary["best_control_branch"],
            "best_control_chi2_act_path": replay_summary["best_control_chi2_act_path"],
            "controls_better_than_candidate": replay_summary["controls_better_than_candidate"],
            "candidate_delta_chi2_vs_baseline": replay_summary["delta_chi2_candidate_minus_baseline"],
            "candidate_delta_chi2_vs_best_control": replay_summary["delta_chi2_candidate_minus_best_control"],
            "corr_baseline_candidate_vs_curl_all": corr(
                candidate_rows, "w_act_baseline_candidate", "w_act_curl_null"
            ),
            "corr_baseline_candidate_vs_curl_mask_positive": corr(
                candidate_rows, "w_act_baseline_candidate", "w_act_curl_null", mask
            ),
            "corr_baseline_candidate_vs_diff_all": corr(
                candidate_rows, "w_act_baseline_candidate", "w_act_diff_f150_f090_null"
            ),
            "corr_baseline_candidate_vs_diff_mask_positive": corr(
                candidate_rows, "w_act_baseline_candidate", "w_act_diff_f150_f090_null", mask
            ),
            "interpretation": (
                "candidate improves over baseline but loses to null/order controls; present ACT "
                "unitless path-weight vector is non-specific and should not be promoted"
            ),
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": "act_dr6_lensing_path_weight_control_dominance_diagnostic_not_validation",
            "verdict": verdict,
        }
    ]
    write_csv(SUMMARY, summary_rows)
    print(f"{summary_rows[0]['status']} verdict={verdict}")


if __name__ == "__main__":
    main()

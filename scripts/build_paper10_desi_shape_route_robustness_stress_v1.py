#!/usr/bin/env python3
from __future__ import annotations

import csv
import itertools
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_route_robustness_stress_policy_v1.csv"
REPLAY_GRID = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv"
REPLAY_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
BAO_COV = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_route_robustness_stress_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def covariance_from_rows(rows: list[dict[str, str]], allowed: list[int]) -> np.ndarray:
    index = {radial: i for i, radial in enumerate(allowed)}
    cov = np.zeros((len(allowed), len(allowed)), dtype=float)
    for row in rows:
        i = int(row["row_i"])
        j = int(row["row_j"])
        if i in index and j in index:
            cov[index[i], index[j]] = float(row["cov_minus_log_DH_over_rs"])
    return cov


def first_difference_covariance() -> np.ndarray:
    allowed = [0, 1, 2, 3, 4]
    rows = [row for row in read_rows(CC_MATCH) if int(row["radial_index"]) in allowed]
    rows = sorted(rows, key=lambda row: int(row["radial_index"]))
    z = np.array([float(row["z_eff"]) for row in rows], dtype=float)
    sigma_logh = np.array([float(row["nearest_cc_sigma_logH"]) for row in rows], dtype=float)
    cov = covariance_from_rows(read_rows(BAO_COV), allowed) + np.diag(sigma_logh**2)
    first = np.zeros((len(z) - 1, len(z)), dtype=float)
    for i in range(len(z) - 1):
        dz = z[i + 1] - z[i]
        first[i, i] = -1.0 / dz
        first[i, i + 1] = 1.0 / dz
    return first @ cov @ first.T


def parse_vector(raw: str) -> np.ndarray:
    return np.array([float(x) for x in raw.split(";") if x], dtype=float)


def quadratic_score(values: np.ndarray, cov: np.ndarray) -> float:
    return float(values @ np.linalg.pinv(cov) @ values)


def rms(values: np.ndarray) -> float:
    return math.sqrt(float(np.mean(values**2)))


def signs(values: np.ndarray) -> str:
    return "".join("+" if x > 0 else "-" if x < 0 else "0" for x in values)


def main() -> None:
    policy = read_one(POLICY)
    replay = read_one(REPLAY_SUMMARY)
    grid = read_rows(REPLAY_GRID)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad policy claim boundary")
    if replay["status"] != "DESI_SHAPE_ROUTE_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION":
        raise SystemExit("authorized replay must exist before robustness stress")
    if replay["endpoint_replay_allowed"] != "true" or replay["endpoint_validation_claimed"] != "false":
        raise SystemExit("robustness stress expects permission-only replay")

    by_branch = {row["branch"]: row for row in grid}
    candidate = by_branch["candidate_CLOCK_SLOPE_SHAPE"]
    candidate_values = parse_vector(candidate["shape_vector"])
    first_cov = first_difference_covariance()
    candidate_score = quadratic_score(candidate_values, first_cov)
    candidate_rms = rms(candidate_values)
    candidate_sign = signs(candidate_values)

    rows: list[dict[str, str]] = []

    def add(test_family: str, test_id: str, values: np.ndarray, cov: np.ndarray, note: str) -> None:
        score = quadratic_score(values, cov)
        rows.append(
            {
                "stress_id": "PAPER10_DESI_SHAPE_ROUTE_ROBUSTNESS_STRESS_V1",
                "test_family": test_family,
                "test_id": test_id,
                "n_shape_rows": str(len(values)),
                "shape_vector": ";".join(f"{x:.12g}" for x in values),
                "shape_sign_pattern": signs(values),
                "shape_rms": f"{rms(values):.12g}",
                "shape_quadratic_score": f"{score:.12g}",
                "score_fraction_of_full_candidate": f"{score / candidate_score:.12g}" if candidate_score else "nan",
                "note": note,
                "endpoint_replay_allowed": "true",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    add("full_candidate", "candidate_CLOCK_SLOPE_SHAPE", candidate_values, first_cov, "full frozen candidate")
    for drop in range(len(candidate_values)):
        keep = [i for i in range(len(candidate_values)) if i != drop]
        add(
            "leave_one",
            f"drop_shape_row_{drop}",
            candidate_values[keep],
            first_cov[np.ix_(keep, keep)],
            "jackknife leave-one robustness stress",
        )
    for drop_pair in itertools.combinations(range(len(candidate_values)), 2):
        keep = [i for i in range(len(candidate_values)) if i not in drop_pair]
        add(
            "leave_two",
            "drop_shape_rows_" + "_".join(str(i) for i in drop_pair),
            candidate_values[keep],
            first_cov[np.ix_(keep, keep)],
            "jackknife leave-two robustness stress",
        )

    controls = [row for row in grid if row["branch"] != "candidate_CLOCK_SLOPE_SHAPE"]
    controls_sorted_score = sorted(controls + [candidate], key=lambda row: float(row["shape_quadratic_score"]), reverse=True)
    controls_sorted_rms = sorted(controls + [candidate], key=lambda row: float(row["shape_rms"]), reverse=True)
    score_rank = [row["branch"] for row in controls_sorted_score].index("candidate_CLOCK_SLOPE_SHAPE") + 1
    rms_rank = [row["branch"] for row in controls_sorted_rms].index("candidate_CLOCK_SLOPE_SHAPE") + 1
    sign_matches = 0
    comparable = 0
    for row in controls:
        values = parse_vector(row["shape_vector"])
        if len(values) == len(candidate_values):
            comparable += 1
            if signs(values) == candidate_sign:
                sign_matches += 1

    leave_one = [row for row in rows if row["test_family"] == "leave_one"]
    leave_two = [row for row in rows if row["test_family"] == "leave_two"]
    max_leave_one = max(leave_one, key=lambda row: float(row["shape_quadratic_score"]))
    min_leave_one = min(leave_one, key=lambda row: float(row["shape_quadratic_score"]))
    max_leave_two = max(leave_two, key=lambda row: float(row["shape_quadratic_score"]))
    leave_one_max_fraction = float(max_leave_one["score_fraction_of_full_candidate"])
    leave_one_min_fraction = float(min_leave_one["score_fraction_of_full_candidate"])
    margin = float(replay["delta_candidate_minus_best_control_score"])
    margin_fraction = margin / candidate_score if candidate_score else float("nan")

    if margin_fraction < 0.01 or leave_one_max_fraction > 0.95:
        verdict = "positive_but_narrow_margin_and_row_sensitive_not_validation"
    elif score_rank == 1 and leave_one_min_fraction > 0.5:
        verdict = "positive_and_internally_robust_not_validation"
    else:
        verdict = "mixed_robustness_not_validation"

    write_csv(OUT, rows)
    write_csv(
        SUMMARY,
        [
            {
                "stress_id": "PAPER10_DESI_SHAPE_ROUTE_ROBUSTNESS_STRESS_V1",
                "status": "DESI_SHAPE_ROUTE_ROBUSTNESS_STRESS_BUILT_PERMISSION_REPLAY_NOT_VALIDATION",
                "candidate_score": f"{candidate_score:.12g}",
                "candidate_rms": f"{candidate_rms:.12g}",
                "candidate_score_rank_among_replay_branches": str(score_rank),
                "candidate_rms_rank_among_replay_branches": str(rms_rank),
                "candidate_sign_pattern": candidate_sign,
                "full_length_control_sign_pattern_matches": str(sign_matches),
                "full_length_control_sign_pattern_comparisons": str(comparable),
                "best_control_branch": replay["best_control_branch"],
                "candidate_minus_best_control_score": replay["delta_candidate_minus_best_control_score"],
                "candidate_minus_best_control_score_fraction": f"{margin_fraction:.12g}",
                "max_leave_one_test": max_leave_one["test_id"],
                "max_leave_one_score": max_leave_one["shape_quadratic_score"],
                "max_leave_one_fraction_of_full_candidate": max_leave_one["score_fraction_of_full_candidate"],
                "min_leave_one_test": min_leave_one["test_id"],
                "min_leave_one_score": min_leave_one["shape_quadratic_score"],
                "min_leave_one_fraction_of_full_candidate": min_leave_one["score_fraction_of_full_candidate"],
                "max_leave_two_test": max_leave_two["test_id"],
                "max_leave_two_score": max_leave_two["shape_quadratic_score"],
                "max_leave_two_fraction_of_full_candidate": max_leave_two["score_fraction_of_full_candidate"],
                "endpoint_replay_allowed": "true",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
            }
        ],
    )
    print(f"paper10_desi_shape_route_robustness_stress_v1: {verdict}")


if __name__ == "__main__":
    main()

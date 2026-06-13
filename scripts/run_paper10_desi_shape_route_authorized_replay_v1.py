#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_TEMPLATE = ROOT / "data/source_manifest/paper10_desi_shape_route_replay_run_template_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1_summary.csv"
SHAPE = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv"
CONTROLS = ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1.csv"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
BAO_COV = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
GRID = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_authorized_replay_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_route_authorized_replay_permission_only_not_validation"
CANDIDATE_BRANCH = "candidate_CLOCK_SLOPE_SHAPE"


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


def shape_covariances() -> tuple[np.ndarray, np.ndarray]:
    allowed = [0, 1, 2, 3, 4]
    cc_rows_all = read_rows(CC_MATCH)
    rows = [row for row in cc_rows_all if int(row["radial_index"]) in allowed]
    rows = sorted(rows, key=lambda row: int(row["radial_index"]))
    if len(rows) != 5:
        raise SystemExit("shape replay requires exactly five CC-matched DESI rows")
    if any(row["cc_extrapolation_used"] != "false" for row in rows):
        raise SystemExit("CC extrapolation is forbidden")
    z = np.array([float(row["z_eff"]) for row in rows], dtype=float)
    sigma_logh = np.array([float(row["nearest_cc_sigma_logH"]) for row in rows], dtype=float)
    cov = covariance_from_rows(read_rows(BAO_COV), allowed) + np.diag(sigma_logh**2)

    first = np.zeros((len(z) - 1, len(z)), dtype=float)
    for i in range(len(z) - 1):
        dz = z[i + 1] - z[i]
        first[i, i] = -1.0 / dz
        first[i, i + 1] = 1.0 / dz
    first_cov = first @ cov @ first.T

    second_rows = []
    for i in range(len(z) - 2):
        dz_left = z[i + 1] - z[i]
        dz_right = z[i + 2] - z[i + 1]
        span = z[i + 2] - z[i]
        row = np.zeros(len(z), dtype=float)
        row[i] = 2.0 / (span * dz_left)
        row[i + 1] = -2.0 * (1.0 / dz_left + 1.0 / dz_right) / span
        row[i + 2] = 2.0 / (span * dz_right)
        second_rows.append(row)
    second = np.array(second_rows)
    second_cov = second @ cov @ second.T
    return first_cov, second_cov


def quadratic_score(values: np.ndarray, cov: np.ndarray) -> float:
    return float(values @ np.linalg.pinv(cov) @ values)


def values_from_shape(family: str) -> np.ndarray:
    rows = [row for row in read_rows(SHAPE) if row["observable_family"] == family]
    rows = sorted(rows, key=lambda row: int(row["shape_row"]))
    return np.array([float(row["shape_value"]) for row in rows], dtype=float)


def parse_control_values(raw: str) -> list[float]:
    return [float(x) for x in raw.split(";") if x]


def main() -> None:
    run = read_one(RUN_TEMPLATE)
    auth = read_one(AUTH_SUMMARY)
    if run["status"] != "DESI_SHAPE_ROUTE_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION":
        raise SystemExit("bad DESI shape replay template status")
    if auth["decision"] != "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY":
        raise SystemExit("DESI shape-route replay is not authorized")
    if auth["endpoint_replay_allowed"] != "true":
        raise SystemExit("authorization must allow permission-only replay")
    if auth["endpoint_validation_claimed"] != "false" or auth["physical_validation_claimed"] != "false":
        raise SystemExit("authorization must not claim validation")
    if run["shape_rows_allowed"] != "0;1;2;3" or run["radial_rows_excluded"] != "5":
        raise SystemExit("shape replay scope changed")

    first_cov, second_cov = shape_covariances()
    candidate_values = values_from_shape("adjacent_first_difference_beta_shape")
    curvature_values = values_from_shape("second_difference_curvature_shape")
    if len(candidate_values) != 4 or len(curvature_values) != 3:
        raise SystemExit("unexpected shape row count")

    grid: list[dict[str, str]] = []

    def add_row(branch: str, family: str, values: np.ndarray, cov: np.ndarray, rule: str, n_rows: int) -> None:
        score = quadratic_score(values, cov)
        rms = math.sqrt(float(np.mean(values**2)))
        grid.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "control_family": family,
                "score_type": "source_native_quadratic_shape_score",
                "branch_rule": rule,
                "n_shape_rows": str(n_rows),
                "shape_vector": ";".join(f"{x:.12g}" for x in values),
                "shape_rms": f"{rms:.12g}",
                "shape_quadratic_score": f"{score:.12g}",
                "score_direction": "higher_source_native_shape_score_is_more_detectable",
                "endpoint_replay_allowed": "true",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    add_row(
        CANDIDATE_BRANCH,
        "candidate",
        candidate_values,
        first_cov,
        "frozen_CLOCK_SLOPE_SHAPE_adjacent_first_difference",
        4,
    )

    controls = {row["control_family"]: row for row in read_rows(CONTROLS)}
    shuffle = np.array(parse_control_values(controls["redshift_order_shuffle"]["control_vector_values"]), dtype=float)
    add_row(
        "control_redshift_order_shuffle",
        "redshift_order_shuffle",
        shuffle,
        first_cov,
        "deterministic_source_side_shuffle_seed_41007",
        4,
    )
    rank_part = controls["wrong_time_basis"]["control_vector_values"].split("|rank_reverse:", 1)[1]
    rank_reverse = np.array(parse_control_values(rank_part), dtype=float)
    add_row(
        "control_wrong_time_basis_rank_reverse",
        "wrong_time_basis",
        rank_reverse,
        first_cov,
        "rank_reverse_first_difference_shape_vector",
        4,
    )
    curvature_part = controls["wrong_time_basis"]["control_vector_values"].split("curvature:", 1)[1].split("|", 1)[0]
    curvature = np.array(parse_control_values(curvature_part), dtype=float)
    add_row(
        "control_wrong_time_basis_curvature",
        "wrong_time_basis",
        curvature,
        second_cov,
        "second_difference_curvature_shape_vector",
        3,
    )
    cc_stress_cov = np.array(first_cov, copy=True)
    cc_stress_cov += np.eye(cc_stress_cov.shape[0]) * np.median(np.diag(first_cov))
    add_row(
        "control_cc_window_stress",
        "cc_window_stress",
        candidate_values,
        cc_stress_cov,
        "caveated_row4_window_stress_covariance_inflation",
        4,
    )
    add_row(
        "control_rd_prior_stress",
        "rd_prior_stress",
        np.zeros_like(candidate_values),
        first_cov,
        "analytic_null_constant_beta_cancels_under_first_difference",
        4,
    )
    # Leave-row controls are reported as the strongest leave-one retained score;
    # this is a robustness control, not a row-selection procedure.
    leave_scores = []
    for i in range(len(candidate_values)):
        keep = [j for j in range(len(candidate_values)) if j != i]
        values = candidate_values[keep]
        cov = first_cov[np.ix_(keep, keep)]
        leave_scores.append((i, quadratic_score(values, cov), values, cov))
    drop_i, _, leave_values, leave_cov = max(leave_scores, key=lambda item: item[1])
    add_row(
        "control_leave_shape_row_max",
        "leave_row_or_pair",
        leave_values,
        leave_cov,
        f"maximum_leave_one_shape_score_drop_shape_row_{drop_i}",
        3,
    )

    write_csv(GRID, grid)
    by_branch = {row["branch"]: row for row in grid}
    candidate = by_branch[CANDIDATE_BRANCH]
    controls_only = [row for row in grid if row["branch"] != CANDIDATE_BRANCH]
    best_control = max(controls_only, key=lambda row: float(row["shape_quadratic_score"]))
    controls_ge_candidate = [
        row for row in controls_only if float(row["shape_quadratic_score"]) >= float(candidate["shape_quadratic_score"])
    ]
    verdict = (
        "desi_shape_route_permission_replay_candidate_exceeds_all_controls_not_validation"
        if not controls_ge_candidate
        else "desi_shape_route_permission_replay_candidate_not_control_resistant_not_validation"
    )
    write_csv(
        SUMMARY,
        [
            {
                "run_id": run["run_id"],
                "status": "DESI_SHAPE_ROUTE_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION",
                "authorization_decision": auth["decision"],
                "active_route_family": run["active_route_family"],
                "candidate_branch": CANDIDATE_BRANCH,
                "n_shape_rows": "4",
                "curvature_rows_available": "3",
                "excluded_radial_rows": run["radial_rows_excluded"],
                "branch_count": str(len(grid)),
                "candidate_shape_rms": candidate["shape_rms"],
                "candidate_shape_quadratic_score": candidate["shape_quadratic_score"],
                "best_control_branch": best_control["branch"],
                "best_control_shape_quadratic_score": best_control["shape_quadratic_score"],
                "delta_candidate_minus_best_control_score": f"{float(candidate['shape_quadratic_score']) - float(best_control['shape_quadratic_score']):.12g}",
                "controls_ge_candidate_score": str(len(controls_ge_candidate)),
                "family_survives_controls": "true" if not controls_ge_candidate else "false",
                "score_direction": "higher_source_native_shape_score_is_more_detectable",
                "endpoint_replay_allowed": "true",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
            }
        ],
    )
    print(
        "PAPER10_DESI_SHAPE_ROUTE_AUTHORIZED_REPLAY_RUN "
        f"verdict={verdict} candidate_score={candidate['shape_quadratic_score']}"
    )


if __name__ == "__main__":
    main()

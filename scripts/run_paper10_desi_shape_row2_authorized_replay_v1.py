#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data/source_manifest/paper10_desi_shape_row2_authorized_replay_run_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1_summary.csv"
SHAPE = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv"
CONTROLS = ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1.csv"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
BAO_COV = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
GRID = ROOT / "data/derived/paper10_desi_shape_row2_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_authorized_replay_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_authorized_replay_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_authorized_replay_permission_only_not_validation"
SHAPE_ROW = 2


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


def parse_control_values(raw: str) -> list[float]:
    return [float(x) for x in raw.split(";") if x]


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
    cc_rows = [row for row in read_rows(CC_MATCH) if int(row["radial_index"]) in allowed]
    cc_rows = sorted(cc_rows, key=lambda row: int(row["radial_index"]))
    if len(cc_rows) != 5:
        raise SystemExit("Row2 replay requires five CC-matched DESI rows for covariance propagation")
    if any(row["cc_extrapolation_used"] != "false" for row in cc_rows):
        raise SystemExit("CC extrapolation is forbidden")
    z = np.array([float(row["z_eff"]) for row in cc_rows], dtype=float)
    sigma_logh = np.array([float(row["nearest_cc_sigma_logH"]) for row in cc_rows], dtype=float)
    cov = covariance_from_rows(read_rows(BAO_COV), allowed) + np.diag(sigma_logh**2)
    first = np.zeros((len(z) - 1, len(z)), dtype=float)
    for i in range(len(z) - 1):
        dz = z[i + 1] - z[i]
        first[i, i] = -1.0 / dz
        first[i, i + 1] = 1.0 / dz
    return first @ cov @ first.T


def shape_row_value() -> dict[str, str]:
    rows = [
        row
        for row in read_rows(SHAPE)
        if row["observable_family"] == "adjacent_first_difference_beta_shape"
        and int(row["shape_row"]) == SHAPE_ROW
    ]
    if len(rows) != 1:
        raise SystemExit("expected exactly one frozen Row2 shape observable")
    return rows[0]


def score(value: float, variance: float) -> float:
    return float(value * value / variance)


def main() -> None:
    run = read_one(RUN_MANIFEST)
    auth = read_one(AUTH_SUMMARY)
    if run["status"] != "ROW2_PERMISSION_ONLY_REPLAY_AUTHORIZED_NOT_VALIDATION":
        raise SystemExit("bad Row2 run manifest status")
    if auth["verdict"] != "GO_DESI_SHAPE_ROW2_REPLAY_PERMISSION_ONLY":
        raise SystemExit("Row2 permission-only replay is not authorized")
    if auth["endpoint_replay_allowed"] != "true":
        raise SystemExit("Row2 authorization must allow replay")
    if auth["endpoint_validation_claimed"] != "false" or auth["physical_validation_claimed"] != "false":
        raise SystemExit("Row2 authorization must not claim validation")
    if run["endpoint_validation_claimed"] != "false" or run["physical_validation_claimed"] != "false":
        raise SystemExit("Row2 run manifest must not claim validation")

    shape = shape_row_value()
    first_cov = first_difference_covariance()
    row_variance = float(first_cov[SHAPE_ROW, SHAPE_ROW])
    row_sigma = math.sqrt(row_variance)
    candidate_value = float(shape["shape_value"])

    controls = {row["control_family"]: row for row in read_rows(CONTROLS)}
    shuffle_values = parse_control_values(controls["redshift_order_shuffle"]["control_vector_values"])
    rank_part = controls["wrong_time_basis"]["control_vector_values"].split("|rank_reverse:", 1)[1]
    rank_values = parse_control_values(rank_part)
    cc_stress_variance = row_variance + float(np.median(np.diag(first_cov)))

    rows = []

    def add(branch: str, family: str, value: float, variance: float, rule: str) -> None:
        rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "control_family": family,
                "shape_row": str(SHAPE_ROW),
                "z_left": shape["z_left"],
                "z_right": shape["z_right"],
                "shape_value": f"{value:.12g}",
                "shape_sigma": f"{math.sqrt(variance):.12g}",
                "shape_quadratic_score": f"{score(value, variance):.12g}",
                "branch_rule": rule,
                "score_direction": "higher_source_native_shape_score_is_more_detectable",
                "endpoint_replay_allowed": "true",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    add("candidate_CLOCK_SLOPE_SHAPE_ROW2", "candidate", candidate_value, row_variance, "frozen_shape_row_2")
    add(
        "control_redshift_order_shuffle_ROW2",
        "redshift_order_shuffle",
        shuffle_values[SHAPE_ROW],
        row_variance,
        "same_row_index_from_deterministic_source_side_shuffle_seed_41007",
    )
    add(
        "control_wrong_time_basis_rank_reverse_ROW2",
        "wrong_time_basis",
        rank_values[SHAPE_ROW],
        row_variance,
        "same_row_index_from_rank_reverse_first_difference_shape_vector",
    )
    add(
        "control_cc_window_stress_ROW2",
        "cc_window_stress",
        candidate_value,
        cc_stress_variance,
        "same_candidate_value_with_caveated_row4_window_stress_covariance_inflation",
    )
    add("control_rd_prior_stress_ROW2", "rd_prior_stress", 0.0, row_variance, "constant_beta_cancels")

    write_csv(GRID, rows)
    candidate = next(row for row in rows if row["branch"] == "candidate_CLOCK_SLOPE_SHAPE_ROW2")
    controls_only = [row for row in rows if row["branch"] != "candidate_CLOCK_SLOPE_SHAPE_ROW2"]
    best_control = max(controls_only, key=lambda row: float(row["shape_quadratic_score"]))
    controls_ge_candidate = [
        row for row in controls_only if float(row["shape_quadratic_score"]) >= float(candidate["shape_quadratic_score"])
    ]
    verdict = (
        "row2_permission_replay_candidate_exceeds_all_row2_controls_not_validation"
        if not controls_ge_candidate
        else "row2_permission_replay_candidate_not_control_resistant_not_validation"
    )
    summary = {
        "run_id": run["run_id"],
        "status": "ROW2_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION",
        "authorization_verdict": auth["verdict"],
        "shape_row": str(SHAPE_ROW),
        "z_interval": f"{shape['z_left']}-{shape['z_right']}",
        "candidate_branch": candidate["branch"],
        "branch_count": str(len(rows)),
        "row2_shape_value": f"{candidate_value:.12g}",
        "row2_shape_sigma": f"{row_sigma:.12g}",
        "candidate_shape_quadratic_score": candidate["shape_quadratic_score"],
        "best_control_branch": best_control["branch"],
        "best_control_shape_quadratic_score": best_control["shape_quadratic_score"],
        "delta_candidate_minus_best_control_score": f"{float(candidate['shape_quadratic_score']) - float(best_control['shape_quadratic_score']):.12g}",
        "controls_ge_candidate_score": str(len(controls_ge_candidate)),
        "family_survives_row2_controls": "true" if not controls_ge_candidate else "false",
        "endpoint_replay_allowed": "true",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": verdict,
    }
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI Shape Row2 Authorized Replay v1",
                "",
                "**Doc class:** permission-only diagnostic replay",
                "**Reader role:** reviewer / reproducibility auditor",
                "**Status:** not endpoint validation; not physical validation",
                "**Canonical parent:** Paper10 DESI shape Row2 gate ledger",
                "",
                "This diagnostic replay uses only the frozen Row2 shape row",
                f"`shape_row={SHAPE_ROW}` over `z={shape['z_left']}--{shape['z_right']}`.",
                "",
                "Summary:",
                "",
                f"- candidate score: `{summary['candidate_shape_quadratic_score']}`",
                f"- best control: `{summary['best_control_branch']}`",
                f"- best control score: `{summary['best_control_shape_quadratic_score']}`",
                f"- delta candidate minus best control: `{summary['delta_candidate_minus_best_control_score']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                CLAIM_BOUNDARY,
                "```",
                "",
            ]
        )
    )
    print(f"PAPER10_DESI_SHAPE_ROW2_AUTHORIZED_REPLAY_BUILT verdict={verdict}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_bound_control_vectors_policy_v1.csv"
CONTROL_SUITE = ROOT / "data/derived/paper10_desi_ordering_control_suite_v1.csv"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
CC_WINDOW_STRESS = ROOT / "data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_bound_control_vectors_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
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


def first_differences(values: np.ndarray, z: np.ndarray) -> np.ndarray:
    return np.diff(values) / np.diff(z)


def curvature(values: np.ndarray, z: np.ndarray) -> np.ndarray:
    out = []
    for i in range(len(z) - 2):
        dz_left = z[i + 1] - z[i]
        dz_right = z[i + 2] - z[i + 1]
        span = z[i + 2] - z[i]
        out.append(
            2.0
            * (
                (values[i] / (span * dz_left))
                - values[i + 1] * (1.0 / dz_left + 1.0 / dz_right) / span
                + (values[i + 2] / (span * dz_right))
            )
        )
    return np.array(out, dtype=float)


def fmt_vector(values: np.ndarray) -> str:
    return ";".join(f"{float(value):.12g}" for value in values)


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad shape-bound controls policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    controls = read_rows(CONTROL_SUITE)
    if {row["control_channel"] for row in controls} != {"K_null"}:
        raise SystemExit("all input controls must be K_null controls")
    cc_window = one_row(CC_WINDOW_STRESS)
    if cc_window["cc_window_stress_bound_to_shape_route"] != "true":
        raise SystemExit("CC-window stress must be bound before final shape-control ledger")
    if cc_window["endpoint_replay_allowed"] != "false":
        raise SystemExit("CC-window stress binding must not authorize replay")

    allowed_rows = [
        row
        for row in read_rows(CC_MATCH)
        if row["cc_support_status"] == "MATCHED_WITHIN_CC_RANGE" and int(row["radial_index"]) in [0, 1, 2, 3, 4]
    ]
    allowed_rows = sorted(allowed_rows, key=lambda row: int(row["radial_index"]))
    if len(allowed_rows) != 5:
        raise SystemExit("shape-bound controls require the five CC-matched rows")

    z = np.array([float(row["z_eff"]) for row in allowed_rows], dtype=float)
    beta_like = np.array(
        [float(row["minus_log_DH_over_rs"]) - float(row["nearest_cc_logH"]) for row in allowed_rows],
        dtype=float,
    )
    candidate_first = first_differences(beta_like, z)
    candidate_curvature = curvature(beta_like, z)

    rng = np.random.default_rng(41007)
    perm = rng.permutation(len(beta_like))
    shuffled_first = first_differences(beta_like[perm], z)
    reversed_first = first_differences(beta_like[::-1], z)
    leave_shape_rows = [f"drop_shape_row_{i}" for i in range(len(candidate_first))]

    rows = [
        {
            "gate_id": policy["gate_id"],
            "control_family": "redshift_order_shuffle",
            "control_binding_status": "bound_source_vector",
            "control_vector_family": "shuffled_adjacent_first_difference_beta_shape",
            "control_vector_values": fmt_vector(shuffled_first),
            "comparison_target": "CLOCK_SLOPE_SHAPE",
            "uses_endpoint_scores": "false",
            "uses_endpoint_residuals": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "control_family": "leave_row_or_pair",
            "control_binding_status": "bound_source_masks",
            "control_vector_family": "leave_shape_row_masks",
            "control_vector_values": ";".join(leave_shape_rows),
            "comparison_target": "CLOCK_SLOPE_SHAPE",
            "uses_endpoint_scores": "false",
            "uses_endpoint_residuals": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "control_family": "cc_window_stress",
            "control_binding_status": "bound_caveated_source_window_stress",
            "control_vector_family": "row4_cc_window_stress_components",
            "control_vector_values": (
                "strict_simon_bracket_bound=true|"
                "non_simon_strict_window_search_bound=true|"
                "caveated_near_window_context_bound=true|"
                f"release_policy={cc_window['cc_window_stress_release_policy']}"
            ),
            "comparison_target": "CLOCK_SLOPE_SHAPE",
            "uses_endpoint_scores": "false",
            "uses_endpoint_residuals": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "control_family": "wrong_time_basis",
            "control_binding_status": "bound_source_vectors",
            "control_vector_family": "curvature_and_rank_reverse_first_difference",
            "control_vector_values": f"curvature:{fmt_vector(candidate_curvature)}|rank_reverse:{fmt_vector(reversed_first)}",
            "comparison_target": "CLOCK_SLOPE_SHAPE",
            "uses_endpoint_scores": "false",
            "uses_endpoint_residuals": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "control_family": "rd_prior_stress",
            "control_binding_status": "bound_analytic_null_for_first_difference",
            "control_vector_family": "constant_beta_cancels_exactly",
            "control_vector_values": "delta_constant_beta_under_first_difference=0",
            "comparison_target": "CLOCK_SLOPE_SHAPE",
            "uses_endpoint_scores": "false",
            "uses_endpoint_residuals": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    bound_count = sum(not row["control_binding_status"].startswith("not_yet") for row in rows)
    summary = [
        {
            "gate_id": policy["gate_id"],
            "status": "DESI_SHAPE_BOUND_CONTROL_VECTORS_BUILT_NOT_REPLAY_NOT_VALIDATION",
            "required_control_count": str(len(rows)),
            "shape_bound_control_count": str(bound_count),
            "unbound_control_families": ";".join(row["control_family"] for row in rows if row["control_binding_status"].startswith("not_yet")) or "none",
            "candidate_shape_rows": str(len(candidate_first)),
            "curvature_shape_rows": str(len(candidate_curvature)),
            "redshift_shuffle_seed": "41007",
            "ordering_control_suite_shape_bound": "true" if bound_count == len(rows) else "false",
            "ordering_control_suite_ready_for_replay": "false",
            "blocks_replay_reason": "controls_are_shape_bound_but_cc_window_stress_is_caveated_and_separate_replay_authorization_is_missing",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "shape_route_controls_bound_but_replay_not_authorized",
        }
    ]
    write_csv(SUMMARY, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

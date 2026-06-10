#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
R1_R3_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r1_r3_source_attachment_v1_summary.csv"
GEOM = ROOT / "data" / "derived" / "low_z_pantheon_void_geometry_join_v1.csv"
ENV = ROOT / "data" / "derived" / "low_z_pantheon_los_environment_v1.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_r4_independence_preflight_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r4_independence_preflight_v1_summary.csv"

LOW_CORR_THRESHOLD = 0.30


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def maybe_float(value: str) -> float:
    if value == "":
        return math.nan
    return float(value)


def pearson(x_values: list[float], y_values: list[float]) -> tuple[float, int]:
    x = np.asarray(x_values, dtype=float)
    y = np.asarray(y_values, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    n = int(mask.sum())
    if n < 3:
        return math.nan, n
    x = x[mask]
    y = y[mask]
    if float(np.std(x)) == 0.0 or float(np.std(y)) == 0.0:
        return math.nan, n
    return float(np.corrcoef(x, y)[0, 1]), n


def rankdata(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + j - 1) / 2.0
        ranks[order[i:j]] = rank
        i = j
    return ranks


def spearman(x_values: list[float], y_values: list[float]) -> tuple[float, int]:
    x = np.asarray(x_values, dtype=float)
    y = np.asarray(y_values, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    n = int(mask.sum())
    if n < 3:
        return math.nan, n
    return pearson(rankdata(x[mask]).tolist(), rankdata(y[mask]).tolist())


def main() -> None:
    parent = read_one(R1_R3_SUMMARY)
    if parent["status"] != "R1_R3_SOURCE_ARTIFACTS_ATTACHED_R4_R6_STILL_OPEN":
        raise SystemExit("R4 preflight expects R1-R3 artifacts to be attached and R4-R6 open")
    if parent["endpoint_replay_allowed"] != "false":
        raise SystemExit("parent R1-R3 attachment must not allow replay")

    geom_rows = read_rows(GEOM)
    env_rows_by_idx = {row["source_row_index"]: row for row in read_rows(ENV)}
    if len(geom_rows) != int(parent["low_z_rows"]):
        raise SystemExit("geometry row count does not match parent low-z rows")

    z_values: list[float] = []
    source_indices: list[float] = []
    features: dict[str, list[float]] = {
        "nearest_void_center_distance_mpc_over_h": [],
        "wall_distance_mpc_over_h": [],
        "angular_separation_to_void_center_deg": [],
        "inside_effective_void_radius_binary": [],
        "los_environment_count": [],
        "los_matter_density_median": [],
        "nearest_environment_matter_density": [],
    }
    for row in geom_rows:
        env = env_rows_by_idx[row["source_row_index"]]
        z_values.append(float(row["zHD"]))
        source_indices.append(float(row["source_row_index"]))
        features["nearest_void_center_distance_mpc_over_h"].append(float(row["nearest_void_center_distance_mpc_over_h"]))
        features["wall_distance_mpc_over_h"].append(float(row["wall_distance_mpc_over_h"]))
        features["angular_separation_to_void_center_deg"].append(float(row["angular_separation_to_void_center_deg"]))
        features["inside_effective_void_radius_binary"].append(
            1.0 if row["inside_effective_void_radius"] == "true" else 0.0
        )
        features["los_environment_count"].append(float(env["los_environment_count"]))
        features["los_matter_density_median"].append(maybe_float(env["los_matter_density_median"]))
        features["nearest_environment_matter_density"].append(maybe_float(env["nearest_environment_matter_density"]))

    rows: list[dict[str, str]] = []
    low_corr_features = 0
    best_max_abs = math.inf
    best_feature = ""
    for feature_id, values in features.items():
        pearson_z, n_z = pearson(values, z_values)
        pearson_row, n_row = pearson(values, source_indices)
        spearman_z, _ = spearman(values, z_values)
        spearman_row, _ = spearman(values, source_indices)
        max_abs_corr = max(
            abs(x)
            for x in [pearson_z, pearson_row, spearman_z, spearman_row]
            if math.isfinite(x)
        )
        passes = max_abs_corr <= LOW_CORR_THRESHOLD
        if passes:
            low_corr_features += 1
        if max_abs_corr < best_max_abs:
            best_max_abs = max_abs_corr
            best_feature = feature_id
        rows.append(
            {
                "preflight_id": "VOID_SOURCE_BASIS_REFINEMENT_R4_INDEPENDENCE_PREFLIGHT_V1",
                "feature_id": feature_id,
                "n_used": str(min(n_z, n_row)),
                "pearson_r_with_zHD": f"{pearson_z:.12g}" if math.isfinite(pearson_z) else "",
                "pearson_r_with_source_row_index": f"{pearson_row:.12g}" if math.isfinite(pearson_row) else "",
                "spearman_r_with_zHD": f"{spearman_z:.12g}" if math.isfinite(spearman_z) else "",
                "spearman_r_with_source_row_index": f"{spearman_row:.12g}" if math.isfinite(spearman_row) else "",
                "max_abs_correlation": f"{max_abs_corr:.12g}",
                "low_correlation_threshold": f"{LOW_CORR_THRESHOLD:.12g}",
                "passes_low_correlation_preflight": str(passes).lower(),
                "endpoint_replay_allowed": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": "r4_independence_preflight_not_scoring_not_validation",
            }
        )

    status = (
        "R4_PREFLIGHT_FINDS_LOW_CORRELATION_CANDIDATES_R5_R6_STILL_OPEN"
        if low_corr_features > 0
        else "R4_PREFLIGHT_FAILS_LOW_CORRELATION_REQUIREMENT"
    )
    summary = [
        {
            "preflight_id": "VOID_SOURCE_BASIS_REFINEMENT_R4_INDEPENDENCE_PREFLIGHT_V1",
            "parent_attachment_id": parent["attachment_id"],
            "status": status,
            "features_tested": str(len(rows)),
            "features_passing_low_correlation": str(low_corr_features),
            "best_feature": best_feature,
            "best_feature_max_abs_correlation": f"{best_max_abs:.12g}",
            "low_correlation_threshold": f"{LOW_CORR_THRESHOLD:.12g}",
            "redshift_independence_preflight_complete": "true",
            "control_resistance_preflight_complete": "false",
            "leakage_review_complete": "false",
            "source_unique_ready": "false",
            "endpoint_replay_allowed": "false",
            "computes_new_scores": "false",
            "uses_distance_residuals": "false",
            "uses_fit_statistics": "false",
            "physical_validation_claimed": "false",
            "recommended_next_action": "build_R5_control_resistance_preflight_before_any_replay_request",
            "claim_boundary": "r4_independence_preflight_not_scoring_not_validation",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R4_INDEPENDENCE_PREFLIGHT_V1_BUILT "
        f"passing={low_corr_features}/{len(rows)} best={best_feature} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()

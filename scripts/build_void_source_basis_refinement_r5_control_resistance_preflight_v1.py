#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
R4 = ROOT / "data" / "derived" / "void_source_basis_refinement_r4_independence_preflight_v1.csv"
R4_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r4_independence_preflight_v1_summary.csv"
GEOM = ROOT / "data" / "derived" / "low_z_pantheon_void_geometry_join_v1.csv"
ENV = ROOT / "data" / "derived" / "low_z_pantheon_los_environment_v1.csv"
OUT_MANIFEST = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_resistance_preflight_v1.csv"
OUT_VECTORS = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_vectors_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv"

BASE_SEED = 20260610


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


def quantile(values: np.ndarray, q: float) -> float:
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return math.nan
    return float(np.quantile(values, q))


def normalized(values: np.ndarray) -> np.ndarray:
    mask = np.isfinite(values)
    out = np.zeros_like(values, dtype=float)
    if mask.sum() == 0:
        return out
    finite = values[mask]
    lo = float(np.min(finite))
    hi = float(np.max(finite))
    if hi <= lo:
        out[mask] = 0.0
    else:
        out[mask] = (finite - lo) / (hi - lo)
    return out


def load_feature_rows() -> tuple[list[dict[str, str]], dict[str, np.ndarray]]:
    geom_rows = read_rows(GEOM)
    env_by_idx = {row["source_row_index"]: row for row in read_rows(ENV)}
    features: dict[str, list[float]] = {
        "angular_separation_to_void_center_deg": [],
        "inside_effective_void_radius_binary": [],
        "los_environment_count": [],
        "los_matter_density_median": [],
        "nearest_environment_matter_density": [],
    }
    base_rows: list[dict[str, str]] = []
    for row in geom_rows:
        env = env_by_idx[row["source_row_index"]]
        base_rows.append(
            {
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
            }
        )
        features["angular_separation_to_void_center_deg"].append(float(row["angular_separation_to_void_center_deg"]))
        features["inside_effective_void_radius_binary"].append(
            1.0 if row["inside_effective_void_radius"] == "true" else 0.0
        )
        features["los_environment_count"].append(float(env["los_environment_count"]))
        features["los_matter_density_median"].append(maybe_float(env["los_matter_density_median"]))
        features["nearest_environment_matter_density"].append(maybe_float(env["nearest_environment_matter_density"]))
    return base_rows, {key: np.asarray(value, dtype=float) for key, value in features.items()}


def main() -> None:
    r4_summary = read_one(R4_SUMMARY)
    if r4_summary["redshift_independence_preflight_complete"] != "true":
        raise SystemExit("R5 expects R4 independence preflight complete")
    if r4_summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("R4 must not allow endpoint replay")
    if r4_summary["control_resistance_preflight_complete"] != "false":
        raise SystemExit("R5 should not already be complete in parent summary")

    passing_features = [
        row["feature_id"]
        for row in read_rows(R4)
        if row["passes_low_correlation_preflight"] == "true"
    ]
    if not passing_features:
        raise SystemExit("R5 requires at least one R4 low-correlation feature")

    base_rows, feature_values = load_feature_rows()
    missing = sorted(set(passing_features) - set(feature_values))
    if missing:
        raise SystemExit(f"R5 builder missing R4 passing features: {missing}")

    manifest_rows: list[dict[str, str]] = []
    vector_rows: list[dict[str, str]] = []
    control_families = [
        "zero_control",
        "wrong_sign_control",
        "deterministic_row_shuffle_control",
        "threshold_low_control",
        "threshold_high_control",
    ]
    for feature_index, feature_id in enumerate(passing_features):
        raw_values = feature_values[feature_id]
        candidate = normalized(raw_values)
        q25 = quantile(candidate, 0.25)
        q75 = quantile(candidate, 0.75)
        seed = BASE_SEED + feature_index
        rng = np.random.default_rng(seed)
        shuffled = candidate[rng.permutation(len(candidate))]
        threshold_low = np.where(candidate <= q25, 1.0, 0.0)
        threshold_high = np.where(candidate >= q75, 1.0, 0.0)
        controls = {
            "zero_control": np.zeros_like(candidate),
            "wrong_sign_control": -candidate,
            "deterministic_row_shuffle_control": shuffled,
            "threshold_low_control": threshold_low,
            "threshold_high_control": threshold_high,
        }
        for family in control_families:
            manifest_rows.append(
                {
                    "preflight_id": "VOID_SOURCE_BASIS_REFINEMENT_R5_CONTROL_RESISTANCE_PREFLIGHT_V1",
                    "feature_id": feature_id,
                    "control_family": family,
                    "seed": str(seed) if family == "deterministic_row_shuffle_control" else "",
                    "source_frozen_rule": {
                        "zero_control": "set_source_feature_to_zero",
                        "wrong_sign_control": "multiply_normalized_source_feature_by_minus_one",
                        "deterministic_row_shuffle_control": "permute_normalized_source_feature_by_frozen_seed",
                        "threshold_low_control": "binary_indicator_normalized_feature_at_or_below_source_q25",
                        "threshold_high_control": "binary_indicator_normalized_feature_at_or_above_source_q75",
                    }[family],
                    "source_q25": f"{q25:.12g}",
                    "source_q75": f"{q75:.12g}",
                    "control_vector_artifact": "data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv",
                    "endpoint_replay_allowed": "false",
                    "contains_endpoint_scores": "false",
                    "contains_distance_residuals": "false",
                    "contains_fit_statistics": "false",
                    "uses_posthoc_control_selection": "false",
                    "physical_validation_claimed": "false",
                    "claim_boundary": "r5_control_resistance_preflight_not_scoring_not_validation",
                }
            )
        for row_index, base in enumerate(base_rows):
            vector_rows.append(
                {
                    "preflight_id": "VOID_SOURCE_BASIS_REFINEMENT_R5_CONTROL_RESISTANCE_PREFLIGHT_V1",
                    "feature_id": feature_id,
                    **base,
                    "candidate_source_feature": f"{candidate[row_index]:.12g}",
                    "zero_control": f"{controls['zero_control'][row_index]:.12g}",
                    "wrong_sign_control": f"{controls['wrong_sign_control'][row_index]:.12g}",
                    "deterministic_row_shuffle_control": f"{controls['deterministic_row_shuffle_control'][row_index]:.12g}",
                    "threshold_low_control": f"{controls['threshold_low_control'][row_index]:.12g}",
                    "threshold_high_control": f"{controls['threshold_high_control'][row_index]:.12g}",
                    "endpoint_replay_allowed": "false",
                    "contains_endpoint_scores": "false",
                    "contains_distance_residuals": "false",
                    "contains_fit_statistics": "false",
                    "physical_validation_claimed": "false",
                    "claim_boundary": "r5_control_resistance_preflight_not_scoring_not_validation",
                }
            )

    summary = [
        {
            "preflight_id": "VOID_SOURCE_BASIS_REFINEMENT_R5_CONTROL_RESISTANCE_PREFLIGHT_V1",
            "parent_preflight_id": r4_summary["preflight_id"],
            "status": "R5_CONTROL_RESISTANCE_PREFLIGHT_FROZEN_R6_STILL_OPEN",
            "features_admitted_from_R4": str(len(passing_features)),
            "control_families_per_feature": str(len(control_families)),
            "control_manifest_rows": str(len(manifest_rows)),
            "control_vector_rows": str(len(vector_rows)),
            "base_seed": str(BASE_SEED),
            "control_resistance_preflight_complete": "true",
            "leakage_review_complete": "false",
            "source_unique_ready": "false",
            "endpoint_replay_allowed": "false",
            "computes_new_scores": "false",
            "uses_distance_residuals": "false",
            "uses_fit_statistics": "false",
            "physical_validation_claimed": "false",
            "recommended_next_action": "complete_R6_independent_leakage_review_before_any_replay_request",
            "claim_boundary": "r5_control_resistance_preflight_not_scoring_not_validation",
        }
    ]
    write_csv(OUT_MANIFEST, manifest_rows)
    write_csv(OUT_VECTORS, vector_rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R5_CONTROL_RESISTANCE_PREFLIGHT_V1_BUILT "
        f"features={len(passing_features)} controls={len(manifest_rows)} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()

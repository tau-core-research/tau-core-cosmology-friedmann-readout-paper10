#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
R4 = ROOT / "data" / "derived" / "void_source_basis_refinement_r4_independence_preflight_v1.csv"
R4_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r4_independence_preflight_v1_summary.csv"
MANIFEST = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_resistance_preflight_v1.csv"
VECTORS = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_vectors_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv"

EXPECTED_CONTROLS = {
    "zero_control",
    "wrong_sign_control",
    "deterministic_row_shuffle_control",
    "threshold_low_control",
    "threshold_high_control",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def as_float(value: str, label: str) -> float:
    try:
        out = float(value)
    except ValueError as exc:
        raise SystemExit(f"{label} must be numeric: {value}") from exc
    require(math.isfinite(out), f"{label} must be finite")
    return out


def sorted_close(left: list[float], right: list[float], tol: float = 1e-10) -> bool:
    if len(left) != len(right):
        return False
    return all(abs(a - b) <= tol for a, b in zip(sorted(left), sorted(right)))


def main() -> None:
    r4_summary = read_one(R4_SUMMARY)
    r4_rows = read_rows(R4)
    manifest = read_rows(MANIFEST)
    vectors = read_rows(VECTORS)
    summary = read_one(SUMMARY)

    require(r4_summary["redshift_independence_preflight_complete"] == "true", "R4 must be complete")
    require(r4_summary["endpoint_replay_allowed"] == "false", "R4 must not allow endpoint replay")
    require(summary["status"] == "R5_CONTROL_RESISTANCE_PREFLIGHT_FROZEN_R6_STILL_OPEN", "bad R5 status")
    require(summary["control_resistance_preflight_complete"] == "true", "R5 should be complete")
    require(summary["leakage_review_complete"] == "false", "R6 must remain open")
    require(summary["source_unique_ready"] == "false", "R5 alone must not claim source uniqueness")
    for key in [
        "endpoint_replay_allowed",
        "computes_new_scores",
        "uses_distance_residuals",
        "uses_fit_statistics",
        "physical_validation_claimed",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")

    passing_features = [
        row["feature_id"]
        for row in r4_rows
        if row["passes_low_correlation_preflight"] == "true"
    ]
    require(passing_features, "R5 requires at least one R4-passing feature")
    require(int(summary["features_admitted_from_R4"]) == len(passing_features), "R4 feature count mismatch")
    require(int(summary["control_families_per_feature"]) == len(EXPECTED_CONTROLS), "control family count mismatch")
    require(int(summary["control_manifest_rows"]) == len(manifest), "manifest row count mismatch")
    require(int(summary["control_vector_rows"]) == len(vectors), "vector row count mismatch")
    require(len(manifest) == len(passing_features) * len(EXPECTED_CONTROLS), "unexpected manifest size")
    require(len(vectors) > 0, "vector artifact must not be empty")

    controls_by_feature: dict[str, set[str]] = defaultdict(set)
    for row in manifest:
        require(row["feature_id"] in passing_features, f"manifest includes non-admitted feature {row['feature_id']}")
        controls_by_feature[row["feature_id"]].add(row["control_family"])
        require(row["control_family"] in EXPECTED_CONTROLS, f"unexpected control family {row['control_family']}")
        for key in [
            "endpoint_replay_allowed",
            "contains_endpoint_scores",
            "contains_distance_residuals",
            "contains_fit_statistics",
            "uses_posthoc_control_selection",
            "physical_validation_claimed",
        ]:
            require(row[key] == "false", f"manifest row must keep {key}=false")
        q25 = as_float(row["source_q25"], "source_q25")
        q75 = as_float(row["source_q75"], "source_q75")
        require(0.0 <= q25 <= q75 <= 1.0, "source quantiles must be normalized and ordered")
        if row["control_family"] == "deterministic_row_shuffle_control":
            require(row["seed"], "shuffle control must record seed")
        else:
            require(row["seed"] == "", "non-shuffle controls must not record a seed")
    for feature_id in passing_features:
        require(controls_by_feature[feature_id] == EXPECTED_CONTROLS, f"missing controls for {feature_id}")

    candidates_by_feature: dict[str, list[float]] = defaultdict(list)
    shuffles_by_feature: dict[str, list[float]] = defaultdict(list)
    source_rows_by_feature: dict[str, set[str]] = defaultdict(set)
    for row in vectors:
        feature_id = row["feature_id"]
        require(feature_id in passing_features, f"vector includes non-admitted feature {feature_id}")
        for key in [
            "endpoint_replay_allowed",
            "contains_endpoint_scores",
            "contains_distance_residuals",
            "contains_fit_statistics",
            "physical_validation_claimed",
        ]:
            require(row[key] == "false", f"vector row must keep {key}=false")
        candidate = as_float(row["candidate_source_feature"], "candidate_source_feature")
        zero = as_float(row["zero_control"], "zero_control")
        wrong = as_float(row["wrong_sign_control"], "wrong_sign_control")
        shuffle = as_float(row["deterministic_row_shuffle_control"], "deterministic_row_shuffle_control")
        low = as_float(row["threshold_low_control"], "threshold_low_control")
        high = as_float(row["threshold_high_control"], "threshold_high_control")
        require(0.0 <= candidate <= 1.0, "candidate source feature must be normalized")
        require(zero == 0.0, "zero control must be exactly zero")
        require(abs(wrong + candidate) <= 1e-10, "wrong-sign control must be the negative candidate")
        require(0.0 <= shuffle <= 1.0, "shuffle control must remain normalized")
        require(low in {0.0, 1.0}, "low-threshold control must be binary")
        require(high in {0.0, 1.0}, "high-threshold control must be binary")
        candidates_by_feature[feature_id].append(candidate)
        shuffles_by_feature[feature_id].append(shuffle)
        source_rows_by_feature[feature_id].add(row["source_row_index"])

    row_counts = {len(rows) for rows in source_rows_by_feature.values()}
    require(len(row_counts) == 1, "all admitted features must cover the same source rows")
    for feature_id in passing_features:
        require(
            sorted_close(candidates_by_feature[feature_id], shuffles_by_feature[feature_id]),
            f"shuffle control is not a permutation for {feature_id}",
        )

    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R5_CONTROL_RESISTANCE_PREFLIGHT_V1_VALIDATED "
        f"features={len(passing_features)} controls={len(manifest)} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()

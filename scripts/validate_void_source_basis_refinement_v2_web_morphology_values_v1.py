#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_web_morphology_values.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_web_morphology_values_summary.csv"

COMPONENT_ID = "V2_WEB_MORPHOLOGY"
SEED = "20260610"
CLAIM_BOUNDARY = "v2_web_morphology_source_values_frozen_not_scoring_not_validation"


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


def rounded_multiset(values: list[float]) -> list[float]:
    return sorted(round(value, 12) for value in values)


def main() -> None:
    rows = read_rows(VALUES)
    summary = read_one(SUMMARY)
    require(rows, "values table is empty")
    require(summary["component_id"] == COMPONENT_ID, "summary component mismatch")
    require(summary["status"] == "V2_WEB_MORPHOLOGY_VALUES_FROZEN_NOT_ENDPOINT_READY", "bad summary status")
    require(summary["n_rows"] == str(len(rows)), "summary row count mismatch")
    require(summary["deterministic_shuffle_seed"] == SEED, "summary seed mismatch")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")

    raw_values: list[float] = []
    shuffled_values: list[float] = []
    for row in rows:
        require(row["component_id"] == COMPONENT_ID, "row component mismatch")
        require(row["channel_id"] == "W_WEB_ANISOTROPY", "row channel mismatch")
        require(row["deterministic_shuffle_seed"] == SEED, "row seed mismatch")
        require(row["endpoint_replay_allowed"] == "false", "rows must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "rows must not claim endpoint validation")
        require(row["contains_endpoint_scores"] == "false", "rows must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "rows must not contain distance residuals")
        require(row["contains_fit_statistics"] == "false", "rows must not contain fit statistics")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        raw = float(row["W_web_source_native_basis"])
        centered = float(row["W_web_centered"])
        rank = float(row["W_web_rank_quantile"])
        require(0.0 <= raw <= 1.0, "raw W_web must stay in source-native [0,1] range")
        require(0.0 <= rank <= 1.0, "rank quantile must be in [0,1]")
        require(abs(float(row["W_web_abs_centered"]) - abs(centered)) < 1e-10, "abs centered mismatch")
        require(float(row["web_off_control"]) == 0.0, "off control must be zero")
        require(abs(float(row["web_wrong_sign_control"]) + raw) < 1e-10, "wrong-sign control mismatch")
        require(row["web_low_quartile_control"] in {"0", "1"}, "low quartile control must be binary")
        require(row["web_high_quartile_control"] in {"0", "1"}, "high quartile control must be binary")
        raw_values.append(raw)
        shuffled_values.append(float(row["web_deterministic_row_shuffle_control"]))

    require(
        rounded_multiset(raw_values) == rounded_multiset(shuffled_values),
        "deterministic shuffle must be a permutation of raw W_web values",
    )
    require(int(summary["web_nonzero_count"]) == sum(1 for value in raw_values if value != 0.0), "nonzero count mismatch")
    require(abs(float(summary["web_min"]) - min(raw_values)) < 1e-10, "summary min mismatch")
    require(abs(float(summary["web_max"]) - max(raw_values)) < 1e-10, "summary max mismatch")
    require(
        summary["verdict"] == "web_morphology_values_frozen_not_endpoint_ready",
        "unexpected web morphology verdict",
    )
    print(
        "PAPER10_V2_WEB_MORPHOLOGY_VALUES_VALIDATED "
        f"rows={len(rows)} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_void_morphology_values.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_void_morphology_values_summary.csv"

COMPONENT_ID = "V2_VOID_MORPHOLOGY"
CLAIM_BOUNDARY = "v2_void_morphology_source_values_frozen_weak_negative_not_scoring_not_validation"
NEGATIVE_VERDICT = "candidate_signal_not_source_specific_shuffled_control_dominates_without_redshift_leak"


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
    require(rows, "void values table is empty")
    require(summary["component_id"] == COMPONENT_ID, "summary component mismatch")
    require(
        summary["status"] == "V2_VOID_MORPHOLOGY_VALUES_FROZEN_WEAK_NEGATIVE_NOT_ENDPOINT_READY",
        "bad summary status",
    )
    require(summary["n_rows"] == str(len(rows)), "row count mismatch")
    require(summary["weak_negative_status_inherited"] == "true", "weak negative status must be inherited")
    require(summary["control_dominance_verdict"] == NEGATIVE_VERDICT, "control dominance verdict mismatch")
    require(summary["candidate_improves_chi2_over_baseline"] == "true", "candidate chi2 improvement fact changed")
    require(summary["candidate_loses_aic_to_baseline"] == "true", "candidate AIC loss fact changed")
    require(summary["best_control_beats_candidate_chi2"] == "true", "best control dominance fact changed")
    require(summary["best_control_is_row_shuffle"] == "true", "row-shuffle control fact changed")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(summary["verdict"] == "void_morphology_values_frozen_but_weak_negative_preserved", "bad verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")

    raw_values: list[float] = []
    shuffled_values: list[float] = []
    for row in rows:
        require(row["component_id"] == COMPONENT_ID, "row component mismatch")
        require(row["channel_id"] == "W_VOID_MATURITY", "row channel mismatch")
        raw = float(row["W_void_source_native_basis"])
        centered = float(row["W_void_centered"])
        require(raw > 0.0, "included low-z rows should have positive void support")
        require(0.0 <= float(row["W_void_rank_quantile"]) <= 1.0, "rank quantile out of range")
        require(abs(float(row["W_void_abs_centered"]) - abs(centered)) < 1e-10, "abs centered mismatch")
        require(row["void_off_control"] == "0", "off control must be zero")
        require(abs(float(row["void_wrong_sign_control"]) + raw) < 1e-10, "wrong sign control mismatch")
        require(row["void_low_quartile_control"] in {"0", "1"}, "low quartile control must be binary")
        require(row["void_high_quartile_control"] in {"0", "1"}, "high quartile control must be binary")
        require(row["weak_negative_status_inherited"] == "true", "row weak negative flag missing")
        require(row["control_dominance_verdict"] == NEGATIVE_VERDICT, "row control dominance verdict mismatch")
        require(row["endpoint_replay_allowed"] == "false", "rows must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "rows must not claim validation")
        require(row["contains_endpoint_scores"] == "false", "rows must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "rows must not contain distance residuals")
        require(row["contains_fit_statistics"] == "false", "rows must not contain fit statistics")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        raw_values.append(raw)
        shuffled_values.append(float(row["void_deterministic_row_shuffle_control"]))
    require(
        rounded_multiset(raw_values) == rounded_multiset(shuffled_values),
        "deterministic void shuffle must be a permutation of raw values",
    )
    print(
        "PAPER10_V2_VOID_MORPHOLOGY_VALUES_VALIDATED "
        f"rows={len(rows)} weak_negative_preserved=true"
    )


if __name__ == "__main__":
    main()

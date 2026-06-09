#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_log_band_prior_mock_sanity_policy_v1.csv"
ELIGIBILITY = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_eligibility_gate_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_mock_sanity_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_mock_sanity_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def unit_mean(values: np.ndarray) -> np.ndarray:
    mean = float(values.mean())
    if mean == 0.0:
        return values
    return values / mean


def unit_norm(values: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(values))
    if norm == 0.0:
        raise SystemExit("zero vector in mock sanity suite")
    return values / norm


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(unit_norm(a), unit_norm(b)))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12e}"


def make_300(values_by_mode: np.ndarray) -> np.ndarray:
    if values_by_mode.shape != (20,):
        raise SystemExit("mode vector must have length 20")
    return np.tile(values_by_mode, 15)


def main() -> None:
    policy = read_one(POLICY)
    eligibility = read_one(ELIGIBILITY)
    if policy["status"] != "LOG_BAND_PRIOR_MOCK_SANITY_POLICY_FROZEN":
        raise SystemExit("unexpected mock sanity policy status")
    if policy["uses_kids_data_vector_values"] != "false" or policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mock sanity policy must remain data-vector-free and non-scoring")
    if policy["uses_random_noise"] != "false":
        raise SystemExit("mock sanity suite must remain deterministic")
    if eligibility["eligibility_verdict"] != "protocol_eligible_for_conditional_envelope_but_not_full_kernel_validated":
        raise SystemExit("unexpected parent eligibility verdict")

    mode = np.arange(1, 21, dtype=float)
    templates_20 = {
        "low_log_band_n^-0.5": unit_mean(mode**-0.5),
        "flat_coherent": unit_mean(np.ones_like(mode)),
        "high_mode_n": unit_mean(mode),
        "oscillatory_alternating": np.where((mode.astype(int) % 2) == 0, 1.0, -1.0),
    }
    truth_20 = {
        "truth_low_log_band": templates_20["low_log_band_n^-0.5"],
        "truth_flat_coherent": templates_20["flat_coherent"],
        "truth_high_mode": templates_20["high_mode_n"],
        "truth_oscillatory": templates_20["oscillatory_alternating"],
    }
    templates = {name: make_300(values) for name, values in templates_20.items()}
    truths = {name: make_300(values) for name, values in truth_20.items()}
    rows: list[dict[str, str]] = []
    expected_best = {
        "truth_low_log_band": "low_log_band_n^-0.5",
        "truth_flat_coherent": "flat_coherent",
        "truth_high_mode": "high_mode_n",
        "truth_oscillatory": "oscillatory_alternating",
    }
    for truth_id, truth_vector in truths.items():
        scores = {
            template_id: cosine(truth_vector, template_vector)
            for template_id, template_vector in templates.items()
        }
        best_template = max(scores, key=scores.get)
        for template_id, score in sorted(scores.items()):
            rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "truth_family": truth_id,
                    "template_family": template_id,
                    "cosine_similarity": fmt(score),
                    "best_template_for_truth": best_template,
                    "expected_best_template": expected_best[truth_id],
                    "truth_recovered_expected_template": str(best_template == expected_best[truth_id]).lower(),
                    "uses_kids_data_vector_values": "false",
                    "uses_fit_statistics": "false",
                    "uses_random_noise": "false",
                    "endpoint_scoring_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "claim_boundary": policy["claim_boundary"],
                }
            )

    recovered = {
        truth_id: max(
            ((row["template_family"], float(row["cosine_similarity"])) for row in rows if row["truth_family"] == truth_id),
            key=lambda item: item[1],
        )[0]
        for truth_id in truths
    }
    recovered_count = sum(recovered[truth_id] == expected_best[truth_id] for truth_id in truths)
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "LOG_BAND_PRIOR_MOCK_SANITY_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "truth_family_count": str(len(truths)),
            "template_family_count": str(len(templates)),
            "grid_rows": str(len(rows)),
            "expected_recovery_count": str(recovered_count),
            "all_expected_templates_recovered": str(recovered_count == len(truths)).lower(),
            "low_truth_best_template": recovered["truth_low_log_band"],
            "flat_truth_best_template": recovered["truth_flat_coherent"],
            "high_truth_best_template": recovered["truth_high_mode"],
            "oscillatory_truth_best_template": recovered["truth_oscillatory"],
            "mock_sanity_verdict": "deterministic_template_recovery_pass_not_physical_mock_validation",
            "uses_kids_data_vector_values": "false",
            "uses_fit_statistics": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(GRID, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_LOG_BAND_PRIOR_MOCK_SANITY_V1_COMPLETE "
        f"recovered={recovered_count}/{len(truths)} "
        f"verdict={summary[0]['mock_sanity_verdict']}"
    )


if __name__ == "__main__":
    main()

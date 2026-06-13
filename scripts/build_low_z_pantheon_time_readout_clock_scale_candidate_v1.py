#!/usr/bin/env python3
from __future__ import annotations

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_time_readout_clock_scale_candidate_policy_v1.csv"
SOURCE_AUDIT = ROOT / "data/derived/low_z_pantheon_time_readout_source_audit_v1_summary.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1_summary.csv"
CLAIM_BOUNDARY = "time_readout_clock_scale_candidate_source_side_not_scoring_not_validation"


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


def load_cc_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with CC_HZ.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            z, hz, err, reference = line.strip().split(",", 3)
            rows.append({"z": z, "Hz": hz, "errHz": err, "reference": reference})
    if not rows:
        raise SystemExit("CC H(z) table is empty")
    return rows


def quantile(sorted_values: list[float], fraction: float) -> float:
    if not sorted_values:
        raise SystemExit("cannot compute quantile of empty list")
    idx = min(len(sorted_values) - 1, max(0, round(fraction * (len(sorted_values) - 1))))
    return sorted_values[idx]


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "TIME_READOUT_CLOCK_SCALE_CANDIDATE_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("clock scale candidate policy must not authorize replay or validation")
    source_audit = read_one(SOURCE_AUDIT)
    if source_audit["verdict"] != "time_readout_sources_partially_available_but_delta_clock_rule_missing":
        raise SystemExit("unexpected parent source audit verdict")
    cc_rows = load_cc_rows()
    rows: list[dict[str, str]] = []
    fractional = []
    for row in cc_rows:
        hz = float(row["Hz"])
        err = float(row["errHz"])
        frac = err / hz
        fractional.append(frac)
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_CLOCK_SCALE_CANDIDATE_V1",
                "z": row["z"],
                "Hz": row["Hz"],
                "errHz": row["errHz"],
                "fractional_hz_uncertainty": f"{frac:.12g}",
                "reference": row["reference"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_late_time_fit_parameters": "false",
                "contains_fit_statistics": "false",
                "uses_posthoc_hz_smoothing": "false",
                "uses_posthoc_clock_anomaly_labels": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    fractional_sorted = sorted(fractional)
    delta_clock_star = statistics.median(fractional)
    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_CLOCK_SCALE_CANDIDATE_V1",
            "status": "TIME_READOUT_CLOCK_SCALE_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING",
            "cc_hz_row_count": str(len(rows)),
            "cc_hz_min_z": f"{min(float(row['z']) for row in rows):.12g}",
            "cc_hz_max_z": f"{max(float(row['z']) for row in rows):.12g}",
            "delta_clock_star_candidate_rule": "median_errHz_over_Hz_from_CC_table",
            "delta_clock_star_candidate": f"{delta_clock_star:.12g}",
            "fractional_uncertainty_q16": f"{quantile(fractional_sorted, 0.16):.12g}",
            "fractional_uncertainty_q84": f"{quantile(fractional_sorted, 0.84):.12g}",
            "redshift_bin_policy_candidate": "source_native_CC_support_bins_no_residual_smoothing",
            "delta_clock_values_computed": "false",
            "W_time_values_computed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "delta_clock_star_candidate_frozen_but_delta_clock_and_w_time_missing",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_TIME_READOUT_CLOCK_SCALE_CANDIDATE_BUILT "
        f"cc_rows={summary[0]['cc_hz_row_count']} "
        f"delta_clock_star_candidate={summary[0]['delta_clock_star_candidate']} "
        "w_time=false"
    )


if __name__ == "__main__":
    main()

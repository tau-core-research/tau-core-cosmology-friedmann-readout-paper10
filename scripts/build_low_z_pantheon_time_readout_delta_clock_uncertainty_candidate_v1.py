#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_policy_v1.csv"
CLOCK_SCALE = ROOT / "data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1_summary.csv"
BIN_POLICY = ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.csv"
BIN_POLICY_SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1_summary.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1_summary.csv"
CLAIM_BOUNDARY = "time_readout_delta_clock_uncertainty_candidate_source_side_not_scoring_not_validation"


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
            frac = float(err) / float(hz)
            rows.append(
                {
                    "z": z,
                    "Hz": hz,
                    "errHz": err,
                    "fractional_hz_uncertainty": f"{frac:.12g}",
                    "reference": reference,
                }
            )
    if not rows:
        raise SystemExit("CC H(z) table is empty")
    return sorted(rows, key=lambda row: float(row["z"]))


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "TIME_READOUT_DELTA_CLOCK_UNCERTAINTY_CANDIDATE_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("Delta_clock uncertainty candidate policy must not authorize replay or validation")
    clock_scale = read_one(CLOCK_SCALE)
    if clock_scale["verdict"] != "delta_clock_star_candidate_frozen_but_delta_clock_and_w_time_missing":
        raise SystemExit("unexpected parent clock-scale verdict")
    bin_summary = read_one(BIN_POLICY_SUMMARY)
    if bin_summary["verdict"] != "redshift_bin_policy_candidate_frozen_but_delta_clock_and_w_time_missing":
        raise SystemExit("unexpected parent redshift-bin verdict")

    delta_clock_star = float(clock_scale["delta_clock_star_candidate"])
    if not (0.0 < delta_clock_star < 1.0):
        raise SystemExit("Delta_clock_star candidate must be a positive bounded fractional scale")
    cc_rows = load_cc_rows()
    bin_rows = read_rows(BIN_POLICY)

    rows: list[dict[str, str]] = []
    values: list[float] = []
    for row in bin_rows:
        idx = int(row["assigned_cc_bin_index"])
        cc = cc_rows[idx]
        frac = float(cc["fractional_hz_uncertainty"])
        delta_clock = math.log(frac / delta_clock_star)
        values.append(delta_clock)
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_DELTA_CLOCK_UNCERTAINTY_CANDIDATE_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "assigned_cc_bin_index": row["assigned_cc_bin_index"],
                "assigned_cc_bin_center_z": row["assigned_cc_bin_center_z"],
                "assigned_cc_fractional_hz_uncertainty": cc["fractional_hz_uncertainty"],
                "delta_clock_star_candidate": f"{delta_clock_star:.12g}",
                "Delta_clock_uncertainty_candidate": f"{delta_clock:.12g}",
                "Delta_clock_candidate_interpretation": "CC_fractional_uncertainty_contrast_not_clock_drift",
                "W_time_value_status": "NOT_COMPUTED_DELTA_CLOCK_UNCERTAINTY_CANDIDATE_ONLY",
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

    by_bin: dict[str, list[float]] = {}
    for row in rows:
        by_bin.setdefault(row["assigned_cc_bin_index"], []).append(
            float(row["Delta_clock_uncertainty_candidate"])
        )
    bin_means = [
        f"{key}:{sum(vals) / len(vals):.12g}"
        for key, vals in sorted(by_bin.items(), key=lambda item: int(item[0]))
    ]
    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_DELTA_CLOCK_UNCERTAINTY_CANDIDATE_V1",
            "status": "TIME_READOUT_DELTA_CLOCK_UNCERTAINTY_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "cc_hz_row_count": str(len(cc_rows)),
            "used_cc_bin_count": bin_summary["used_cc_bin_count"],
            "delta_clock_star_candidate": f"{delta_clock_star:.12g}",
            "delta_clock_rule": "log_assigned_CC_fractional_uncertainty_over_CC_median_fractional_uncertainty",
            "delta_clock_min": f"{min(values):.12g}",
            "delta_clock_max": f"{max(values):.12g}",
            "delta_clock_mean": f"{sum(values) / len(values):.12g}",
            "delta_clock_bin_means": ";".join(bin_means),
            "W_time_values_computed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "delta_clock_uncertainty_candidate_frozen_but_w_time_missing",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_TIME_READOUT_DELTA_CLOCK_UNCERTAINTY_CANDIDATE_BUILT "
        f"rows={summary[0]['rows']} "
        f"delta_clock_range=[{summary[0]['delta_clock_min']},{summary[0]['delta_clock_max']}] "
        "w_time=false"
    )


if __name__ == "__main__":
    main()

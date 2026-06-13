#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_time_readout_clock_rate_phase_candidate_policy_v1.csv"
BIN_POLICY = ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.csv"
BIN_SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1_summary.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1_summary.csv"
CLAIM_BOUNDARY = "time_readout_clock_rate_phase_candidate_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_cc_rows() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    with CC_HZ.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            z, hz, err, reference = line.strip().split(",", 3)
            rows.append({"z": float(z), "Hz": float(hz), "errHz": float(err), "reference": reference})
    if len(rows) < 3:
        raise SystemExit("need at least three CC rows for finite-difference slope")
    return sorted(rows, key=lambda row: float(row["z"]))


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def std(values: list[float], center: float) -> float:
    return math.sqrt(sum((value - center) ** 2 for value in values) / len(values))


def normalize(values: list[float]) -> tuple[list[float], float, float]:
    center = mean(values)
    scale = std(values, center)
    if scale <= 0:
        raise SystemExit("degenerate source vector")
    return [(value - center) / scale for value in values], center, scale


def logh_slope(cc_rows: list[dict[str, float | str]], idx: int) -> float:
    if idx <= 0:
        left, right = 0, 1
    elif idx >= len(cc_rows) - 1:
        left, right = len(cc_rows) - 2, len(cc_rows) - 1
    else:
        left, right = idx - 1, idx + 1
    z_left = float(cc_rows[left]["z"])
    z_right = float(cc_rows[right]["z"])
    h_left = float(cc_rows[left]["Hz"])
    h_right = float(cc_rows[right]["Hz"])
    denom = math.log1p(z_right) - math.log1p(z_left)
    if denom == 0:
        raise SystemExit("degenerate CC redshift support")
    return (math.log(h_right) - math.log(h_left)) / denom


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "TIME_READOUT_CLOCK_RATE_PHASE_CANDIDATE_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("bad policy status")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("policy must not authorize replay or validation")
    bin_summary = read_one(BIN_SUMMARY)
    if bin_summary["verdict"] != "redshift_bin_policy_candidate_frozen_but_delta_clock_and_w_time_missing":
        raise SystemExit("unexpected parent bin-policy verdict")
    cc_rows = load_cc_rows()
    bin_rows = read_rows(BIN_POLICY)

    raw_rows: list[dict[str, str | float]] = []
    level_raw: list[float] = []
    slope_raw: list[float] = []
    for row in bin_rows:
        idx = int(row["assigned_cc_bin_index"])
        cc = cc_rows[idx]
        level = math.log(float(cc["Hz"]))
        slope = logh_slope(cc_rows, idx)
        level_raw.append(level)
        slope_raw.append(slope)
        raw_rows.append(
            {
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "assigned_cc_bin_index": row["assigned_cc_bin_index"],
                "assigned_cc_bin_center_z": row["assigned_cc_bin_center_z"],
                "assigned_cc_Hz": f"{float(cc['Hz']):.12g}",
                "assigned_cc_reference": str(cc["reference"]),
                "clock_logH_level_raw": f"{level:.12g}",
                "clock_dlogH_dlog1pz_slope_raw": f"{slope:.12g}",
            }
        )
    level_basis, level_center, level_scale = normalize(level_raw)
    slope_basis, slope_center, slope_scale = normalize(slope_raw)
    phase_raw = [a * b for a, b in zip(level_basis, slope_basis)]
    phase_basis, phase_center, phase_scale = normalize(phase_raw)

    rows: list[dict[str, str]] = []
    for raw, level, slope, phase in zip(raw_rows, level_basis, slope_basis, phase_basis):
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_CLOCK_RATE_PHASE_CANDIDATE_V1",
                **{key: str(value) for key, value in raw.items()},
                "W_time_clock_level_basis": f"{level:.12g}",
                "W_time_clock_slope_basis": f"{slope:.12g}",
                "W_time_clock_phase_basis": f"{phase:.12g}",
                "normalization_rule": "source_mean_std_over_low_z_rows",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_late_time_fit_parameters": "false",
                "contains_fit_statistics": "false",
                "uses_posthoc_hz_smoothing": "false",
                "uses_posthoc_clock_anomaly_labels": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_CLOCK_RATE_PHASE_CANDIDATE_V1",
            "status": "TIME_READOUT_CLOCK_RATE_PHASE_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "cc_hz_row_count": str(len(cc_rows)),
            "used_cc_bin_count": bin_summary["used_cc_bin_count"],
            "level_center": f"{level_center:.12g}",
            "level_scale": f"{level_scale:.12g}",
            "slope_center": f"{slope_center:.12g}",
            "slope_scale": f"{slope_scale:.12g}",
            "phase_center": f"{phase_center:.12g}",
            "phase_scale": f"{phase_scale:.12g}",
            "level_basis_range": f"{min(level_basis):.12g};{max(level_basis):.12g}",
            "slope_basis_range": f"{min(slope_basis):.12g};{max(slope_basis):.12g}",
            "phase_basis_range": f"{min(phase_basis):.12g};{max(phase_basis):.12g}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "clock_rate_phase_candidate_frozen_source_side_not_endpoint_authorized",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_CLOCK_RATE_PHASE_CANDIDATE_BUILT "
        f"rows={summary[0]['rows']} phase_range={summary[0]['phase_basis_range']}"
    )


if __name__ == "__main__":
    main()

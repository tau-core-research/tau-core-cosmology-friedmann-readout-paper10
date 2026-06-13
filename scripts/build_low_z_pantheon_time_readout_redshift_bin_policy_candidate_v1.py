#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_time_readout_redshift_bin_policy_candidate_policy_v1.csv"
SOURCE_AUDIT = ROOT / "data/derived/low_z_pantheon_time_readout_source_audit_v1_summary.csv"
CLOCK_SCALE = ROOT / "data/derived/low_z_pantheon_time_readout_clock_scale_candidate_v1_summary.csv"
LOW_Z_MASK = ROOT / "data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1_summary.csv"
CLAIM_BOUNDARY = "time_readout_redshift_bin_policy_candidate_source_side_not_scoring_not_validation"


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
    return sorted(rows, key=lambda row: float(row["z"]))


def nearest_index(value: float, candidates: list[float]) -> int:
    if not candidates:
        raise SystemExit("candidate list is empty")
    return min(range(len(candidates)), key=lambda idx: abs(value - candidates[idx]))


def nearest_delta(value: float, candidates: list[float]) -> float:
    return min(abs(value - candidate) for candidate in candidates)


def build_cc_cells(cc_z: list[float]) -> list[tuple[float, float]]:
    cells: list[tuple[float, float]] = []
    for idx, z in enumerate(cc_z):
        lower = 0.0 if idx == 0 else 0.5 * (cc_z[idx - 1] + z)
        upper = math.inf if idx == len(cc_z) - 1 else 0.5 * (z + cc_z[idx + 1])
        cells.append((lower, upper))
    return cells


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("redshift bin policy must not authorize replay or validation")
    source_audit = read_one(SOURCE_AUDIT)
    if source_audit["verdict"] != "time_readout_sources_partially_available_but_delta_clock_rule_missing":
        raise SystemExit("unexpected parent source audit verdict")
    clock_scale = read_one(CLOCK_SCALE)
    if clock_scale["verdict"] != "delta_clock_star_candidate_frozen_but_delta_clock_and_w_time_missing":
        raise SystemExit("unexpected parent clock-scale verdict")

    low_z_rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    cc_rows = load_cc_rows()
    cc_z = [float(row["z"]) for row in cc_rows]
    cc_cells = build_cc_cells(cc_z)
    sdss_z = sorted({0.70, 0.77, 0.845})
    partial_scope = {"344", "350", "374", "375", "384", "448", "554", "595", "603", "606", "635", "701"}

    rows: list[dict[str, str]] = []
    for row in low_z_rows:
        z = float(row["zHD"])
        idx = nearest_index(z, cc_z)
        lower, upper = cc_cells[idx]
        cc_delta = abs(z - cc_z[idx])
        sdss_delta = nearest_delta(z, sdss_z)
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "assigned_cc_bin_index": str(idx),
                "assigned_cc_bin_center_z": f"{cc_z[idx]:.12g}",
                "assigned_cc_bin_lower_z": f"{lower:.12g}",
                "assigned_cc_bin_upper_z": "inf" if math.isinf(upper) else f"{upper:.12g}",
                "nearest_cc_hz_delta_z": f"{cc_delta:.12g}",
                "cc_hz_support_near_low_z": str(cc_delta <= 0.05).lower(),
                "nearest_sdss_bao_rsd_delta_z": f"{sdss_delta:.12g}",
                "sdss_bao_rsd_route_marker_near": str(sdss_delta <= 0.10).lower(),
                "partial_path_scope": str(row["source_row_index"] in partial_scope).lower(),
                "delta_clock_star_candidate": clock_scale["delta_clock_star_candidate"],
                "delta_clock_value_status": "NOT_COMPUTED_BIN_POLICY_ONLY",
                "W_time_value_status": "NOT_COMPUTED_BIN_POLICY_ONLY",
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

    used_bins = sorted({row["assigned_cc_bin_index"] for row in rows}, key=int)
    partial_rows = [row for row in rows if row["partial_path_scope"] == "true"]
    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_V1",
            "status": "TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "cc_hz_row_count": str(len(cc_rows)),
            "cc_hz_min_z": f"{min(cc_z):.12g}",
            "cc_hz_max_z": f"{max(cc_z):.12g}",
            "used_cc_bin_count": str(len(used_bins)),
            "used_cc_bin_indices": ";".join(used_bins),
            "low_z_rows_with_cc_hz_support_delta_z_le_0p05": str(
                sum(row["cc_hz_support_near_low_z"] == "true" for row in rows)
            ),
            "sdss_bao_rsd_redshift_nodes": ";".join(f"{value:.12g}" for value in sdss_z),
            "low_z_rows_with_sdss_route_marker_delta_z_le_0p10": str(
                sum(row["sdss_bao_rsd_route_marker_near"] == "true" for row in rows)
            ),
            "partial_path_scope_rows": str(len(partial_rows)),
            "partial_path_scope_cc_hz_support_delta_z_le_0p05": str(
                sum(row["cc_hz_support_near_low_z"] == "true" for row in partial_rows)
            ),
            "delta_clock_star_candidate": clock_scale["delta_clock_star_candidate"],
            "delta_clock_values_computed": "false",
            "W_time_values_computed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "redshift_bin_policy_candidate_frozen_but_delta_clock_and_w_time_missing",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_BUILT "
        f"rows={summary[0]['rows']} used_cc_bins={summary[0]['used_cc_bin_count']} "
        "w_time=false"
    )


if __name__ == "__main__":
    main()

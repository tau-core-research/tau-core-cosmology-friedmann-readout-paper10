#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_high_z_independent_clock_support_audit_policy_v1.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_high_z_independent_clock_support_audit_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_cc_rows() -> list[dict[str, str | float]]:
    rows: list[dict[str, str | float]] = []
    with CC_HZ.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            z, hz, err, reference = line.strip().split(",", 3)
            rows.append({"z": float(z), "Hz": float(hz), "errHz": float(err), "reference": reference})
    return sorted(rows, key=lambda row: float(row["z"]))


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad high-z clock support audit claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")
    target_index = policy["target_radial_index"]
    target_z = float(policy["target_z_eff"])
    cc_match_rows = read_rows(CC_MATCH)
    target_rows = [row for row in cc_match_rows if row["radial_index"] == target_index]
    if len(target_rows) != 1:
        raise SystemExit(f"target radial index {target_index} not found in CC match ledger")
    target = target_rows[0]
    if target["cc_support_status"] != "BLOCKED_OUTSIDE_CC_RANGE_NO_EXTRAPOLATION":
        raise SystemExit("high-z audit expects the target row to remain outside CC support")
    if target["cc_extrapolation_used"] != "false":
        raise SystemExit("high-z audit forbids CC extrapolation")

    cc_rows = load_cc_rows()
    z_values = [float(row["z"]) for row in cc_rows]
    z_min = min(z_values)
    z_max = max(z_values)
    nearest = min(cc_rows, key=lambda row: abs(float(row["z"]) - target_z))
    nearest_delta = abs(float(nearest["z"]) - target_z)
    bracket_available = any(z <= target_z for z in z_values) and any(z >= target_z for z in z_values)
    within_support = z_min <= target_z <= z_max
    endpoint_ready = within_support and bracket_available

    out_rows = [
        {
            "audit_id": policy["audit_id"],
            "route_id": "FROZEN_CC_TABLE",
            "route_status": "AVAILABLE_BUT_DOES_NOT_COVER_TARGET_Z",
            "target_radial_index": target_index,
            "target_z_eff": f"{target_z:.12g}",
            "cc_z_min": f"{z_min:.12g}",
            "cc_z_max": f"{z_max:.12g}",
            "nearest_clock_z": f"{float(nearest['z']):.12g}",
            "delta_z_to_nearest_clock": f"{nearest_delta:.12g}",
            "nearest_clock_reference": str(nearest["reference"]),
            "target_bracketed_without_extrapolation": "true" if bracket_available else "false",
            "target_within_clock_support_range": "true" if within_support else "false",
            "endpoint_ready_support": "true" if endpoint_ready else "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": policy["audit_id"],
            "route_id": "FUTURE_HIGH_Z_CLOCK_COMPILATION",
            "route_status": "REQUIRED_NOT_FETCHED_NOT_FROZEN",
            "target_radial_index": target_index,
            "target_z_eff": f"{target_z:.12g}",
            "cc_z_min": f"{z_min:.12g}",
            "cc_z_max": f"{z_max:.12g}",
            "nearest_clock_z": "not_available",
            "delta_z_to_nearest_clock": "not_available",
            "nearest_clock_reference": "not_available",
            "target_bracketed_without_extrapolation": "false",
            "target_within_clock_support_range": "false",
            "endpoint_ready_support": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": policy["audit_id"],
            "route_id": "FUTURE_CROSS_PROBE_TIME_SHAPE",
            "route_status": "REQUIRED_NOT_DERIVED_NOT_FROZEN",
            "target_radial_index": target_index,
            "target_z_eff": f"{target_z:.12g}",
            "cc_z_min": f"{z_min:.12g}",
            "cc_z_max": f"{z_max:.12g}",
            "nearest_clock_z": "not_available",
            "delta_z_to_nearest_clock": "not_available",
            "nearest_clock_reference": "not_available",
            "target_bracketed_without_extrapolation": "false",
            "target_within_clock_support_range": "false",
            "endpoint_ready_support": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, out_rows)

    summary = [
        {
            "audit_id": policy["audit_id"],
            "status": "DESI_HIGH_Z_INDEPENDENT_CLOCK_SUPPORT_AUDIT_BUILT_NOT_REPLAY_NOT_VALIDATION",
            "target_radial_index": target_index,
            "target_z_eff": f"{target_z:.12g}",
            "cc_table_row_count": str(len(cc_rows)),
            "cc_z_min": f"{z_min:.12g}",
            "cc_z_max": f"{z_max:.12g}",
            "nearest_frozen_clock_z": f"{float(nearest['z']):.12g}",
            "delta_z_to_nearest_frozen_clock": f"{nearest_delta:.12g}",
            "nearest_frozen_clock_reference": str(nearest["reference"]),
            "target_within_frozen_cc_support": "true" if within_support else "false",
            "target_bracketed_without_extrapolation": "true" if bracket_available else "false",
            "endpoint_ready_support_count": str(sum(1 for row in out_rows if row["endpoint_ready_support"] == "true")),
            "high_z_row_can_enter_replay": "false",
            "next_primary_source_gate": "acquire_or_freeze_independent_high_z_clock_support_near_z_2p33",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "desi_high_z_clock_support_missing_row_remains_holdout_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)


if __name__ == "__main__":
    main()

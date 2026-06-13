#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_dr2_radial_bao_cc_match_policy_v1.csv"
INTERFACE = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1.csv"
CC_HZ = ROOT / "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat"
OUT = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_dr2_radial_bao_cc_match_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
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
            rows.append(
                {
                    "z": float(z),
                    "Hz": float(hz),
                    "errHz": float(err),
                    "reference": reference,
                }
            )
    return sorted(rows, key=lambda row: float(row["z"]))


def nearest_cc_index(cc_rows: list[dict[str, float | str]], z: float) -> int:
    return min(range(len(cc_rows)), key=lambda idx: abs(float(cc_rows[idx]["z"]) - z))


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "SOURCE_SIDE_CC_MATCH_LEDGER_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad policy status")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"{field} must remain false")

    interface_rows = read_rows(INTERFACE)
    if len(interface_rows) != 6:
        raise SystemExit("DESI radial interface must contain six rows")
    cc_rows = load_cc_rows()
    z_min = min(float(row["z"]) for row in cc_rows)
    z_max = max(float(row["z"]) for row in cc_rows)

    out_rows: list[dict[str, str]] = []
    for row in interface_rows:
        z = float(row["z_eff"])
        idx = nearest_cc_index(cc_rows, z)
        cc = cc_rows[idx]
        cc_z = float(cc["z"])
        cc_hz = float(cc["Hz"])
        cc_err = float(cc["errHz"])
        within_range = z_min <= z <= z_max
        support_status = "MATCHED_WITHIN_CC_RANGE" if within_range else "BLOCKED_OUTSIDE_CC_RANGE_NO_EXTRAPOLATION"
        out_rows.append(
            {
                "match_id": policy["match_id"],
                "radial_index": row["radial_index"],
                "z_eff": row["z_eff"],
                "minus_log_DH_over_rs": row["minus_log_DH_over_rs"],
                "sigma_minus_log_DH_over_rs": row["sigma_minus_log_DH_over_rs"],
                "nearest_cc_index": str(idx),
                "nearest_cc_z": f"{cc_z:.12g}",
                "delta_z_to_nearest_cc": f"{abs(z - cc_z):.12g}",
                "nearest_cc_Hz": f"{cc_hz:.12g}",
                "nearest_cc_sigma_Hz": f"{cc_err:.12g}",
                "nearest_cc_logH": f"{math.log(cc_hz):.12g}",
                "nearest_cc_sigma_logH": f"{cc_err / cc_hz:.12g}",
                "nearest_cc_reference": str(cc["reference"]),
                "cc_support_status": support_status,
                "cc_extrapolation_used": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, out_rows)

    matched = [row for row in out_rows if row["cc_support_status"] == "MATCHED_WITHIN_CC_RANGE"]
    blocked = [row for row in out_rows if row["cc_support_status"] != "MATCHED_WITHIN_CC_RANGE"]
    matched_cc_indices = {row["nearest_cc_index"] for row in matched}
    max_delta = max(float(row["delta_z_to_nearest_cc"]) for row in matched) if matched else float("nan")
    summary = {
        "match_id": policy["match_id"],
        "status": "DESI_DR2_RADIAL_BAO_CC_MATCH_LEDGER_FROZEN_NOT_REPLAY_NOT_VALIDATION",
        "input_radial_rows": str(len(interface_rows)),
        "matched_within_cc_range_rows": str(len(matched)),
        "blocked_outside_cc_range_rows": str(len(blocked)),
        "unique_matched_cc_rows": str(len(matched_cc_indices)),
        "cc_z_min": f"{z_min:.12g}",
        "cc_z_max": f"{z_max:.12g}",
        "max_matched_delta_z_to_nearest_cc": f"{max_delta:.12g}",
        "blocked_radial_indices": ";".join(row["radial_index"] for row in blocked) or "none",
        "blocked_z_eff": ";".join(row["z_eff"] for row in blocked) or "none",
        "cc_extrapolation_used": "false",
        "control_seed_manifest_required_before_replay": "true",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "desi_bao_cc_support_partially_matched_high_z_row_blocked_no_replay",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_DESI_DR2_RADIAL_BAO_CC_MATCH_BUILT "
        f"matched={summary['matched_within_cc_range_rows']} blocked={summary['blocked_outside_cc_range_rows']} "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

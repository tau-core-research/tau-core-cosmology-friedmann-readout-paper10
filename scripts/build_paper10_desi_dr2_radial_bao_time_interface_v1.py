#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_dr2_radial_bao_time_interface_policy_v1.csv"
INVENTORY = ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1.csv"
COV = ROOT / "data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_cov.txt"
OUT = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1.csv"
COV_OUT = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_dr2_radial_bao_time_interface_not_validation"


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


def load_covariance(path: Path) -> list[list[float]]:
    rows = [
        [float(item) for item in line.split()]
        for line in path.read_text().splitlines()
        if line.strip()
    ]
    if not rows:
        raise SystemExit("empty covariance")
    if len(rows) != len(rows[0]) or any(len(row) != len(rows) for row in rows):
        raise SystemExit("covariance must be square")
    return rows


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "SOURCE_SIDE_TIME_LEVEL_INTERFACE_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad policy status")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"{field} must remain false")

    inventory = read_rows(INVENTORY)
    radial = [row for row in inventory if row["quantity"] == "DH_over_rs"]
    if len(radial) != 6:
        raise SystemExit(f"expected six DESI radial rows, got {len(radial)}")
    cov = load_covariance(COV)
    if len(cov) != len(inventory):
        raise SystemExit("inventory/covariance dimension mismatch")

    out_rows: list[dict[str, str]] = []
    for new_index, row in enumerate(radial):
        original_index = int(row["row_index"])
        value = float(row["value"])
        sigma_x = math.sqrt(cov[original_index][original_index])
        y = -math.log(value)
        sigma_y = sigma_x / value
        out_rows.append(
            {
                "interface_id": policy["interface_id"],
                "radial_index": str(new_index),
                "source_row_index": row["row_index"],
                "z_eff": row["z_eff"],
                "DH_over_rs": row["value"],
                "sigma_DH_over_rs": f"{sigma_x:.12g}",
                "minus_log_DH_over_rs": f"{y:.12g}",
                "sigma_minus_log_DH_over_rs": f"{sigma_y:.12g}",
                "time_level_interpretation": "minus_log_DH_over_rs_equals_logH_plus_beta_rd",
                "beta_rd_status": "nuisance_parameter_not_tau_signal",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    cov_rows: list[dict[str, str]] = []
    radial_indices = [int(row["row_index"]) for row in radial]
    radial_values = [float(row["value"]) for row in radial]
    for i_new, i_old in enumerate(radial_indices):
        for j_new, j_old in enumerate(radial_indices):
            transformed = cov[i_old][j_old] / (radial_values[i_new] * radial_values[j_new])
            cov_rows.append(
                {
                    "interface_id": policy["interface_id"],
                    "row_i": str(i_new),
                    "row_j": str(j_new),
                    "source_row_i": str(i_old),
                    "source_row_j": str(j_old),
                    "cov_minus_log_DH_over_rs": f"{transformed:.12g}",
                    "jacobian_rule": "C_y_ij=C_x_ij/(x_i*x_j)_for_y=-log_x",
                    "endpoint_replay_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "physical_validation_claimed": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(OUT, out_rows)
    write_csv(COV_OUT, cov_rows)

    z_values = [float(row["z_eff"]) for row in out_rows]
    variances = [float(row["sigma_minus_log_DH_over_rs"]) ** 2 for row in out_rows]
    offdiag_nonzero = sum(
        1
        for row in cov_rows
        if row["row_i"] != row["row_j"] and abs(float(row["cov_minus_log_DH_over_rs"])) > 0
    )
    summary = {
        "interface_id": policy["interface_id"],
        "status": "DESI_DR2_RADIAL_BAO_TIME_INTERFACE_FROZEN_NOT_REPLAY_NOT_VALIDATION",
        "parent_inventory": policy["parent_inventory"],
        "radial_row_count": str(len(out_rows)),
        "covariance_dimension": str(len(out_rows)),
        "z_min": f"{min(z_values):.12g}",
        "z_max": f"{max(z_values):.12g}",
        "min_sigma_minus_log_DH_over_rs": f"{math.sqrt(min(variances)):.12g}",
        "max_sigma_minus_log_DH_over_rs": f"{math.sqrt(max(variances)):.12g}",
        "offdiagonal_nonzero_covariance_entries": str(offdiag_nonzero),
        "beta_rd_nuisance_required": "true",
        "matched_cc_support_required_before_replay": "true",
        "control_seed_manifest_required_before_replay": "true",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "desi_radial_bao_time_interface_frozen_but_endpoint_replay_still_blocked",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_DESI_DR2_RADIAL_BAO_TIME_INTERFACE_BUILT "
        f"radial_rows={summary['radial_row_count']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

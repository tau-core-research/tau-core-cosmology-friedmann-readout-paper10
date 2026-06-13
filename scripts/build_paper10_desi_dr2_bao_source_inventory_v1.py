#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_dr2_bao_source_inventory_policy_v1.csv"
RAW_DIR = ROOT / "data/raw/desi_dr2_bao"
OUT = ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_dr2_bao_source_inventory_not_validation"

DOWNLOADS = {
    "desi_gaussian_bao_ALL_GCcomb_mean.txt": (
        "https://raw.githubusercontent.com/CobayaSampler/bao_data/master/"
        "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt"
    ),
    "desi_gaussian_bao_ALL_GCcomb_cov.txt": (
        "https://raw.githubusercontent.com/CobayaSampler/bao_data/master/"
        "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"
    ),
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_raw_file(name: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / name
    if not path.exists():
        path.write_bytes(urllib.request.urlopen(DOWNLOADS[name], timeout=30).read())
    return path


def parse_mean(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        z_eff, value, quantity = stripped.split()
        rows.append(
            {
                "z_eff": z_eff,
                "value": value,
                "quantity": quantity,
            }
        )
    return rows


def covariance_dimension(path: Path) -> int:
    rows = [
        [float(item) for item in line.split()]
        for line in path.read_text().splitlines()
        if line.strip()
    ]
    if not rows:
        raise SystemExit("empty covariance file")
    width = len(rows[0])
    if len(rows) != width or any(len(row) != width for row in rows):
        raise SystemExit("covariance file must be square")
    return width


def main() -> None:
    policy_rows = read_rows(POLICY)
    if len(policy_rows) != 1:
        raise SystemExit("policy must contain exactly one row")
    policy = policy_rows[0]
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")

    mean_path = ensure_raw_file(policy["mean_file"])
    cov_path = ensure_raw_file(policy["cov_file"])
    mean_rows = parse_mean(mean_path)
    cov_dim = covariance_dimension(cov_path)
    if cov_dim != len(mean_rows):
        raise SystemExit("mean/covariance dimensions disagree")

    radial_rows = [row for row in mean_rows if row["quantity"] == "DH_over_rs"]
    transverse_rows = [row for row in mean_rows if row["quantity"] == "DM_over_rs"]
    isotropic_rows = [row for row in mean_rows if row["quantity"] == "DV_over_rs"]

    inventory: list[dict[str, str]] = []
    for index, row in enumerate(mean_rows):
        inventory.append(
            {
                "inventory_id": policy["inventory_id"],
                "row_index": str(index),
                "z_eff": row["z_eff"],
                "value": row["value"],
                "quantity": row["quantity"],
                "candidate_time_level_role": "radial_DH_over_rd" if row["quantity"] == "DH_over_rs" else "supporting_nonradial_bao",
                "mean_file_sha256": sha256(mean_path),
                "cov_file_sha256": sha256(cov_path),
                "source_url": DOWNLOADS[policy["mean_file"]],
                "covariance_url": DOWNLOADS[policy["cov_file"]],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, inventory)

    summary = {
        "inventory_id": policy["inventory_id"],
        "status": "DESI_DR2_BAO_SOURCE_INVENTORY_FROZEN_NOT_REPLAY_NOT_VALIDATION",
        "source_family": policy["source_family"],
        "mean_row_count": str(len(mean_rows)),
        "covariance_dimension": str(cov_dim),
        "radial_dh_over_rd_rows": str(len(radial_rows)),
        "transverse_dm_over_rd_rows": str(len(transverse_rows)),
        "isotropic_dv_over_rd_rows": str(len(isotropic_rows)),
        "minimum_radial_rows_for_endpoint_consideration": policy["minimum_radial_rows_for_endpoint_consideration"],
        "candidate_bao_support_blocker_status": "source_frozen_but_not_integrated_into_endpoint",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "desi_dr2_public_bao_source_frozen_but_time_level_endpoint_not_replayed",
    }
    write_csv(SUMMARY, [summary])
    print(f"PAPER10_DESI_DR2_BAO_SOURCE_INVENTORY_BUILT verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PANTHEON_DATA = ROOT / "data" / "raw" / "pantheon_plus" / "pantheon_plus_mu_covariance" / "Pantheon+SH0ES.dat"
ROW_MASK = ROOT / "data" / "derived" / "pantheon_scope_v1_row_mask.csv"
PROTOCOL = ROOT / "data" / "source_manifest" / "pantheon_design_matrix_protocol_v1.csv"
OUT = ROOT / "data" / "derived" / "pantheon_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_design_matrix_v1_summary.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    protocol = read_one(PROTOCOL)
    if protocol["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("design matrix protocol must keep endpoint scoring disabled")
    with PANTHEON_DATA.open() as f:
        pantheon_rows = list(csv.DictReader(f, delimiter=" ", skipinitialspace=True))
    with ROW_MASK.open(newline="") as f:
        mask_rows = list(csv.DictReader(f))

    output_rows: list[dict[str, str]] = []
    for mask in mask_rows:
        if mask["included"] != "true":
            continue
        idx = int(mask["source_row_index"])
        row = pantheon_rows[idx]
        z_hd = float(row["zHD"])
        z_cmb = float(row["zCMB"])
        a_scale = 1.0 / (1.0 + z_hd)
        output_rows.append(
            {
                "design_id": protocol["design_id"],
                "CID": row["CID"],
                "source_row_index": str(idx),
                "zHD": row["zHD"],
                "zCMB": row["zCMB"],
                "a_scale": f"{a_scale:.12g}",
                "log1p_z": f"{math.log1p(z_hd):.12g}",
                "MU_SH0ES": row["MU_SH0ES"],
                "MU_SH0ES_ERR_DIAG": row["MU_SH0ES_ERR_DIAG"],
                "baseline_intercept_column": "1.0",
                "W_tau_basis_a_over_1pa": f"{a_scale / (1.0 + a_scale):.12g}",
                "W_tau_basis_a2_over_1pa2": f"{a_scale * a_scale / (1.0 + a_scale * a_scale):.12g}",
                "W_void_proxy_basis": f"{(a_scale * a_scale) / (a_scale * a_scale + 0.55 * 0.55):.12g}",
                "W_web_proxy_basis": f"{math.tanh((math.log1p(z_hd) - 0.45) / 0.35):.12g}",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    z_values = [float(row["zHD"]) for row in output_rows]
    summary = {
        "design_id": protocol["design_id"],
        "status": protocol["status"],
        "rows": str(len(output_rows)),
        "min_zHD": f"{min(z_values):.6g}",
        "max_zHD": f"{max(z_values):.6g}",
        "pantheon_data_sha256": sha256(PANTHEON_DATA),
        "row_mask_sha256": sha256(ROW_MASK),
        "design_matrix_sha256": sha256(OUT),
        "endpoint_scoring_allowed": "false",
        "contains_model_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_PANTHEON_DESIGN_MATRIX_V1_BUILT "
        f"rows={len(output_rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

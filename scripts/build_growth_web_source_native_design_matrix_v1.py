#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

try:
    from build_pantheon_void_web_source_native_design_matrix_v1 import load_web_profile, nearest_lookup
except ImportError:
    from scripts.build_pantheon_void_web_source_native_design_matrix_v1 import load_web_profile, nearest_lookup


ROOT = Path(__file__).resolve().parents[1]
GROWTH = ROOT / "data" / "source_manifest" / "sdss_final_bao_rsd_growth_summary_v1.csv"
TRANSFORM = ROOT / "data" / "source_manifest" / "growth_web_source_native_transform_rule_v1.csv"
OUT = ROOT / "data" / "derived" / "growth_web_source_native_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "growth_web_source_native_design_matrix_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    transform = read_one(TRANSFORM)
    if transform["endpoint_scoring_allowed"] != "false":
        raise SystemExit("growth web transform must remain endpoint disabled")
    web_centers, web_values, web_stats = load_web_profile()
    with GROWTH.open(newline="") as f:
        growth_rows = list(csv.DictReader(f))

    output_rows: list[dict[str, str]] = []
    for row in growth_rows:
        z = float(row["z_eff"])
        output_rows.append(
            {
                "transform_id": transform["transform_id"],
                "growth_product_id": row["growth_product_id"],
                "sample": row["sample"],
                "z_eff": row["z_eff"],
                "fsigma8": row["fsigma8"],
                "fsigma8_sigma": row["fsigma8_sigma"],
                "W_web_source_native_basis": f"{nearest_lookup(z, web_centers, web_values):.12g}",
                "endpoint_scoring_allowed": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    nonzero = sum(float(row["W_web_source_native_basis"]) > 0 for row in output_rows)
    summary = {
        "transform_id": transform["transform_id"],
        "status": transform["status"],
        "rows": str(len(output_rows)),
        "web_nonzero_rows": str(nonzero),
        "web_rows_total": str(int(web_stats["web_rows_total"])),
        "web_rows_usable": str(int(web_stats["web_rows_usable"])),
        "web_bins": str(int(web_stats["web_bins"])),
        "endpoint_scoring_allowed": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_GROWTH_WEB_SOURCE_NATIVE_DESIGN_MATRIX_V1_BUILT "
        f"rows={len(output_rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

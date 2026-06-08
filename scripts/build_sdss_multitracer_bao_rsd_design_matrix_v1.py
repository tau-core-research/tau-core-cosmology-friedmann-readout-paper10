#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

try:
    from build_pantheon_void_web_source_native_design_matrix_v1 import load_web_profile, nearest_lookup, read_one
except ImportError:
    from scripts.build_pantheon_void_web_source_native_design_matrix_v1 import load_web_profile, nearest_lookup, read_one


ROOT = Path(__file__).resolve().parents[1]
TRANSFORM = ROOT / "data" / "source_manifest" / "sdss_multitracer_bao_rsd_transform_rule_v1.csv"
PRODUCTS = ROOT / "data" / "source_manifest" / "sdss_multitracer_bao_rsd_products_v1.csv"
OUT = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_design_matrix_v1_summary.csv"


def parse_measurement(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for idx, line in enumerate(path.read_text().splitlines()):
        if not line.strip() or line.strip().startswith("#"):
            continue
        values = line.split("#", 1)[0].split()
        comment = line.split("#", 1)[1].strip() if "#" in line else ""
        if len(values) < 3:
            raise SystemExit(f"cannot parse SDSS measurement line: {line}")
        z_eff = float(values[0])
        value = float(values[1])
        sigma = float(values[2])
        if "DM_ov_rd" in comment:
            observable = "DM_over_rd"
        elif "DH_ov_rd" in comment:
            observable = "DH_over_rd"
        elif "f\\sigma_8" in comment or "f" in comment and "sigma" in comment:
            observable = "fsigma8"
        else:
            raise SystemExit(f"cannot infer observable from comment: {comment}")
        rows.append(
            {
                "vector_index": str(idx),
                "z_eff": f"{z_eff:.12g}",
                "observable": observable,
                "observed_value": f"{value:.12g}",
                "published_sigma": f"{sigma:.12g}",
                "published_comment": comment,
            }
        )
    return rows


def main() -> None:
    transform = read_one(TRANSFORM)
    if transform["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("SDSS multitracer transform must remain endpoint disabled")
    with PRODUCTS.open(newline="") as f:
        product_rows = list(csv.DictReader(f))
    pk_rows = [row for row in product_rows if row["measurement_space"] == "fourier_space"]
    if len(pk_rows) != 1:
        raise SystemExit("expected exactly one Fourier-space SDSS multitracer product")
    product = pk_rows[0]
    data_path = ROOT / product["data_path"]
    cov_path = ROOT / product["covariance_path"]
    rows = parse_measurement(data_path)
    cov = np.loadtxt(cov_path)
    if cov.shape != (len(rows), len(rows)):
        raise SystemExit(f"covariance shape {cov.shape} does not match vector length {len(rows)}")
    eig = np.linalg.eigvalsh(cov)
    if float(eig[0]) <= 0:
        raise SystemExit("SDSS multitracer covariance is not positive definite")
    web_centers, web_values, web_stats = load_web_profile()
    out_rows: list[dict[str, str]] = []
    for row in rows:
        z = float(row["z_eff"])
        out_rows.append(
            {
                **row,
                "transform_id": transform["transform_id"],
                "measurement_space": "fourier_space",
                "covariance_path": product["covariance_path"],
                "W_web_source_native_basis": f"{nearest_lookup(z, web_centers, web_values):.12g}",
                "W_web_applies_to_observable": "true" if row["observable"] == "fsigma8" else "false",
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)
    summary = {
        "transform_id": transform["transform_id"],
        "status": transform["status"],
        "rows": str(len(out_rows)),
        "n_redshift_bins": str(len({row["z_eff"] for row in out_rows})),
        "covariance_shape": f"{cov.shape[0]}x{cov.shape[1]}",
        "covariance_min_eigenvalue": f"{float(eig[0]):.12g}",
        "covariance_condition_number": f"{float(eig[-1] / eig[0]):.12g}",
        "web_rows_total": str(int(web_stats["web_rows_total"])),
        "web_rows_usable": str(int(web_stats["web_rows_usable"])),
        "web_bins": str(int(web_stats["web_bins"])),
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
        "PAPER10_SDSS_MULTITRACER_BAO_RSD_DESIGN_MATRIX_V1_BUILT "
        f"rows={len(out_rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

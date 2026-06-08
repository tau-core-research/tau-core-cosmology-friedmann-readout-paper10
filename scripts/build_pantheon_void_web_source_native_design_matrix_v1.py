#!/usr/bin/env python3
from __future__ import annotations

import bisect
import csv
import math
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PANTHEON = ROOT / "data" / "derived" / "pantheon_design_matrix_v1.csv"
TRANSFORM = ROOT / "data" / "source_manifest" / "void_web_source_native_transform_rule_v1.csv"
VOID_TABLE = (
    ROOT
    / "data"
    / "raw"
    / "public_void_catalog"
    / "vast_dr7_planck2018"
    / "VoidFinder-nsa_v1_0_1_Planck2018_comoving_maximal.txt"
)
WEB_FITS = ROOT / "data" / "raw" / "cosmic_web" / "sdss_dr17_mcpm" / "slimeMold_galaxy_catalog_v1_0_1.fits"
OUT = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1_summary.csv"

D_H_MPC_OVER_H = 2997.92458
R_BIN_WIDTH = 10.0
Z_BIN_WIDTH = 0.02


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def quantile(values: list[float], q: float) -> float:
    if not values:
        raise SystemExit("cannot quantile empty list")
    sorted_values = sorted(values)
    idx = q * (len(sorted_values) - 1)
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return sorted_values[lo]
    frac = idx - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def median(values: list[float]) -> float:
    return quantile(values, 0.5)


def clip01(value: float) -> float:
    return min(1.0, max(0.0, value))


def load_void_profile() -> tuple[list[float], list[float], dict[str, float]]:
    rows: list[tuple[float, float]] = []
    with VOID_TABLE.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split()
            r = float(parts[6])
            reff = float(parts[9])
            if math.isfinite(r) and math.isfinite(reff) and r > 0 and reff > 0:
                rows.append((r, reff**3))
    if not rows:
        raise SystemExit("void table has no usable rows")
    max_r = max(r for r, _ in rows)
    n_bins = int(math.ceil(max_r / R_BIN_WIDTH)) + 1
    bin_load = [0.0 for _ in range(n_bins)]
    for r, volume in rows:
        idx = min(n_bins - 1, int(r // R_BIN_WIDTH))
        bin_load[idx] += volume
    total = sum(bin_load)
    cumulative = 0.0
    bin_centers: list[float] = []
    w_values: list[float] = []
    for idx, value in enumerate(bin_load):
        cumulative += value
        bin_centers.append((idx + 0.5) * R_BIN_WIDTH)
        w_values.append(cumulative / total if total > 0 else 0.0)
    stats = {
        "void_rows": float(len(rows)),
        "void_min_r": min(r for r, _ in rows),
        "void_max_r": max_r,
        "void_total_reff3": total,
    }
    return bin_centers, w_values, stats


def read_fits_bintable_header(path: Path) -> tuple[int, int, int]:
    with path.open("rb") as f:
        while True:
            header = b""
            while True:
                block = f.read(2880)
                if not block:
                    raise SystemExit(f"no BINTABLE extension found in {path}")
                header += block
                if b"END" in block:
                    break
            cards = [header[i : i + 80].decode("ascii", "ignore") for i in range(0, len(header), 80)]
            values: dict[str, str] = {}
            for card in cards:
                key = card[:8].strip()
                if key and card[8:10] == "= ":
                    values[key] = card[10:30].split("/")[0].strip().strip("'")
            if values.get("XTENSION") == "BINTABLE":
                return f.tell(), int(values["NAXIS1"]), int(values["NAXIS2"])
            f.seek(0, 1)


def load_web_profile() -> tuple[list[float], list[float], dict[str, float]]:
    offset, row_bytes, n_rows = read_fits_bintable_header(WEB_FITS)
    bins: dict[int, list[float]] = {}
    usable = 0
    with WEB_FITS.open("rb") as f:
        f.seek(offset)
        for _ in range(n_rows):
            row = f.read(row_bytes)
            if len(row) != row_bytes:
                break
            z = struct.unpack(">f", row[37:41])[0]
            density = struct.unpack(">f", row[58:62])[0]
            if not (math.isfinite(z) and math.isfinite(density)):
                continue
            if not (0.0 < z < 3.0 and density > -90.0):
                continue
            idx = int(z // Z_BIN_WIDTH)
            bins.setdefault(idx, []).append(density)
            usable += 1
    if not bins:
        raise SystemExit("web table has no usable rows")
    medians = {idx: median(values) for idx, values in bins.items()}
    q10 = quantile(list(medians.values()), 0.1)
    q90 = quantile(list(medians.values()), 0.9)
    denom = q90 - q10
    if denom <= 0:
        raise SystemExit("web density normalization collapsed")
    bin_centers = sorted((idx + 0.5) * Z_BIN_WIDTH for idx in medians)
    w_values = [clip01((medians[int(center // Z_BIN_WIDTH)] - q10) / denom) for center in bin_centers]
    stats = {
        "web_rows_total": float(n_rows),
        "web_rows_usable": float(usable),
        "web_bins": float(len(bins)),
        "web_density_q10": q10,
        "web_density_q90": q90,
    }
    return bin_centers, w_values, stats


def nearest_lookup(x: float, centers: list[float], values: list[float], outside_zero: bool = True) -> float:
    if outside_zero and (x < centers[0] or x > centers[-1]):
        return 0.0
    idx = bisect.bisect_left(centers, x)
    if idx <= 0:
        return values[0]
    if idx >= len(centers):
        return values[-1]
    before = centers[idx - 1]
    after = centers[idx]
    return values[idx - 1] if abs(x - before) <= abs(x - after) else values[idx]


def main() -> None:
    transform = read_one(TRANSFORM)
    if transform["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("source-native transform must remain endpoint disabled")

    void_centers, void_values, void_stats = load_void_profile()
    web_centers, web_values, web_stats = load_web_profile()

    with PANTHEON.open(newline="") as f:
        pantheon_rows = list(csv.DictReader(f))

    output_rows: list[dict[str, str]] = []
    for row in pantheon_rows:
        z = float(row["zHD"])
        r_proxy = D_H_MPC_OVER_H * z
        output_rows.append(
            {
                **row,
                "source_native_transform_id": transform["transform_id"],
                "r_pantheon_lowz_mpc_over_h": f"{r_proxy:.12g}",
                "W_void_source_native_basis": f"{nearest_lookup(r_proxy, void_centers, void_values):.12g}",
                "W_web_source_native_basis": f"{nearest_lookup(z, web_centers, web_values):.12g}",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    void_nonzero = sum(float(row["W_void_source_native_basis"]) > 0 for row in output_rows)
    web_nonzero = sum(float(row["W_web_source_native_basis"]) > 0 for row in output_rows)
    summary = {
        "transform_id": transform["transform_id"],
        "status": transform["status"],
        "rows": str(len(output_rows)),
        "void_nonzero_rows": str(void_nonzero),
        "web_nonzero_rows": str(web_nonzero),
        "void_rows": str(int(void_stats["void_rows"])),
        "void_min_r": f"{void_stats['void_min_r']:.12g}",
        "void_max_r": f"{void_stats['void_max_r']:.12g}",
        "web_rows_total": str(int(web_stats["web_rows_total"])),
        "web_rows_usable": str(int(web_stats["web_rows_usable"])),
        "web_bins": str(int(web_stats["web_bins"])),
        "web_density_q10": f"{web_stats['web_density_q10']:.12g}",
        "web_density_q90": f"{web_stats['web_density_q90']:.12g}",
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
        "PAPER10_PANTHEON_VOID_WEB_SOURCE_NATIVE_DESIGN_MATRIX_V1_BUILT "
        f"rows={len(output_rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

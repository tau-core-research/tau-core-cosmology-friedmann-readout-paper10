#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_directional_web_anisotropy_policy_v1.csv"
PANTHEON_RAW = ROOT / "data/raw/pantheon_plus/pantheon_plus_mu_covariance/Pantheon+SH0ES.dat"
LOW_Z_MASK = ROOT / "data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
WEB_FITS = ROOT / "data/raw/cosmic_web/sdss_dr17_mcpm/slimeMold_galaxy_catalog_v1_0_1.fits"
OUT = ROOT / "data/derived/low_z_pantheon_directional_web_anisotropy_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_directional_web_anisotropy_v1_summary.csv"
CLAIM_BOUNDARY = "directional_web_anisotropy_source_side_not_scoring_not_validation"


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


def load_pantheon_raw_by_source_index() -> dict[int, dict[str, str]]:
    with PANTHEON_RAW.open() as f:
        header = f.readline().split()
        rows = [dict(zip(header, line.split())) for line in f if line.strip()]
    return {idx: row for idx, row in enumerate(rows)}


def valid_ra_dec(ra: float, dec: float) -> bool:
    return math.isfinite(ra) and math.isfinite(dec) and 0.0 <= ra <= 360.0 and -90.0 <= dec <= 90.0


def angular_sep_deg(ra1: float, dec1: float, ra2: np.ndarray, dec2: np.ndarray) -> np.ndarray:
    ra1r = math.radians(ra1)
    dec1r = math.radians(dec1)
    ra2r = np.deg2rad(ra2)
    dec2r = np.deg2rad(dec2)
    sin_ddec = np.sin((dec2r - dec1r) / 2.0)
    sin_dra = np.sin((ra2r - ra1r) / 2.0)
    a = sin_ddec * sin_ddec + math.cos(dec1r) * np.cos(dec2r) * sin_dra * sin_dra
    return np.rad2deg(2.0 * np.arcsin(np.minimum(1.0, np.sqrt(np.maximum(0.0, a)))))


def tangent_offsets_rad(ra0: float, dec0: float, ra: np.ndarray, dec: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    dra = (ra - ra0 + 180.0) % 360.0 - 180.0
    dx = np.deg2rad(dra) * math.cos(math.radians(dec0))
    dy = np.deg2rad(dec - dec0)
    return dx, dy


def parse_window(spec: str) -> tuple[float, float]:
    lo, hi = spec.split(":")
    return float(lo), float(hi)


def fmt(value: float) -> str:
    return "" if math.isnan(value) else f"{value:.12g}"


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    if values.size == 0 or weights.size == 0:
        return math.nan
    total = float(np.sum(weights))
    if total <= 0.0:
        return math.nan
    return float(np.sum(weights * values) / total)


def moment_observables(dx: np.ndarray, dy: np.ndarray, density: np.ndarray) -> dict[str, float]:
    if dx.size == 0:
        return {
            "web_density_mean": math.nan,
            "web_density_median": math.nan,
            "web_dipole_amplitude_rad": math.nan,
            "web_quadrupole_q": math.nan,
            "web_quadrupole_angle_rad": math.nan,
            "web_quadrupole_xx_minus_yy": math.nan,
            "web_quadrupole_xy2": math.nan,
        }
    weights = np.maximum(density, 0.0)
    if float(np.sum(weights)) <= 0.0:
        weights = np.ones_like(density)
    mx = weighted_mean(dx, weights)
    my = weighted_mean(dy, weights)
    centered_x = dx - mx
    centered_y = dy - my
    mxx = weighted_mean(centered_x * centered_x, weights)
    myy = weighted_mean(centered_y * centered_y, weights)
    mxy = weighted_mean(centered_x * centered_y, weights)
    trace = mxx + myy
    qx = mxx - myy
    qy = 2.0 * mxy
    quad = math.sqrt(qx * qx + qy * qy) / trace if trace > 0.0 else math.nan
    angle = 0.5 * math.atan2(qy, qx) if trace > 0.0 else math.nan
    return {
        "web_density_mean": float(np.mean(density)),
        "web_density_median": float(np.median(density)),
        "web_dipole_amplitude_rad": math.sqrt(mx * mx + my * my),
        "web_quadrupole_q": quad,
        "web_quadrupole_angle_rad": angle,
        "web_quadrupole_xx_minus_yy": qx,
        "web_quadrupole_xy2": qy,
    }


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "DIRECTIONAL_WEB_ANISOTROPY_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("directional web policy must not authorize replay or validation")
    radius = float(policy["angular_radius_deg"])
    zlo_offset, zhi_offset = parse_window(policy["redshift_window"])
    pantheon = load_pantheon_raw_by_source_index()
    low_z_rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    with fits.open(WEB_FITS) as hdul:
        data = hdul[1].data
        gra = np.asarray(data["ra"], dtype=float)
        gdec = np.asarray(data["dec"], dtype=float)
        gz = np.asarray(data["z"], dtype=float)
        gdens = np.asarray(data["matterDens"], dtype=float)
    usable = (
        np.isfinite(gra)
        & np.isfinite(gdec)
        & np.isfinite(gz)
        & np.isfinite(gdens)
        & (gz > 0)
        & (gz < 3)
        & (gdens > -90)
    )
    gra, gdec, gz, gdens = gra[usable], gdec[usable], gz[usable], gdens[usable]
    rows: list[dict[str, str]] = []
    for lowz in low_z_rows:
        raw = pantheon[int(lowz["source_row_index"])]
        host_ra = float(raw.get("HOST_RA", "-999"))
        host_dec = float(raw.get("HOST_DEC", "-999"))
        if valid_ra_dec(host_ra, host_dec):
            ra, dec, coord_source = host_ra, host_dec, "HOST_RA_DEC"
        else:
            ra, dec, coord_source = float(raw["RA"]), float(raw["DEC"]), "SN_RA_DEC_FALLBACK"
        if not valid_ra_dec(ra, dec):
            raise SystemExit(f"invalid sky coordinate for {lowz['CID']}")
        z = float(lowz["zHD"])
        zmask = (gz >= z + zlo_offset) & (gz <= z + zhi_offset)
        sep = angular_sep_deg(ra, dec, gra[zmask], gdec[zmask]) if np.any(zmask) else np.array([], dtype=float)
        cone = sep <= radius
        cone_ra = gra[zmask][cone] if np.any(zmask) else np.array([], dtype=float)
        cone_dec = gdec[zmask][cone] if np.any(zmask) else np.array([], dtype=float)
        cone_z = gz[zmask][cone] if np.any(zmask) else np.array([], dtype=float)
        cone_density = gdens[zmask][cone] if np.any(zmask) else np.array([], dtype=float)
        dx, dy = tangent_offsets_rad(ra, dec, cone_ra, cone_dec) if cone_ra.size else (np.array([]), np.array([]))
        moments = moment_observables(dx, dy, cone_density)
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_DIRECTIONAL_WEB_ANISOTROPY_V1",
                "CID": lowz["CID"],
                "source_row_index": lowz["source_row_index"],
                "zHD": lowz["zHD"],
                "coordinate_source": coord_source,
                "ra_deg": f"{ra:.12g}",
                "dec_deg": f"{dec:.12g}",
                "angular_radius_deg": f"{radius:.12g}",
                "redshift_window": policy["redshift_window"],
                "web_cone_count": str(int(cone_density.size)),
                "web_z_mean": fmt(float(np.mean(cone_z)) if cone_z.size else math.nan),
                "web_density_mean": fmt(moments["web_density_mean"]),
                "web_density_median": fmt(moments["web_density_median"]),
                "web_dipole_amplitude_rad": fmt(moments["web_dipole_amplitude_rad"]),
                "web_quadrupole_q": fmt(moments["web_quadrupole_q"]),
                "web_quadrupole_angle_rad": fmt(moments["web_quadrupole_angle_rad"]),
                "web_quadrupole_xx_minus_yy": fmt(moments["web_quadrupole_xx_minus_yy"]),
                "web_quadrupole_xy2": fmt(moments["web_quadrupole_xy2"]),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)
    partial_scope = {"344", "350", "374", "375", "384", "448", "554", "595", "603", "606", "635", "701"}
    partial_rows = [row for row in rows if row["source_row_index"] in partial_scope]
    nonempty = [row for row in rows if int(row["web_cone_count"]) > 0]
    quadrupole_ready = [row for row in rows if int(row["web_cone_count"]) >= 3 and row["web_quadrupole_q"]]
    partial_nonempty = [row for row in partial_rows if int(row["web_cone_count"]) > 0]
    partial_quadrupole = [row for row in partial_rows if int(row["web_cone_count"]) >= 3 and row["web_quadrupole_q"]]
    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_DIRECTIONAL_WEB_ANISOTROPY_V1",
            "status": "DIRECTIONAL_WEB_ANISOTROPY_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "nonempty_web_cone_rows": str(len(nonempty)),
            "quadrupole_ready_rows": str(len(quadrupole_ready)),
            "partial_path_scope_rows": str(len(partial_rows)),
            "partial_path_scope_nonempty_web_cone_rows": str(len(partial_nonempty)),
            "partial_path_scope_quadrupole_ready_rows": str(len(partial_quadrupole)),
            "angular_radius_deg": f"{radius:.12g}",
            "redshift_window": policy["redshift_window"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "directional_web_anisotropy_available_as_partial_source_observable_not_full_path_tensor",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_DIRECTIONAL_WEB_ANISOTROPY_BUILT "
        f"rows={summary[0]['rows']} quadrupole_ready={summary[0]['quadrupole_ready_rows']} "
        f"partial_ready={summary[0]['partial_path_scope_quadrupole_ready_rows']}"
    )


if __name__ == "__main__":
    main()

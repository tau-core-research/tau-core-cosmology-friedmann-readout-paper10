#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_los_radial_profile_policy_v1.csv"
PANTHEON_RAW = ROOT / "data/raw/pantheon_plus/pantheon_plus_mu_covariance/Pantheon+SH0ES.dat"
LOW_Z_MASK = ROOT / "data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
WEB_FITS = ROOT / "data/raw/cosmic_web/sdss_dr17_mcpm/slimeMold_galaxy_catalog_v1_0_1.fits"
OUT = ROOT / "data/derived/low_z_pantheon_los_radial_profile_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_los_radial_profile_v1_summary.csv"
CLAIM_BOUNDARY = "los_radial_profile_source_side_not_scoring_not_validation"


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


def angular_sep_deg(ra1: float, dec1: float, ra2: np.ndarray, dec2: np.ndarray) -> np.ndarray:
    ra1r = math.radians(ra1)
    dec1r = math.radians(dec1)
    ra2r = np.deg2rad(ra2)
    dec2r = np.deg2rad(dec2)
    sin_ddec = np.sin((dec2r - dec1r) / 2.0)
    sin_dra = np.sin((ra2r - ra1r) / 2.0)
    a = sin_ddec * sin_ddec + math.cos(dec1r) * np.cos(dec2r) * sin_dra * sin_dra
    return np.rad2deg(2.0 * np.arcsin(np.minimum(1.0, np.sqrt(np.maximum(0.0, a)))))


def parse_shells(spec: str) -> list[tuple[str, float, float]]:
    shells: list[tuple[str, float, float]] = []
    for item in spec.split(";"):
        name, lo, hi = item.split(":")
        shells.append((name, float(lo), float(hi)))
    if not shells:
        raise SystemExit("no shells declared")
    return shells


def finite_mean(values: np.ndarray) -> float:
    if values.size == 0:
        return math.nan
    return float(np.mean(values))


def finite_median(values: np.ndarray) -> float:
    if values.size == 0:
        return math.nan
    return float(np.median(values))


def fmt(value: float) -> str:
    return "" if math.isnan(value) else f"{value:.12g}"


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "LOS_RADIAL_PROFILE_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("LOS radial profile policy must not authorize replay or validation")
    shells = parse_shells(policy["redshift_shells"])
    radius = float(policy["angular_radius_deg"])
    pantheon_by_idx = load_pantheon_raw_by_source_index()
    low_z_rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    with fits.open(WEB_FITS) as hdul:
        data = hdul[1].data
        gra = np.asarray(data["ra"], dtype=float)
        gdec = np.asarray(data["dec"], dtype=float)
        gz = np.asarray(data["z"], dtype=float)
        gdens = np.asarray(data["matterDens"], dtype=float)
    usable = np.isfinite(gra) & np.isfinite(gdec) & np.isfinite(gz) & np.isfinite(gdens) & (gz > 0) & (gz < 3) & (gdens > -90)
    gra, gdec, gz, gdens = gra[usable], gdec[usable], gz[usable], gdens[usable]
    rows: list[dict[str, str]] = []
    for lowz in low_z_rows:
        raw = pantheon_by_idx[int(lowz["source_row_index"])]
        host_ra = float(raw.get("HOST_RA", "-999"))
        host_dec = float(raw.get("HOST_DEC", "-999"))
        if host_ra != -999 and host_dec != -999:
            ra, dec, coord_source = host_ra, host_dec, "HOST_RA_DEC"
        else:
            ra, dec, coord_source = float(raw["RA"]), float(raw["DEC"]), "SN_RA_DEC_FALLBACK"
        z = float(lowz["zHD"])
        zlo = z + min(lo for _, lo, _ in shells)
        zhi = z + max(hi for _, _, hi in shells)
        zmask = (gz >= zlo) & (gz <= zhi)
        sep_all = angular_sep_deg(ra, dec, gra[zmask], gdec[zmask]) if np.any(zmask) else np.array([], dtype=float)
        dz_all = gz[zmask] - z if np.any(zmask) else np.array([], dtype=float)
        dens_all = gdens[zmask] if np.any(zmask) else np.array([], dtype=float)
        cone = sep_all <= radius
        dz_cone = dz_all[cone]
        dens_cone = dens_all[cone]
        out: dict[str, str] = {
            "artifact_id": "LOW_Z_PANTHEON_LOS_RADIAL_PROFILE_V1",
            "CID": lowz["CID"],
            "source_row_index": lowz["source_row_index"],
            "zHD": lowz["zHD"],
            "coordinate_source": coord_source,
            "ra_deg": f"{ra:.12g}",
            "dec_deg": f"{dec:.12g}",
            "angular_radius_deg": f"{radius:.12g}",
            "total_shell_count": str(int(dens_cone.size)),
        }
        counts: list[int] = []
        means: list[float] = []
        for name, lo, hi in shells:
            mask = (dz_cone >= lo) & (dz_cone < hi)
            dens = dens_cone[mask]
            counts.append(int(dens.size))
            means.append(finite_mean(dens))
            out[f"{name}_dz_min"] = f"{lo:.12g}"
            out[f"{name}_dz_max"] = f"{hi:.12g}"
            out[f"{name}_count"] = str(int(dens.size))
            out[f"{name}_density_mean"] = fmt(finite_mean(dens))
            out[f"{name}_density_median"] = fmt(finite_median(dens))
        foreground = [value for name, value in zip([s[0] for s in shells], means) if name.startswith("foreground") and not math.isnan(value)]
        background = [value for name, value in zip([s[0] for s in shells], means) if name.startswith("background") and not math.isnan(value)]
        near = [value for name, value in zip([s[0] for s in shells], means) if name == "near_source" and not math.isnan(value)]
        fg_mean = float(np.mean(foreground)) if foreground else math.nan
        bg_mean = float(np.mean(background)) if background else math.nan
        near_mean = float(np.mean(near)) if near else math.nan
        out["foreground_density_mean"] = fmt(fg_mean)
        out["background_density_mean"] = fmt(bg_mean)
        out["near_source_density_mean"] = fmt(near_mean)
        out["foreground_minus_background_density"] = fmt(fg_mean - bg_mean if not math.isnan(fg_mean) and not math.isnan(bg_mean) else math.nan)
        out["near_minus_far_density"] = fmt(near_mean - 0.5 * (fg_mean + bg_mean) if not math.isnan(near_mean) and not math.isnan(fg_mean) and not math.isnan(bg_mean) else math.nan)
        out["profile_nonempty_shell_count"] = str(sum(count > 0 for count in counts))
        out["endpoint_replay_allowed"] = "false"
        out["endpoint_validation_claimed"] = "false"
        out["contains_endpoint_scores"] = "false"
        out["contains_distance_residuals"] = "false"
        out["contains_fit_statistics"] = "false"
        out["physical_lensing_path_weight_claimed"] = "false"
        out["claim_boundary"] = CLAIM_BOUNDARY
        rows.append(out)
    write_csv(OUT, rows)
    nonempty_any = sum(int(row["total_shell_count"]) > 0 for row in rows)
    complete = sum(int(row["profile_nonempty_shell_count"]) == len(shells) for row in rows)
    partial_scope = {"344", "350", "374", "375", "384", "448", "554", "595", "603", "606", "635", "701"}
    partial_rows = [row for row in rows if row["source_row_index"] in partial_scope]
    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_LOS_RADIAL_PROFILE_V1",
            "status": "LOS_RADIAL_PROFILE_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "shell_count": str(len(shells)),
            "nonempty_any_shell_rows": str(nonempty_any),
            "complete_profile_rows": str(complete),
            "partial_path_scope_rows": str(len(partial_rows)),
            "partial_path_scope_nonempty_any_shell_rows": str(sum(int(row["total_shell_count"]) > 0 for row in partial_rows)),
            "partial_path_scope_complete_profile_rows": str(sum(int(row["profile_nonempty_shell_count"]) == len(shells) for row in partial_rows)),
            "angular_radius_deg": f"{radius:.12g}",
            "redshift_shells": policy["redshift_shells"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "los_radial_profile_available_as_partial_source_observable_not_full_path_integral",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_LOS_RADIAL_PROFILE_BUILT "
        f"rows={summary[0]['rows']} complete={summary[0]['complete_profile_rows']} "
        f"partial_complete={summary[0]['partial_path_scope_complete_profile_rows']}"
    )


if __name__ == "__main__":
    main()

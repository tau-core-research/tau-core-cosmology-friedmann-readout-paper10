#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from astropy.io import fits

ROOT = Path(__file__).resolve().parents[1]
ACQUISITION = ROOT / "data" / "derived" / "void_source_basis_refinement_acquisition_manifest_v1.csv"
ACQ_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_acquisition_manifest_v1_summary.csv"
VOID_TABLE = ROOT / "data" / "raw" / "public_void_catalog" / "vast_dr7_planck2018" / "VoidFinder-nsa_v1_0_1_Planck2018_comoving_maximal.txt"
VOID_INVENTORY = ROOT / "data" / "derived" / "void_web_source_native_inventory_v1.csv"
PANTHEON_RAW = ROOT / "data" / "raw" / "pantheon_plus" / "pantheon_plus_mu_covariance" / "Pantheon+SH0ES.dat"
LOW_Z_MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
WEB_FITS = ROOT / "data" / "raw" / "cosmic_web" / "sdss_dr17_mcpm" / "slimeMold_galaxy_catalog_v1_0_1.fits"
OUT_ATTACH = ROOT / "data" / "derived" / "void_source_basis_refinement_r1_r3_source_attachment_v1.csv"
OUT_GEOM = ROOT / "data" / "derived" / "low_z_pantheon_void_geometry_join_v1.csv"
OUT_ENV = ROOT / "data" / "derived" / "low_z_pantheon_los_environment_v1.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r1_r3_source_attachment_v1_summary.csv"

D_H_MPC_OVER_H = 2997.92458
LOS_DZ_WINDOW = 0.01
LOS_ANGULAR_RADIUS_DEG = 2.0


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


def load_voids() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with VOID_TABLE.open() as f:
        header = None
        for line in f:
            if not line.strip():
                continue
            if line.startswith("#"):
                header = line[1:].split()
                continue
            parts = line.split()
            if header is None or len(parts) < len(header):
                raise SystemExit("void table header/row mismatch")
            data = {key: float(value) for key, value in zip(header, parts)}
            rows.append(data)
    if not rows:
        raise SystemExit("void table has no rows")
    return rows


def load_pantheon_raw_by_source_index() -> dict[int, dict[str, str]]:
    with PANTHEON_RAW.open() as f:
        header = f.readline().split()
        rows = [dict(zip(header, line.split())) for line in f if line.strip()]
    return {idx: row for idx, row in enumerate(rows)}


def spherical_to_cartesian(ra_deg: float, dec_deg: float, radius: float) -> tuple[float, float, float]:
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    cdec = math.cos(dec)
    return (
        radius * cdec * math.cos(ra),
        radius * cdec * math.sin(ra),
        radius * math.sin(dec),
    )


def angular_sep_deg(ra1: float, dec1: float, ra2: np.ndarray, dec2: np.ndarray) -> np.ndarray:
    ra1r = math.radians(ra1)
    dec1r = math.radians(dec1)
    ra2r = np.deg2rad(ra2)
    dec2r = np.deg2rad(dec2)
    sin_ddec = np.sin((dec2r - dec1r) / 2.0)
    sin_dra = np.sin((ra2r - ra1r) / 2.0)
    a = sin_ddec * sin_ddec + math.cos(dec1r) * np.cos(dec2r) * sin_dra * sin_dra
    return np.rad2deg(2.0 * np.arcsin(np.minimum(1.0, np.sqrt(np.maximum(0.0, a)))))


def build_geometry(low_z_rows: list[dict[str, str]], pantheon_by_idx: dict[int, dict[str, str]], voids: list[dict[str, float]]) -> list[dict[str, str]]:
    vx = np.array([v["x"] for v in voids])
    vy = np.array([v["y"] for v in voids])
    vz = np.array([v["z"] for v in voids])
    vra = np.array([v["ra"] for v in voids])
    vdec = np.array([v["dec"] for v in voids])
    vreff = np.array([v["Reff"] for v in voids])
    vradius = np.array([v["radius"] for v in voids])
    vvoid = np.array([v["void"] for v in voids])
    out: list[dict[str, str]] = []
    for row in low_z_rows:
        raw = pantheon_by_idx[int(row["source_row_index"])]
        host_ra = float(raw.get("HOST_RA", "-999"))
        host_dec = float(raw.get("HOST_DEC", "-999"))
        if host_ra != -999 and host_dec != -999:
            ra, dec, coord_source = host_ra, host_dec, "HOST_RA_DEC"
        else:
            ra, dec, coord_source = float(raw["RA"]), float(raw["DEC"]), "SN_RA_DEC_FALLBACK"
        z = float(row["zHD"])
        radius = D_H_MPC_OVER_H * z
        sx, sy, sz = spherical_to_cartesian(ra, dec, radius)
        dist = np.sqrt((vx - sx) ** 2 + (vy - sy) ** 2 + (vz - sz) ** 2)
        idx = int(np.argmin(dist))
        wall = float(dist[idx] - vreff[idx])
        out.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_VOID_GEOMETRY_JOIN_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "coordinate_source": coord_source,
                "ra_deg": f"{ra:.12g}",
                "dec_deg": f"{dec:.12g}",
                "sn_radius_proxy_mpc_over_h": f"{radius:.12g}",
                "sn_x_mpc_over_h": f"{sx:.12g}",
                "sn_y_mpc_over_h": f"{sy:.12g}",
                "sn_z_mpc_over_h": f"{sz:.12g}",
                "nearest_void_row_index": str(idx),
                "nearest_void_id": f"{vvoid[idx]:.0f}",
                "nearest_void_ra_deg": f"{vra[idx]:.12g}",
                "nearest_void_dec_deg": f"{vdec[idx]:.12g}",
                "nearest_void_center_distance_mpc_over_h": f"{float(dist[idx]):.12g}",
                "nearest_void_reff_mpc_over_h": f"{float(vreff[idx]):.12g}",
                "nearest_void_radius_mpc_over_h": f"{float(vradius[idx]):.12g}",
                "wall_distance_mpc_over_h": f"{wall:.12g}",
                "inside_effective_void_radius": str(wall <= 0.0).lower(),
                "angular_separation_to_void_center_deg": f"{float(angular_sep_deg(ra, dec, np.array([vra[idx]]), np.array([vdec[idx]]))[0]):.12g}",
                "endpoint_replay_allowed": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": "r1_r3_source_attachment_not_scoring_not_validation",
            }
        )
    return out


def build_environment(low_z_rows: list[dict[str, str]], pantheon_by_idx: dict[int, dict[str, str]]) -> list[dict[str, str]]:
    with fits.open(WEB_FITS) as hdul:
        data = hdul[1].data
        gra = np.asarray(data["ra"], dtype=float)
        gdec = np.asarray(data["dec"], dtype=float)
        gz = np.asarray(data["z"], dtype=float)
        gdens = np.asarray(data["matterDens"], dtype=float)
    usable = np.isfinite(gra) & np.isfinite(gdec) & np.isfinite(gz) & np.isfinite(gdens) & (gz > 0) & (gz < 3) & (gdens > -90)
    gra, gdec, gz, gdens = gra[usable], gdec[usable], gz[usable], gdens[usable]
    out: list[dict[str, str]] = []
    for row in low_z_rows:
        raw = pantheon_by_idx[int(row["source_row_index"])]
        host_ra = float(raw.get("HOST_RA", "-999"))
        host_dec = float(raw.get("HOST_DEC", "-999"))
        if host_ra != -999 and host_dec != -999:
            ra, dec, coord_source = host_ra, host_dec, "HOST_RA_DEC"
        else:
            ra, dec, coord_source = float(raw["RA"]), float(raw["DEC"]), "SN_RA_DEC_FALLBACK"
        z = float(row["zHD"])
        zmask = np.abs(gz - z) <= LOS_DZ_WINDOW
        if np.any(zmask):
            sep = angular_sep_deg(ra, dec, gra[zmask], gdec[zmask])
            cone = sep <= LOS_ANGULAR_RADIUS_DEG
            dens = gdens[zmask][cone]
            sep_cone = sep[cone]
        else:
            dens = np.array([], dtype=float)
            sep_cone = np.array([], dtype=float)
        if dens.size:
            median_density = float(np.median(dens))
            mean_density = float(np.mean(dens))
            nearest_sep = float(np.min(sep_cone))
            nearest_density = float(dens[int(np.argmin(sep_cone))])
        else:
            median_density = math.nan
            mean_density = math.nan
            nearest_sep = math.nan
            nearest_density = math.nan
        out.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_LOS_ENVIRONMENT_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "coordinate_source": coord_source,
                "ra_deg": f"{ra:.12g}",
                "dec_deg": f"{dec:.12g}",
                "los_dz_window": f"{LOS_DZ_WINDOW:.12g}",
                "los_angular_radius_deg": f"{LOS_ANGULAR_RADIUS_DEG:.12g}",
                "los_environment_count": str(int(dens.size)),
                "los_matter_density_median": "" if math.isnan(median_density) else f"{median_density:.12g}",
                "los_matter_density_mean": "" if math.isnan(mean_density) else f"{mean_density:.12g}",
                "nearest_environment_angular_sep_deg": "" if math.isnan(nearest_sep) else f"{nearest_sep:.12g}",
                "nearest_environment_matter_density": "" if math.isnan(nearest_density) else f"{nearest_density:.12g}",
                "endpoint_replay_allowed": "false",
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": "r1_r3_source_attachment_not_scoring_not_validation",
            }
        )
    return out


def main() -> None:
    acq_summary = read_one(ACQ_SUMMARY)
    if acq_summary["status"] != "VOID_SOURCE_BASIS_REFINEMENT_ACQUISITION_MANIFEST_BUILT_NOT_ATTACHED":
        raise SystemExit("R1-R3 attachment must start from frozen-not-attached manifest")
    if acq_summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("parent manifest must not allow replay")
    route_ids = {row["route_id"] for row in read_rows(ACQUISITION)}
    for route in ["R1_void_catalogue_object_properties", "R2_supernova_host_to_void_geometry", "R3_line_of_sight_environment"]:
        if route not in route_ids:
            raise SystemExit(f"missing acquisition route: {route}")

    voids = load_voids()
    inventory = read_rows(VOID_INVENTORY)
    pantheon_by_idx = load_pantheon_raw_by_source_index()
    low_z_rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    if not low_z_rows:
        raise SystemExit("low-z mask has no included rows")

    geometry = build_geometry(low_z_rows, pantheon_by_idx, voids)
    environment = build_environment(low_z_rows, pantheon_by_idx)

    void_inventory_row = next(row for row in inventory if row["frozen_product_id"] == "VOIDFINDER_PLANCK2018_MAXIMAL_VOID_TABLE")
    web_inventory_row = next(row for row in inventory if row["frozen_product_id"] == "SDSS_DR17_MCPM_SLIMEMOLD_GALAXY_CATALOG")
    env_with_counts = sum(int(row["los_environment_count"]) > 0 for row in environment)
    inside_void = sum(row["inside_effective_void_radius"] == "true" for row in geometry)
    attachment_rows = [
        {
            "attachment_id": "VOID_SOURCE_BASIS_REFINEMENT_R1_R3_SOURCE_ATTACHMENT_V1",
            "route_id": "R1_void_catalogue_object_properties",
            "attached_artifact": void_inventory_row["local_path"],
            "status": "ATTACHED_SOURCE_NATIVE_OBJECT_LEVEL_VOID_CATALOGUE",
            "rows_or_objects": void_inventory_row["observable_summary"].split(";")[0].split("=")[-1],
            "source_features_attached": "x;y;z;radius;void;edge;r;ra;dec;Reff",
            "endpoint_replay_allowed": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "r1_r3_source_attachment_not_scoring_not_validation",
        },
        {
            "attachment_id": "VOID_SOURCE_BASIS_REFINEMENT_R1_R3_SOURCE_ATTACHMENT_V1",
            "route_id": "R2_supernova_host_to_void_geometry",
            "attached_artifact": "data/derived/low_z_pantheon_void_geometry_join_v1.csv",
            "status": "BUILT_RESIDUAL_BLIND_LOW_Z_HOST_TO_VOID_GEOMETRY",
            "rows_or_objects": str(len(geometry)),
            "source_features_attached": "host_or_sn_coordinate_rule;nearest_void_id;center_distance;wall_distance;inside_effective_void_radius;angular_separation",
            "endpoint_replay_allowed": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "r1_r3_source_attachment_not_scoring_not_validation",
        },
        {
            "attachment_id": "VOID_SOURCE_BASIS_REFINEMENT_R1_R3_SOURCE_ATTACHMENT_V1",
            "route_id": "R3_line_of_sight_environment",
            "attached_artifact": "data/derived/low_z_pantheon_los_environment_v1.csv",
            "status": "BUILT_SOURCE_SIDE_LOW_Z_LINE_OF_SIGHT_ENVIRONMENT_PROXY",
            "rows_or_objects": str(len(environment)),
            "source_features_attached": "sdss_mcpm_matter_density;fixed_dz_window;fixed_angular_cone;environment_count;median_density;nearest_density",
            "endpoint_replay_allowed": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "r1_r3_source_attachment_not_scoring_not_validation",
        },
    ]
    summary = [
        {
            "attachment_id": "VOID_SOURCE_BASIS_REFINEMENT_R1_R3_SOURCE_ATTACHMENT_V1",
            "parent_manifest": acq_summary["policy_id"],
            "status": "R1_R3_SOURCE_ARTIFACTS_ATTACHED_R4_R6_STILL_OPEN",
            "attached_routes": "3",
            "required_routes": acq_summary["required_routes"],
            "low_z_rows": str(len(low_z_rows)),
            "void_catalogue_rows": attachment_rows[0]["rows_or_objects"],
            "host_to_void_geometry_rows": str(len(geometry)),
            "inside_effective_void_radius_rows": str(inside_void),
            "los_environment_rows": str(len(environment)),
            "los_environment_nonempty_rows": str(env_with_counts),
            "los_environment_source": web_inventory_row["local_path"],
            "los_dz_window": f"{LOS_DZ_WINDOW:.12g}",
            "los_angular_radius_deg": f"{LOS_ANGULAR_RADIUS_DEG:.12g}",
            "redshift_independence_preflight_complete": "false",
            "control_resistance_preflight_complete": "false",
            "leakage_review_complete": "false",
            "source_unique_ready": "false",
            "endpoint_replay_allowed": "false",
            "computes_new_scores": "false",
            "uses_distance_residuals": "false",
            "uses_fit_statistics": "false",
            "physical_validation_claimed": "false",
            "recommended_next_action": "run_R4_redshift_independence_preflight_then_R5_controls_then_R6_independent_leakage_review",
            "claim_boundary": "r1_r3_source_attachment_not_scoring_not_validation",
        }
    ]
    write_csv(OUT_GEOM, geometry)
    write_csv(OUT_ENV, environment)
    write_csv(OUT_ATTACH, attachment_rows)
    write_csv(OUT_SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R1_R3_SOURCE_ATTACHMENT_V1_BUILT "
        f"low_z_rows={len(low_z_rows)} los_nonempty={env_with_counts} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()

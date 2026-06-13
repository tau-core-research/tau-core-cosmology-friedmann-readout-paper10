#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_path_aware_void_geometry_policy_v1.csv"
VOID_TABLE = ROOT / "data/raw/public_void_catalog/vast_dr7_planck2018/VoidFinder-nsa_v1_0_1_Planck2018_comoving_maximal.txt"
PANTHEON_RAW = ROOT / "data/raw/pantheon_plus/pantheon_plus_mu_covariance/Pantheon+SH0ES.dat"
LOW_Z_MASK = ROOT / "data/derived/low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
OUT = ROOT / "data/derived/low_z_pantheon_path_aware_void_geometry_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_path_aware_void_geometry_v1_summary.csv"
CLAIM_BOUNDARY = "path_aware_void_geometry_source_side_not_scoring_not_validation"
D_H_MPC_OVER_H = 2997.92458


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
            rows.append({key: float(value) for key, value in zip(header, parts)})
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


def fmt(value: float) -> str:
    return f"{value:.12g}"


def valid_ra_dec(ra: float, dec: float) -> bool:
    return math.isfinite(ra) and math.isfinite(dec) and 0.0 <= ra <= 360.0 and -90.0 <= dec <= 90.0


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "PATH_AWARE_VOID_GEOMETRY_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("policy must not authorize replay or validation")
    voids = load_voids()
    pantheon = load_pantheon_raw_by_source_index()
    low_z_rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    centers = np.array([[v["x"], v["y"], v["z"]] for v in voids], dtype=float)
    reff = np.array([v["Reff"] for v in voids], dtype=float)
    radius = np.array([v["radius"] for v in voids], dtype=float)
    void_id = np.array([v["void"] for v in voids], dtype=float)
    rows: list[dict[str, str]] = []
    for row in low_z_rows:
        raw = pantheon[int(row["source_row_index"])]
        host_ra = float(raw.get("HOST_RA", "-999"))
        host_dec = float(raw.get("HOST_DEC", "-999"))
        if valid_ra_dec(host_ra, host_dec):
            ra, dec, coord_source = host_ra, host_dec, "HOST_RA_DEC"
        else:
            ra, dec, coord_source = float(raw["RA"]), float(raw["DEC"]), "SN_RA_DEC_FALLBACK"
        if not valid_ra_dec(ra, dec):
            raise SystemExit(f"invalid sky coordinate for {row['CID']}")
        source_radius = D_H_MPC_OVER_H * float(row["zHD"])
        sx, sy, sz = spherical_to_cartesian(ra, dec, source_radius)
        source_vec = np.array([sx, sy, sz], dtype=float)
        source_norm2 = float(np.dot(source_vec, source_vec))
        if source_norm2 <= 0.0:
            raise SystemExit(f"nonpositive source vector for {row['CID']}")
        t_raw = (
            centers[:, 0] * source_vec[0]
            + centers[:, 1] * source_vec[1]
            + centers[:, 2] * source_vec[2]
        ) / source_norm2
        t_clipped = np.clip(t_raw, 0.0, 1.0)
        closest = t_clipped[:, None] * source_vec[None, :]
        impact = np.linalg.norm(centers - closest, axis=1)
        idx = int(np.argmin(impact))
        crossing_margin = float(reff[idx] - impact[idx])
        intersects_segment = bool(crossing_margin >= 0.0 and 0.0 <= t_raw[idx] <= 1.0)
        segment_entry = math.nan
        segment_exit = math.nan
        path_chord = 0.0
        if intersects_segment:
            half = math.sqrt(max(0.0, float(reff[idx] ** 2 - impact[idx] ** 2))) / source_radius
            segment_entry = max(0.0, float(t_raw[idx] - half))
            segment_exit = min(1.0, float(t_raw[idx] + half))
            path_chord = max(0.0, segment_exit - segment_entry) * source_radius
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_PATH_AWARE_VOID_GEOMETRY_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "coordinate_source": coord_source,
                "ra_deg": fmt(ra),
                "dec_deg": fmt(dec),
                "source_radius_mpc_over_h": fmt(source_radius),
                "source_x_mpc_over_h": fmt(sx),
                "source_y_mpc_over_h": fmt(sy),
                "source_z_mpc_over_h": fmt(sz),
                "path_nearest_void_row_index": str(idx),
                "path_nearest_void_id": f"{void_id[idx]:.0f}",
                "path_closest_approach_fraction": fmt(float(t_clipped[idx])),
                "path_closest_approach_fraction_raw": fmt(float(t_raw[idx])),
                "path_closest_approach_distance_mpc_over_h": fmt(float(t_clipped[idx] * source_radius)),
                "path_impact_parameter_mpc_over_h": fmt(float(impact[idx])),
                "path_nearest_void_reff_mpc_over_h": fmt(float(reff[idx])),
                "path_nearest_void_radius_mpc_over_h": fmt(float(radius[idx])),
                "path_void_crossing_margin_mpc_over_h": fmt(crossing_margin),
                "path_intersects_effective_void": str(intersects_segment).lower(),
                "path_void_entry_fraction": "" if math.isnan(segment_entry) else fmt(segment_entry),
                "path_void_exit_fraction": "" if math.isnan(segment_exit) else fmt(segment_exit),
                "path_void_chord_length_mpc_over_h": fmt(path_chord),
                "path_void_depth_fraction": fmt(path_chord / source_radius if source_radius > 0.0 else 0.0),
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
    crossing_rows = [row for row in rows if row["path_intersects_effective_void"] == "true"]
    partial_crossing = [row for row in partial_rows if row["path_intersects_effective_void"] == "true"]
    nonzero_chord = [row for row in rows if float(row["path_void_chord_length_mpc_over_h"]) > 0.0]
    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_PATH_AWARE_VOID_GEOMETRY_V1",
            "status": "PATH_AWARE_VOID_GEOMETRY_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "void_catalogue_rows": str(len(voids)),
            "path_intersection_rows": str(len(crossing_rows)),
            "nonzero_chord_rows": str(len(nonzero_chord)),
            "partial_path_scope_rows": str(len(partial_rows)),
            "partial_path_scope_intersection_rows": str(len(partial_crossing)),
            "max_path_void_depth_fraction": fmt(max(float(row["path_void_depth_fraction"]) for row in rows)),
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "path_aware_void_geometry_available_as_source_observable_not_full_metric_path",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_PATH_AWARE_VOID_GEOMETRY_BUILT "
        f"rows={summary[0]['rows']} intersections={summary[0]['path_intersection_rows']} "
        f"partial_intersections={summary[0]['partial_path_scope_intersection_rows']}"
    )


if __name__ == "__main__":
    main()

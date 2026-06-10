#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOW_Z_GEOMETRY = ROOT / "data" / "derived" / "low_z_pantheon_void_geometry_join_v1.csv"
KIDS_TILES = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_crossmap_audit.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv"

ARTIFACT_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PROJECTION_CROSSMAP_AUDIT_V1"
CLAIM_BOUNDARY = "v2_path_projection_crossmap_audit_not_values_not_scoring"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def angular_sep_deg(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    ra1_rad = math.radians(ra1)
    ra2_rad = math.radians(ra2)
    dec1_rad = math.radians(dec1)
    dec2_rad = math.radians(dec2)
    cos_sep = (
        math.sin(dec1_rad) * math.sin(dec2_rad)
        + math.cos(dec1_rad) * math.cos(dec2_rad) * math.cos(ra1_rad - ra2_rad)
    )
    return math.degrees(math.acos(max(-1.0, min(1.0, cos_sep))))


def main() -> None:
    low_z_rows = read_rows(LOW_Z_GEOMETRY)
    tile_rows = read_rows(KIDS_TILES)
    if not low_z_rows:
        raise SystemExit("low-z geometry join is empty")
    if not tile_rows:
        raise SystemExit("KiDS tile inventory is empty")

    tiles = [
        {
            "tile_index_zero_based": row["tile_index_zero_based"],
            "ra": float(row["tile_ra_deg_filename_proxy"]),
            "dec": float(row["tile_dec_deg_filename_proxy"]),
            "coordinate_source": row["tile_coordinate_source"],
        }
        for row in tile_rows
    ]
    dec_values = [tile["dec"] for tile in tiles]
    ra_values = [tile["ra"] for tile in tiles]
    dec_min = min(dec_values)
    dec_max = max(dec_values)
    ra_min = min(ra_values)
    ra_max = max(ra_values)

    out_rows: list[dict[str, str]] = []
    for row in low_z_rows:
        ra = float(row["ra_deg"])
        dec = float(row["dec_deg"])
        nearest = min(tiles, key=lambda tile: angular_sep_deg(ra, dec, tile["ra"], tile["dec"]))
        sep = angular_sep_deg(ra, dec, nearest["ra"], nearest["dec"])
        inside_dec_envelope = dec_min <= dec <= dec_max
        inside_ra_envelope = ra_min <= ra <= ra_max
        nearest_within_one_deg = sep <= 1.0
        nearest_within_two_deg = sep <= 2.0
        if nearest_within_one_deg:
            status = "CROSSMAP_CANDIDATE_NEAREST_TILE_WITHIN_1_DEG"
        elif inside_dec_envelope and nearest_within_two_deg:
            status = "CROSSMAP_CANDIDATE_NEAREST_TILE_WITHIN_2_DEG"
        elif inside_dec_envelope:
            status = "DEC_ENVELOPE_ONLY_NO_TILE_MATCH"
        else:
            status = "OUTSIDE_KIDS_DEC_ENVELOPE"
        out_rows.append(
            {
                "artifact_id": ARTIFACT_ID,
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "coordinate_source": row["coordinate_source"],
                "ra_deg": f"{ra:.10f}",
                "dec_deg": f"{dec:.10f}",
                "kids_tile_inventory_available": "true",
                "kids_tile_coordinate_source": nearest["coordinate_source"],
                "nearest_kids_tile_index_zero_based": nearest["tile_index_zero_based"],
                "nearest_kids_tile_ra_deg": f"{nearest['ra']:.10f}",
                "nearest_kids_tile_dec_deg": f"{nearest['dec']:.10f}",
                "nearest_kids_tile_sep_deg": f"{sep:.10f}",
                "inside_kids_ra_filename_envelope": str(inside_ra_envelope).lower(),
                "inside_kids_dec_filename_envelope": str(inside_dec_envelope).lower(),
                "nearest_tile_within_1_deg": str(nearest_within_one_deg).lower(),
                "nearest_tile_within_2_deg": str(nearest_within_two_deg).lower(),
                "crossmap_candidate_status": status,
                "W_path_value_status": "NOT_COMPUTED_CROSSMAP_AUDIT_ONLY",
                "W_path_source_value": "NA",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_lensing_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_sky_direction_selection": "false",
                "uses_posthoc_path_projection_labels": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    n = len(out_rows)
    n_dec = sum(row["inside_kids_dec_filename_envelope"] == "true" for row in out_rows)
    n_1deg = sum(row["nearest_tile_within_1_deg"] == "true" for row in out_rows)
    n_2deg = sum(row["nearest_tile_within_2_deg"] == "true" for row in out_rows)
    summary = [
        {
            "artifact_id": ARTIFACT_ID,
            "status": "V2_PATH_PROJECTION_CROSSMAP_AUDIT_BUILT_VALUES_NOT_COMPUTED",
            "low_z_geometry_artifact": str(LOW_Z_GEOMETRY.relative_to(ROOT)),
            "kids_tile_inventory_artifact": str(KIDS_TILES.relative_to(ROOT)),
            "n_rows": str(n),
            "lowz_ra_dec_available": "true",
            "kids_tile_coordinate_inventory_available": "true",
            "kids_tile_count": str(len(tiles)),
            "kids_ra_min_deg_filename_proxy": f"{ra_min:.10f}",
            "kids_ra_max_deg_filename_proxy": f"{ra_max:.10f}",
            "kids_dec_min_deg_filename_proxy": f"{dec_min:.10f}",
            "kids_dec_max_deg_filename_proxy": f"{dec_max:.10f}",
            "rows_inside_kids_dec_filename_envelope": str(n_dec),
            "rows_nearest_tile_within_1_deg": str(n_1deg),
            "rows_nearest_tile_within_2_deg": str(n_2deg),
            "crossmap_candidate_available": str(n_1deg > 0 or n_2deg > 0).lower(),
            "crossmap_complete_for_lowz_scope": str(n_1deg == n).lower(),
            "path_values_computed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_lensing_residuals": "false",
            "contains_fit_statistics": "false",
            "verdict": "lowz_coordinates_available_but_path_values_not_computed",
            "recommended_next_action": "freeze_pantheon_to_kids_path_weight_rule_or_keep_path_blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, out_rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_PATH_PROJECTION_CROSSMAP_AUDIT_BUILT "
        f"rows={n} dec_envelope={n_dec} nearest_1deg={n_1deg} path_values_computed=false"
    )


if __name__ == "__main__":
    main()

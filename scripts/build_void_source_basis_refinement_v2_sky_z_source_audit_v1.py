#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH_VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_values.csv"
CROSSMAP = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_crossmap_audit.csv"
SUMMARY_REPLAY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_sky_z_authorized_replay_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_sky_z_source_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_sky_z_source_audit_v1_summary.csv"
CLAIM_BOUNDARY = "v2_sky_z_source_audit_not_scoring_not_validation"


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


def main() -> None:
    replay = read_one(SUMMARY_REPLAY)
    if replay["active_family"] != "W_path_x_sky_z":
        raise SystemExit("sky-z source audit requires the W_path_x_sky_z replay summary")
    if replay["endpoint_validation_claimed"] != "false":
        raise SystemExit("sky-z replay must not claim validation")
    cross_by_index = {row["source_row_index"]: row for row in read_rows(CROSSMAP)}
    rows = []
    raw_values = []
    for path in read_rows(PATH_VALUES):
        w_path = float(path["W_path_source_value"])
        if w_path <= 0.0:
            continue
        source_index = path["source_row_index"]
        cross = cross_by_index.get(source_index)
        if cross is None:
            raise SystemExit(f"missing crossmap row for source index {source_index}")
        if path["CID"] != cross["CID"]:
            raise SystemExit(f"CID mismatch for source index {source_index}")
        for label, row in [("path", path), ("crossmap", cross)]:
            if row.get("contains_distance_residuals", "false") != "false":
                raise SystemExit(f"{label} row contains distance residuals")
            if row.get("contains_fit_statistics", "false") != "false":
                raise SystemExit(f"{label} row contains fit statistics")
            if row.get("endpoint_validation_claimed", "false") != "false":
                raise SystemExit(f"{label} row claims validation")
        ra_deg = float(cross["ra_deg"])
        dec_deg = float(cross["dec_deg"])
        ra = math.radians(ra_deg)
        dec = math.radians(dec_deg)
        sky_x = math.cos(dec) * math.cos(ra)
        sky_y = math.cos(dec) * math.sin(ra)
        sky_z = math.sin(dec)
        raw = w_path * sky_z
        raw_values.append(raw)
        rows.append(
            {
                "artifact_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_SKY_Z_SOURCE_AUDIT_V1",
                "CID": path["CID"],
                "source_row_index": source_index,
                "zHD": path["zHD"],
                "ra_deg": f"{ra_deg:.12g}",
                "dec_deg": f"{dec_deg:.12g}",
                "sky_x": f"{sky_x:.12g}",
                "sky_y": f"{sky_y:.12g}",
                "sky_z": f"{sky_z:.12g}",
                "W_path_source_value": f"{w_path:.12g}",
                "W_path_x_sky_z_raw": f"{raw:.12g}",
                "nearest_kids_tile_sep_deg": cross["nearest_kids_tile_sep_deg"],
                "crossmap_candidate_status": cross["crossmap_candidate_status"],
                "contains_distance_residuals": "false",
                "contains_fit_statistics": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if len(rows) != 12:
        raise SystemExit(f"sky-z source audit requires exactly 12 rows, found {len(rows)}")
    max_abs = max(abs(value) for value in raw_values)
    if max_abs <= 0.0:
        raise SystemExit("sky-z source audit has zero max_abs")
    for row in rows:
        raw = float(row["W_path_x_sky_z_raw"])
        row["W_path_x_sky_z_normalized"] = f"{raw / max_abs:.12g}"
    rows.sort(key=lambda row: int(row["source_row_index"]))
    write_csv(OUT, rows)
    positives = sum(1 for value in raw_values if value > 0.0)
    negatives = sum(1 for value in raw_values if value < 0.0)
    summary = [
        {
            "artifact_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_SKY_Z_SOURCE_AUDIT_V1",
            "status": "V2_SKY_Z_SOURCE_AUDIT_BUILT_NOT_SCORING",
            "n_rows": str(len(rows)),
            "positive_raw_count": str(positives),
            "negative_raw_count": str(negatives),
            "max_abs_W_path_x_sky_z_raw": f"{max_abs:.12g}",
            "active_replay_family": replay["active_family"],
            "replay_verdict": replay["verdict"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "recommended_next_action": "predeclare_source_frozen_observer_orientation_kernel_v2_before_any_new_replay",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_SKY_Z_SOURCE_AUDIT_V1_BUILT "
        f"n_rows={len(rows)} positives={positives} negatives={negatives}"
    )


if __name__ == "__main__":
    main()


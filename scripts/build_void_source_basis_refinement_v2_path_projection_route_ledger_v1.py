#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOW_Z_MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
KIDS_INVENTORY = ROOT / "data" / "derived" / "kids1000_lensing_inventory_v1_summary.csv"
PATH_ROUTE = ROOT / "data" / "derived" / "kids1000_cosebis_path_source_product_route_manifest_v1.csv"
CROSSMAP = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_route_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv"

COMPONENT_ID = "V2_OBSERVER_PATH_PROJECTION"
CLAIM_BOUNDARY = "v2_path_projection_route_ledger_not_scoring_not_validation"


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
    low_z_rows = [row for row in read_rows(LOW_Z_MASK) if row["included"] == "true"]
    kids = read_one(KIDS_INVENTORY)
    route_rows = read_rows(PATH_ROUTE)
    crossmap = read_one(CROSSMAP)
    if not low_z_rows:
        raise SystemExit("no included low-z rows found")
    if kids["endpoint_scoring_allowed"] != "false":
        raise SystemExit("KiDS inventory must remain endpoint disabled")
    if any(row["endpoint_scoring_allowed"] != "false" for row in route_rows):
        raise SystemExit("path route manifest must remain endpoint disabled")
    source_supported_factors = sorted(
        {
            row["factor_id"]
            for row in route_rows
            if row["requirement_current_state"].startswith("available_")
            and row["route_status"] in {"already_source_supported_no_fetch", "alternative_not_needed_after_pixel_fraction_route"}
        }
    )
    route_supported = (
        {"F_overlap", "D_path"} <= set(source_supported_factors)
        and kids["status"] == "KIDS1000_LENSING_INVENTORY_BUILT_NOT_SCORED"
    )
    lowz_ra_dec_available = crossmap["lowz_ra_dec_available"] == "true"
    crossmap_candidate_available = crossmap["crossmap_candidate_available"] == "true"
    complete_crossmap_available = crossmap["crossmap_complete_for_lowz_scope"] == "true"
    if crossmap["path_values_computed"] != "false":
        raise SystemExit("crossmap audit must not compute path values")

    rows: list[dict[str, str]] = []
    for row in low_z_rows:
        rows.append(
            {
                "component_id": COMPONENT_ID,
                "channel_id": "W_PATH_PROJECTION",
                "source_scope": "LOW_Z_PANTHEON_VOID_SCOPE_CANDIDATE_POLICY_V1_INCLUDED_ROWS",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "kids_lensing_route_available": str(route_supported).lower(),
                "path_source_products_available": ";".join(source_supported_factors),
                "pantheon_lowz_ra_dec_available": str(lowz_ra_dec_available).lower(),
                "lowz_to_kids_path_crossmap_available": str(complete_crossmap_available).lower(),
                "lowz_to_kids_path_crossmap_candidate_available": str(crossmap_candidate_available).lower(),
                "crossmap_audit_artifact": str(CROSSMAP.relative_to(ROOT)),
                "W_path_value_status": "BLOCKED_PATH_WEIGHT_RULE_NOT_FROZEN_FOR_PANTHEON_ROWS",
                "W_path_source_value": "NA",
                "path_off_control": "0",
                "rotated_sky_control_available": "false",
                "shuffled_sky_direction_control_available": "false",
                "missing_next_artifact": "data/derived/void_source_basis_refinement_v2_path_projection_values.csv",
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

    summary = [
        {
            "component_id": COMPONENT_ID,
            "status": "V2_PATH_PROJECTION_ROUTE_LEDGER_FROZEN_VALUES_BLOCKED",
            "low_z_scope_artifact": str(LOW_Z_MASK.relative_to(ROOT)),
            "kids_inventory_artifact": str(KIDS_INVENTORY.relative_to(ROOT)),
            "path_route_artifact": str(PATH_ROUTE.relative_to(ROOT)),
            "crossmap_audit_artifact": str(CROSSMAP.relative_to(ROOT)),
            "output_artifact": str(OUT.relative_to(ROOT)),
            "n_rows": str(len(rows)),
            "kids_lensing_route_available": str(route_supported).lower(),
            "path_source_products_available": ";".join(source_supported_factors),
            "pantheon_lowz_ra_dec_available": str(lowz_ra_dec_available).lower(),
            "lowz_to_kids_path_crossmap_available": str(complete_crossmap_available).lower(),
            "lowz_to_kids_path_crossmap_candidate_available": str(crossmap_candidate_available).lower(),
            "path_values_computed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_lensing_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "verdict": "path_route_and_lowz_coordinates_available_but_path_weight_values_not_frozen",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_PATH_PROJECTION_ROUTE_LEDGER_BUILT "
        f"rows={len(rows)} route_available={str(route_supported).lower()} path_values_computed=false"
    )


if __name__ == "__main__":
    main()

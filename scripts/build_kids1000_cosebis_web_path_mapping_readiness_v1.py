#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_web_path_mapping_policy_v1.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1_summary.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_web_path_mapping_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    theory = read_one(THEORY)
    tomo = read_one(TOMO)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs web/path mapping policy must remain endpoint disabled")
    if policy["current_mapping_computed"].lower() != "false":
        raise SystemExit("COSEBIs web/path mapping must not be computed in this gate")
    if theory["contains_theory_vector"].lower() != "false":
        raise SystemExit("theory-vector readiness must not contain a theory vector")
    if policy["expected_target_rows"] != theory["expected_theory_vector_rows"]:
        raise SystemExit("web/path mapping target rows must match theory-vector target rows")
    if policy["expected_target_rows"] != tomo["data_vector_rows"]:
        raise SystemExit("web/path mapping target rows must match COSEBIs data-vector rows")

    required_products = policy["required_future_source_products"].split(";")
    row = {
        "policy_id": policy["policy_id"],
        "parent_policy": policy["parent_policy"],
        "selected_statistic": policy["selected_statistic"],
        "target_rows": policy["expected_target_rows"],
        "n_tomographic_pairs": tomo["n_tomographic_pairs"],
        "n_modes_per_pair": tomo["n_modes_per_pair"],
        "active_channels": policy["active_channels"],
        "mapping_status": policy["mapping_status"],
        "current_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_sky_direction_selection": "false",
        "required_future_source_product_count": str(len(required_products)),
        "required_future_source_products": policy["required_future_source_products"],
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_cosebis_web_path_mapping_readiness_not_validation",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    summary = dict(row)
    summary["status"] = "KIDS1000_COSEBIS_WEB_PATH_MAPPING_READINESS_BUILT_NOT_COMPUTED"
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_WEB_PATH_MAPPING_READINESS_V1_BUILT "
        f"rows={row['target_rows']} mapping_computed=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
